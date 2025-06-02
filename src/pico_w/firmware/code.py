import time
import board
from protocol import PicoSerialProtocol
from pumpe import MultiPumpController
from waage import HX711

class PumpenManager:
    def __init__(self):
        self.proto = PicoSerialProtocol()

        pump_pins = {
            "Rum": board.GP18,
            "Vodka": board.GP19,
            "Cola": board.GP20,
            "Tonic Water": board.GP21
        }

        ml_to_sec = {
            "Rum": 0.078,
            "Vodka": 0.077,
            "Cola": 0.077,
            "Tonic Water": 0.08
        }

        self.pump_controller = MultiPumpController(pump_pins, ml_to_sec)

        self.waage = HX711(board.GP2, board.GP3)
        self.waage.set_scale(960)
        print("Tare Waage...")
        self.waage.tare()

        self.rezept_queue = []
        self.current_rezept = []
        self.current_task = None
        self.current_rezept_name = ""
        self.finished_sent = False
        self.rezept_start_gewicht = None

    def wait_for_glas(self):
        print("Bitte Glas aufstellen...")
        while True:
            gewicht = self.get_stable_weight()
            print(f"[DEBUG] Warte auf Glas... Gewicht: {gewicht:.1f}g")
            if gewicht >= 20:
                self.rezept_start_gewicht = gewicht
                print(f"[INFO] Glas erkannt mit {gewicht:.1f}g")
                break
            time.sleep(0.2)

    def wait_for_glas_entfernt(self):
        print("Bitte Glas entfernen...")
        while True:
            gewicht = self.get_stable_weight()
            print(f"[DEBUG] Warte auf Glasentfernung... Gewicht: {gewicht:.1f}g")
            if gewicht < 20:
                print("[INFO] Glas entfernt")
                break
            time.sleep(0.2)

    def get_stable_weight(self, samples=3, delay=0.01, max_jump=100.0):
        """Lese Gewicht mehrfach, verwerfe Ausreißer über 100g Unterschied."""
        readings = []
        last_valid = None

        for _ in range(samples * 2):
            raw = self.waage.get_units()
            if last_valid is None or abs(raw - last_valid) <= max_jump:
                readings.append(raw)
                last_valid = raw
            else:
                print(f"[WARNUNG] Gewichtssprung ignoriert: {raw:.1f}g (letzter gültiger: {last_valid:.1f}g)")
            time.sleep(delay)
            if len(readings) >= samples:
                break

        if not readings:
            print("[WARNUNG] Keine gültigen Gewichtsdaten – Rückgabe 0.0")
            return 0.0

        readings.sort()
        return readings[len(readings) // 2]

    def process_message(self, msg):
        print("Empfangen:", msg)

        if msg.get("command") == "prepare" and "ingredients" in msg:
            rezeptname = msg.get("recipe", "Unbenannt")
            ingredients = msg["ingredients"]
            tasks = []
            ignored = []

            for ingredient, menge_ml in ingredients.items():
                if ingredient not in self.pump_controller.ml_to_sec:
                    print(f"Ignoriere unbekannte Zutat: {ingredient}")
                    ignored.append(ingredient)
                    continue

                duration = self.pump_controller.ml_to_duration(ingredient, menge_ml)
                tasks.append({
                    "ingredient": ingredient,
                    "duration": duration,
                    "menge_ml": menge_ml
                })

            if tasks:
                # Glas steht evtl. schon da
                gewicht = self.get_stable_weight()
                if gewicht >= 20:
                    self.rezept_start_gewicht = gewicht
                    print(f"[INFO] Glas erkannt mit {gewicht:.1f}g (frühzeitig)")
                else:
                    self.rezept_start_gewicht = None

                self.rezept_queue.append({"name": rezeptname, "tasks": tasks})

                response = {
                    "status": "ok",
                    "action": f"{len(tasks)} gültige Zutaten für Rezept '{rezeptname}' aufgenommen"
                }
                if ignored:
                    response["ignored"] = ignored

                self.proto.send_response(response)
            else:
                self.proto.send_response({
                    "status": "error",
                    "message": f"Keine gültigen Zutaten im Rezept '{rezeptname}'"
                })
        else:
            self.proto.send_response({"status": "error", "message": "Ungültiges Format oder Befehl"})

    def update(self):
        if not self.current_task and not self.current_rezept and self.rezept_queue:
            if self.rezept_start_gewicht is None:
                self.wait_for_glas()
            rezept = self.rezept_queue.pop(0)
            self.current_rezept = rezept["tasks"]
            self.current_rezept_name = rezept.get("name", "Unbekannt")
            self.finished_sent = False

        if self.current_task is None and self.current_rezept:
            self.current_task = self.current_rezept.pop(0)
            ingredient = self.current_task["ingredient"]
            menge_ml = self.current_task["menge_ml"]
            zielgewicht = self.rezept_start_gewicht + menge_ml

            print(f"Starte Pumpe {ingredient} - Zielgewicht: {zielgewicht:.1f}g")
            self.pump_controller.start_pump(ingredient)

            nachlauf_puffer = 5.0
            nachlauf_zeit = 0.1

            while True:
                aktuelles_gewicht = self.get_stable_weight()
                print(f"[DEBUG] Gewicht: {aktuelles_gewicht:.1f}g / Ziel: {zielgewicht:.1f}g")

                if aktuelles_gewicht < self.rezept_start_gewicht - 10:
                    print("[WARNUNG] Glas wurde entfernt während Befüllung!")
                    self.pump_controller.stop_pump(ingredient)
                    self.proto.send_response({
                        "status": "error",
                        "message": f"Abbruch: Glas wurde entfernt während {ingredient}-Befüllung"
                    })
                    self.current_task = None
                    self.current_rezept = []
                    self.rezept_queue = []
                    self.finished_sent = True
                    self.wait_for_glas_entfernt()
                    return

                if aktuelles_gewicht >= (zielgewicht - nachlauf_puffer):
                    print(f"Stoppe Pumpe kurz vor Ziel bei {aktuelles_gewicht:.1f}g (Ziel - Puffer: {zielgewicht - nachlauf_puffer:.1f}g)")
                    self.pump_controller.stop_pump(ingredient)
                    time.sleep(nachlauf_zeit)
                    gewicht_nach_nachlauf = self.get_stable_weight()
                    print(f"[DEBUG] Gewicht nach Nachlauf: {gewicht_nach_nachlauf:.1f}g")
                    break

                time.sleep(0.05)

            print(f"Pumpe {ingredient} gestoppt bei {gewicht_nach_nachlauf:.1f}g")
            self.rezept_start_gewicht = gewicht_nach_nachlauf
            self.current_task = None

            if not self.current_rezept and not self.finished_sent:
                self.proto.send_response({
                    "status": "ok",
                    "message": f"Rezept '{self.current_rezept_name}' abgeschlossen"
                })
                self.finished_sent = True
                self.wait_for_glas_entfernt()

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
