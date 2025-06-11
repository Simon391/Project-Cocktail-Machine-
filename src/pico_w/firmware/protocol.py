import usb_cdc
import json

# Klasse für die Kommunikation über die serielle USB-Datenverbindung
class PicoSerialProtocol:
    def __init__(self):
        # Verwende den USB-Datenkanal (nicht die Standard-Konsole)
        self.serial = usb_cdc.data

        # Interner Puffer für eingehende Bytes
        self.buffer = bytearray()

        print("Pico startet Kommunikation...")

    def read_message(self):
        """
        Liest Bytes von der seriellen Schnittstelle, bis ein '\n' empfangen wird.
        Versucht dann, die empfangene Zeichenkette als JSON zu parsen.
        Gibt das JSON-Objekt zurück oder None, falls noch keine vollständige Nachricht vorliegt.
        """
        while self.serial.in_waiting:
            byte = self.serial.read(1)
            if byte == b'\n':
                try:
                    # Vollständige Zeile empfangen, versuche zu parsen
                    line = self.buffer.decode().strip()
                    self.buffer = bytearray()  # Puffer zurücksetzen
                    msg = json.loads(line)  # JSON parsen
                    return msg
                except Exception as e:
                    # Fehler beim Parsen – Zeile verwerfen
                    print("Fehler beim Parsen:", e)
                    self.buffer = bytearray()
            else:
                # Weitere Bytes im Puffer sammeln
                self.buffer.extend(byte)

        # Noch keine vollständige Nachricht
        return None

    def send_response(self, msg_dict):
        """
        Sendet ein Dictionary als JSON-Zeichenkette über die serielle Verbindung.
        Fügt automatisch ein '\n' hinzu, um das Nachrichtenende zu signalisieren.
        """
        msg_json = json.dumps(msg_dict) + "\n"
        self.serial.write(msg_json.encode())

