import usb_cdc
import json

class PicoSerialProtocol:
    def __init__(self):
        self.serial = usb_cdc.data
        self.buffer = bytearray()
        print("Pico startet Kommunikation...")

    def read_message(self):
        """
        Liest Bytes bis '\n' und gibt ein geparstes JSON-Objekt zurück,
        oder None, wenn noch keine vollständige Nachricht da ist.
        """
        while self.serial.in_waiting:
            byte = self.serial.read(1)
            if byte == b'\n':
                try:
                    line = self.buffer.decode().strip()
                    self.buffer = bytearray()
                    msg = json.loads(line)
                    return msg
                except Exception as e:
                    print("Fehler beim Parsen:", e)
                    self.buffer = bytearray()
            else:
                self.buffer.extend(byte)
        return None

    def send_response(self, msg_dict):
        """
        Sendet ein Dictionary als JSON mit Zeilenumbruch.
        """
        msg_json = json.dumps(msg_dict) + "\n"
        self.serial.write(msg_json.encode())

