from sorting_algorithms import QuickSort, BubbleSort, HashTable, BinarySearch

class CocktailDataManager:
    def __init__(self):
        # Initialisierung der Datenstrukturen
        self.cocktails = {}  # Hauptdatenbank aller Cocktails
        self.sorted_cocktails = []  # Liste für sortierte Cocktail-Namen

        # Algorithmus-Instanzen initialisieren
        self.quicksort = QuickSort([])  # Für schnelles Sortieren nach Namen
        self.bubblesort = BubbleSort([])  # Für Sortieren nach anderen Kriterien
        self.hashtable = HashTable()  # Für schnellen Zugriff auf einzelne Cocktails
        self.binarysearch = BinarySearch([])  # Für Suche in sortierten Listen

        # Beispieldaten laden und initial sortieren
        self.load_sample_data()
        self.sort_data()

        self.cocktails = {
            "Dark & Stormy Twist": {
                "Ingredients": {"Rum": "50", "Cola": "100", "Tonic Water": "20", "Lime Juice": "10"},
                "Notes": "Mit Limettenscheibe garnieren",
                "Category": "Classic",
                "Popularity": 7,
                "Price": 8
            },
            "Vodka Tonic Cola": {
                "Ingredients": {"Vodka": "40", "Tonic Water": "100", "Cola": "60", "Lemon Juice": "10"},
                "Notes": "Eiskalt servieren",
                "Category": "Classic",
                "Popularity": 8,
                "Price": 9
            },
            "Rum & Vodka Fusion": {
                "Ingredients": {"Rum": "30", "Vodka": "30", "Cola": "80", "Tonic Water": "20"},
                "Notes": "Mit Minzblatt garnieren",
                "Category": "Creative",
                "Popularity": 9,
                "Price": 10
            },
            "Cola Tonic Highball": {
                "Ingredients": {"Cola": "100", "Tonic Water": "50", "Rum": "40"},
                "Notes": "Mit Zitronenscheibe garnieren",
                "Category": "Highball",
                "Popularity": 7,
                "Price": 8
            },
            "Vodka Cola Spritz": {
                "Ingredients": {"Vodka": "40", "Cola": "80", "Tonic Water": "20"},
                "Notes": "Mit Limettenscheibe servieren",
                "Category": "Refreshing",
                "Popularity": 8,
                "Price": 9
            },
            "Tonic Rum Cooler": {
                "Ingredients": {"Rum": "50", "Tonic Water": "100"},
                "Notes": "Eiswürfel hinzufügen",
                "Category": "Classic",
                "Popularity": 7,
                "Price": 8
            },
            "Cola Vodka Breeze": {
                "Ingredients": {"Cola": "80", "Vodka": "40", "Lemon Juice": "10"},
                "Notes": "Mit Zitronenscheibe servieren",
                "Category": "Citrus",
                "Popularity": 8,
                "Price": 9
            },
            "Tonic Cola Punch": {
                "Ingredients": {"Tonic Water": "50", "Cola": "80", "Rum": "40", "Vodka": "30"},
                "Notes": "Mit Orangenzeste garnieren",
                "Category": "Party",
                "Popularity": 9,
                "Price": 10
            },
            "Rum & Cola Classic": {
                "Ingredients": {"Rum": "50", "Cola": "100", "Lime Juice": "10"},
                "Notes": "Mit Limettenscheibe servieren",
                "Category": "Classic",
                "Popularity": 7,
                "Price": 8
            },
            "Vodka Tonic Delight": {
                "Ingredients": {"Vodka": "40", "Tonic Water": "100", "Mint": "2"},
                "Notes": "Mit Minzblatt garnieren",
                "Category": "Fresh",
                "Popularity": 8,
                "Price": 9
            }
        }
        # Initiale Speicherung aller Cocktails in der Hashtable
        self.hashtable.insert(self.cocktails)

    def update_popularity_scores(self, scores):
        # Aktualisiert die Beliebtheitswerte für Cocktails
        for name, popularity in scores.items():
            if name in self.cocktails:
                self.cocktails[name]["Popularity"] = popularity
        self.sort_data()  # Daten neu sortieren nach Änderung

    def update_prices(self, prices):
        # Aktualisiert die Preise für Cocktails
        for name, price in prices.items():
            if name in self.cocktails:
                self.cocktails[name]["Price"] = price
        self.sort_data()  # Daten neu sortieren nach Änderung

    def add_cocktail(self, name, ingredients, notes, category="Other", popularity=5, price=10):
        # Fügt einen neuen Cocktail hinzu
        self.cocktails[name] = {
            "Ingredients": ingredients,
            "Notes": notes,
            "Category": category,
            "Popularity": popularity,
            "Price": price
        }
        # Cocktail in Hashtable einfügen und Daten neu sortieren
        self.hashtable.insert({name: self.cocktails[name]})
        self.sort_data()

    def sort_data(self, criteria="Name", order="Aufsteigend"):
        # Sortiert die Cocktails nach verschiedenen Kriterien
        keys = list(self.cocktails.keys())
        reverse = (order == "Absteigend")  # Sortierreihenfolge bestimmen

        if criteria == "Name":
            # Quicksort für Namen verwenden
            self.quicksort.original_data = keys
            sorted_keys = self.quicksort.sort(reverse=reverse)
        else:
            # Temporäre Liste mit Tupeln (Name, Sortierwert) erstellen
            if criteria == "Beliebtheit":
                temp_list = [(x, self.cocktails[x].get("Popularity", 0)) for x in keys]
            elif criteria == "Preis":
                temp_list = [(x, self.cocktails[x].get("Price", 0)) for x in keys]
            elif criteria == "Zutatenanzahl":
                temp_list = [(x, len(self.cocktails[x]["Ingredients"])) for x in keys]
            else:
                temp_list = [(x, x) for x in keys]  # Fallback

            # Key-Funktion für den Vergleich des zweiten Tupel-Elements
            def sort_key(item):
                return item[1]

            # BubbleSort mit angepasster Vergleichslogik
            self.bubblesort.original_data = temp_list
            sorted_pairs = self.bubblesort.sort(reverse=reverse, key=sort_key)
            sorted_keys = [x[0] for x in sorted_pairs]  # Nur die Namen extrahieren

        # Sortierte Liste speichern und BinarySearch aktualisieren
        self.sorted_cocktails = sorted_keys
        self.binarysearch.data = sorted_keys  # Für spätere Suche vorbereiten
        return sorted_keys

    def get_cocktail(self, name):
        # Holt einen einzelnen Cocktail aus der Hashtable
        return self.hashtable.get(name)

    def get_all_cocktails(self):
        # Gibt eine Kopie aller Cocktails zurück
        return self.cocktails.copy()

    def search_cocktail(self, name):
        # Sucht einen Cocktail mit BinarySearch
        index = self.binarysearch.search(name)
        if index != -1:  # Wenn gefunden
            result_name = self.sorted_cocktails[index]
            return self.get_cocktail(result_name)
        return None  # Wenn nicht gefunden

    def delete_cocktail(self, name):
        # Löscht einen Cocktail aus allen Datenstrukturen
        if name in self.cocktails:
            del self.cocktails[name]
            self.hashtable.delete(name)
            self.sort_data()  # Daten neu sortieren nach Löschung
            return True
        return False  # Wenn Cocktail nicht existiert