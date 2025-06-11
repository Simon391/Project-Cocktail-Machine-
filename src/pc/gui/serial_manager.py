import serial
import serial.tools.list_ports
import threading
import time
import json
from typing import Callable, Dict, List


class SerialManager:
    def __init__(self):
        self.serial_conn = None
        self.running = False
        self.port = None
        self.baudrate = 115200
        self.event_handlers = {
            'connected': [],
            'disconnected': [],
            'message_received': [],
            'error': []
        }
        self._receive_thread = None
        self._heartbeat_thread = None
        self.heartbeat_interval = 2.0
        self.enable_heartbeat = True

    def register_handler(self, event: str, handler: Callable):
        if event in self.event_handlers:
            self.event_handlers[event].append(handler)

    def _notify_handlers(self, event: str, *args):
        for handler in self.event_handlers.get(event, []):
            handler(*args)

    def connect(self, port: str) -> bool:
        try:
            self.serial_conn = serial.Serial(port, self.baudrate, timeout=1)
            self.port = port
            self.running = True
            self._start_threads()
            self._notify_handlers('connected')
            return True
        except serial.SerialException as e:
            self._notify_handlers('error', f"Connection failed: {str(e)}")
            return False

    def disconnect(self):
        self.running = False
        if self._receive_thread and self._receive_thread.is_alive():
            self._receive_thread.join()
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_thread.join()
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        self._notify_handlers('disconnected')

    def reconnect(self) -> bool:
        self.disconnect()
        time.sleep(1)
        return self.connect(self.port)

    def send_message(self, message: str):
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write((message + '\n').encode('utf-8'))
            except serial.SerialException as e:
                self._notify_handlers('error', f"Send failed: {str(e)}")

    def send_cocktail_recipe(self, name: str, ingredients: Dict[str, int]):
        recipe = {
            "command": "prepare",
            "recipe": name,
            "ingredients": ingredients
        }
        self.send_message(json.dumps(recipe))

    def _start_threads(self):
        self._receive_thread = threading.Thread(
            target=self._receive_loop,
            daemon=True
        )
        self._receive_thread.start()

        if self.enable_heartbeat:
            self._heartbeat_thread = threading.Thread(
                target=self._heartbeat_loop,
                daemon=True
            )
            self._heartbeat_thread.start()

    def _receive_loop(self):
        buffer = ""
        while self.running and self.serial_conn and self.serial_conn.is_open:
            try:
                if self.serial_conn.in_waiting > 0:
                    data = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8')
                    buffer += data

                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        self._notify_handlers('message_received', line.strip())
            except serial.SerialException as e:
                self._notify_handlers('error', f"Receive error: {str(e)}")
                self.disconnect()
                break

    def _heartbeat_loop(self):
        while self.running:
            self.send_message("HEARTBEAT")
            time.sleep(self.heartbeat_interval)

    @staticmethod
    def list_ports() -> List[str]:
        return [port.device for port in serial.tools.list_ports.comports()]
