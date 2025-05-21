import digitalio
import board

class MultiPumpController:
    def __init__(self, pump_pins, ml_to_sec_map):
        """
        pump_pins: dict {'zutat': Pin-Objekt (z. B. board.GP18)}
        ml_to_sec_map: dict {'zutat': sekunden_pro_ml (z. B. 0.5)}
        """
        self.pumps = {}
        self.ml_to_sec = ml_to_sec_map

        for ingredient, pin in pump_pins.items():
            p = digitalio.DigitalInOut(pin)
            p.direction = digitalio.Direction.OUTPUT
            p.value = True  # HIGH = AUS
            self.pumps[ingredient] = p

    def start_pump(self, ingredient):
        """Aktiviert die Pumpe (LOW = EIN)."""
        pump = self.pumps.get(ingredient)
        if pump:
            pump.value = False
            print(f"Pumpe {ingredient} eingeschaltet")
        else:
            print(f"Pumpe {ingredient} nicht gefunden")

    def stop_pump(self, ingredient):
        """Deaktiviert die Pumpe (HIGH = AUS)."""
        pump = self.pumps.get(ingredient)
        if pump:
            pump.value = True
            print(f"Pumpe {ingredient} ausgeschaltet")
        else:
            print(f"Pumpe {ingredient} nicht gefunden")

    def ml_to_duration(self, ingredient, menge_ml):
        """
        Rechnet die Menge in ml in Sekunden um, basierend auf ml_to_sec_map.
        Gibt die Pumpdauer in Sekunden zurück.
        """
        faktor = self.ml_to_sec.get(ingredient)
        if faktor:
            return menge_ml * faktor
        else:
            print(f"Keine Kalibrierung für {ingredient}, Standardwert 1s/ml verwendet")
            return menge_ml  # default: 1s pro ml

