import time
import board
from protocol import PicoSerialProtocol          # Kommunikation mit dem Host
from pumpe import MultiPumpController            # Pumpensteuerung

class PumpenManager:
    def __init__(self):
        self.proto = PicoSerialProtocol()

        # Zutat → GPIO
        pump_pins = {
            "wasser": board.GP18,
            "zucker": board.GP19,
            "saft": board.GP20,
            "sirup": board.GP21
        }

        # Zutat → Sekunden pro Milliliter
        ml_to_sec = {
            "wasser": 0.4,
            "zucker": 0.6,
            "saft": 0.5,
            "sirup": 0.7
        }

        self.pump_controller = MultiPumpController(pump_pins, ml_to_sec)

        self.rezept_queue = []      # Warteschlange von Rezepten (Liste von Task-Listen)
        self.current_rezept = []    # Aktuell ausgeführtes Rezept (Liste von Tasks)
        self.current_task = None    # Aktueller Task (Zutat + Dauer)
        self.task_end_time = 0      # Zeitpunkt, wann aktueller Task endet
        self.finished_sent = False  # Wurde das aktuelle Rezept abgeschlossen gemeldet

    def process_message(self, msg):
        print("Empfangen:", msg)

        # Einzelpumpe (als Task)
        if msg.get("command") == "pump":
            task = {"ingredient": msg["ingredient"]}

            if "duration" in msg:
                task["duration"] = msg["duration"]
            elif "menge_ml" in msg:
                task["duration"] = self.pump_controller.ml_to_duration(msg["ingredient"], msg["menge_ml"])
            else:
                self.proto.send_response({"status": "error", "message": "Keine Dauer oder Menge angegeben"})
                return

            self.rezept_queue.append([task])
            self.proto.send_response({"status": "ok", "action": "Einzelauftrag aufgenommen"})

        # Rezept mit mehreren Tasks
        elif "Rezept" in msg and "tasks" in msg:
            rezeptname = msg.get("Rezept", "Unbenannt")
            tasks = []

            for task_data in msg["tasks"]:
                ingredient = task_data["ingredient"]

                if "duration" in task_data:
                    duration = task_data["duration"]
                elif "menge_ml" in task_data:
                    duration = self.pump_controller.ml_to_duration(ingredient, task_data["menge_ml"])
                else:
                    continue

                tasks.append({
                    "ingredient": ingredient,
                    "duration": duration
                })

            if tasks:
                self.rezept_queue.append({"name": rezeptname, "tasks": tasks})
                self.proto.send_response({"status": "ok", "action": f"{len(tasks)} Aufgaben für Rezept '{rezeptname}' angenommen"})
            else:
                self.proto.send_response({"status": "error", "message": "Keine gültigen Aufgaben im Rezept"})

        else:
            self.proto.send_response({"status": "error", "message": "Unbekannter Befehl"})

    def update(self):
        now = time.monotonic()

        # Neues Rezept starten, falls keines aktiv
        if not self.current_task and not self.current_rezept and self.rezept_queue:
            rezept = self.rezept_queue.pop(0)
            self.current_rezept = rezept["tasks"]
            self.current_rezept_name = rezept.get("name", "Unbekannt")
            self.finished_sent = False

        # Nächsten Task aus aktuellem Rezept starten
        if self.current_task is None and self.current_rezept:
            self.current_task = self.current_rezept.pop(0)
            ingredient = self.current_task["ingredient"]
            duration = self.current_task["duration"]

            self.pump_controller.start_pump(ingredient)
            self.task_end_time = now + duration
            print(f"Starte Pumpe {ingredient} für {duration:.2f} Sekunden")

        # Aktuellen Task beenden
        if self.current_task and now >= self.task_end_time:
            self.pump_controller.stop_pump(self.current_task["ingredient"])
            print(f"Pumpe {self.current_task['ingredient']} fertig")
            self.current_task = None

            # Rezept abgeschlossen
            if not self.current_rezept and not self.finished_sent:
                self.proto.send_response({
                    "status": "ok",
                    "message": f"Rezept '{self.current_rezept_name}' abgeschlossen"
                })
                self.finished_sent = True

    def loop(self):
        print("Starte Hauptschleife...")
        while True:
            msg = self.proto.read_message()
            if msg:
                self.process_message(msg)
            self.update()
            time.sleep(0.05)


if __name__ == "__main__":
    manager = PumpenManager()
    manager.loop()
