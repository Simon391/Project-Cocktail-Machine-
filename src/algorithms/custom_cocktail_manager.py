import json

class CustomCocktailManager:
    """ Speichert experimentelle Cocktails in einer JSON-Datei """
    
    def __init__(self, datei="custom_cocktails.json"):
        self.datei = datei
        self.experimentelle_cocktails = self.lade_cocktails()  # Lade bestehende Cocktails

    def lade_cocktails(self):
        """ Lädt experimentelle Cocktails aus der JSON-Datei """
        try:
            with open(self.datei, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []  # Falls die Datei nicht existiert, starten mit leerer Liste

    def speichere_cocktails(self):
        """ Speichert experimentelle Cocktails dauerhaft """
        with open(self.datei, "w") as file:
            json.dump(self.experimentelle_cocktails, file, indent=4)

    def add_cocktail(self, name, zutaten):
        """ Fügt einen neuen Cocktail hinzu & speichert ihn dauerhaft """
        neuer_cocktail = {
            "name": name.strip(),
            "zutaten": zutaten,
            "kategorie": "Experimentell",
            "preis": 0  # Standardpreis
        }
        
        self.experimentelle_cocktails.append(neuer_cocktail)
        self.speichere_cocktails()  # Sofort speichern
        
        print(f"\n🎉 Dein Cocktail '{name}' wurde erfolgreich gespeichert!")

    def get_experimentelle_cocktails(self):
        """ Gibt alle experimentellen Cocktails zurück """
        return self.experimentelle_cocktails
