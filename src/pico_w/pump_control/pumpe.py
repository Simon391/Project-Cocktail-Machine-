import digitalio
import board

# Klasse zur Steuerung mehrerer Pumpen über GPIO-Pins
class MultiPumpController:
    def __init__(self, pump_pins, ml_to_sec_map):
        # Dictionary zur Speicherung der digitalen Ausgänge für jede Pumpe
        self.pumps = {}

        # Umrechnungstabelle von ml zu Pumpdauer in Sekunden
        self.ml_to_sec = ml_to_sec_map

        # Initialisiere alle Pumpen-Pins
        for ingredient, pin in pump_pins.items():
            p = digitalio.DigitalInOut(pin)       # Erstelle digitalen Ausgang
            p.direction = digitalio.Direction.OUTPUT  # Setze Richtung auf OUTPUT
            p.value = True  # Standard: True = AUS (Pumpe deaktiviert)
            self.pumps[ingredient] = p  # Speichere Pumpe im Dictionary

    def start_pump(self, ingredient):
        """Aktiviert die Pumpe für die angegebene Zutat (False = EIN)."""
        pump = self.pumps.get(ingredient)
        if pump:
            pump.value = False  # Aktiviert die Pumpe (LOW)
            print(f"Pumpe {ingredient} eingeschaltet")
        else:
            print(f"Pumpe {ingredient} nicht gefunden")

    def stop_pump(self, ingredient):
        """Deaktiviert die Pumpe für die angegebene Zutat (True = AUS)."""
        pump = self.pumps.get(ingredient)
        if pump:
            pump.value = True  # Deaktiviert die Pumpe (HIGH)
            print(f"Pumpe {ingredient} ausgeschaltet")
        else:
            print(f"Pumpe {ingredient} nicht gefunden")

    def ml_to_duration(self, ingredient, menge_ml):
        """
        Rechnet die gewünschte Menge (in ml) in Pumpdauer (in Sekunden) um.
        Verwendet die vorher definierte Kalibrierung (ml_to_sec_map).
        """
        faktor = self.ml_to_sec.get(ingredient)
        if faktor:
            return menge_ml * faktor
        else:
            print(f"Keine Kalibrierung für {ingredient}, Standardwert 1s/ml verwendet")
            return menge_ml  # Fallback: 1 Sekunde pro ml

