from sorting_algorithms import QuickSort, BubbleSort, HashTable, BinarySearch

class CocktailDataManager:
    def __init__(self):
        self.cocktails = {}
        self.popularity_scores = {}
        self.prices = {}
        self.sorted_cocktails = []

        # Algorithmus-Instanzen
        self.quicksort = QuickSort([])
        self.bubblesort = BubbleSort([])
        self.hashtable = HashTable()  # Keine Größe mehr übergeben, verwendet Standardwert
        self.binarysearch = BinarySearch([])

        self.load_sample_data()
        self.sort_data()

    def load_sample_data(self):
        self.cocktails = {
            "Dark & Stormy Twist": {
                "Ingredients": {"Rum": "50", "Cola": "100", "Tonic Water": "20", "Lime Juice": "10"},
                "Notes": "Mit Limettenscheibe garnieren",
                "Category": "Classic"
            },
            "Vodka Tonic Cola": {
                "Ingredients": {"Vodka": "40", "Tonic Water": "100", "Cola": "60", "Lemon Juice": "10"},
                "Notes": "Eiskalt servieren",
                "Category": "Classic"
            },
            "Rum & Vodka Fusion": {
                "Ingredients": {"Rum": "30", "Vodka": "30", "Cola": "80", "Tonic Water": "20"},
                "Notes": "Mit Minzblatt garnieren",
                "Category": "Creative"
            },
            "Cola Tonic Highball": {
                "Ingredients": {"Cola": "100", "Tonic Water": "50", "Rum": "40"},
                "Notes": "Mit Zitronenscheibe garnieren",
                "Category": "Highball"
            },
            "Vodka Cola Spritz": {
                "Ingredients": {"Vodka": "40", "Cola": "80", "Tonic Water": "20"},
                "Notes": "Mit Limettenscheibe servieren",
                "Category": "Refreshing"
            },
            "Tonic Rum Cooler": {
                "Ingredients": {"Rum": "50", "Tonic Water": "100"},
                "Notes": "Eiswürfel hinzufügen",
                "Category": "Classic"
            },
            "Cola Vodka Breeze": {
                "Ingredients": {"Cola": "80", "Vodka": "40", "Lemon Juice": "10"},
                "Notes": "Mit Zitronenscheibe servieren",
                "Category": "Citrus"
            },
            "Tonic Cola Punch": {
                "Ingredients": {"Tonic Water": "50", "Cola": "80", "Rum": "40", "Vodka": "30"},
                "Notes": "Mit Orangenzeste garnieren",
                "Category": "Party"
            },
            "Rum & Cola Classic": {
                "Ingredients": {"Rum": "50", "Cola": "100", "Lime Juice": "10"},
                "Notes": "Mit Limettenscheibe servieren",
                "Category": "Classic"
            },
            "Vodka Tonic Delight": {
                "Ingredients": {"Vodka": "40", "Tonic Water": "100", "Mint": "2"},
                "Notes": "Mit Minzblatt garnieren",
                "Category": "Fresh"
            }
        }

        self.popularity_scores = {name: 7 + idx % 3 for idx, name in enumerate(self.cocktails)}
        self.prices = {name: 8 + idx % 5 for idx, name in enumerate(self.cocktails)}

        # Initiale Speicherung in Hashtable
        self.hashtable.insert(self.cocktails)

    def update_popularity_scores(self, scores):
        self.popularity_scores.update(scores)
        self.sort_data()

    def update_prices(self, prices):
        self.prices.update(prices)
        self.sort_data()

    def add_cocktail(self, name, ingredients, notes, category="Other", popularity=5, price=10):
        self.cocktails[name] = {
            "Ingredients": ingredients,
            "Notes": notes,
            "Category": category
        }
        self.popularity_scores[name] = popularity
        self.prices[name] = price

        # HashTable aktualisieren - als Dictionary übergeben
        self.hashtable.insert({name: self.cocktails[name]})
        self.sort_data()

    def sort_data(self, criteria="Name", order="Aufsteigend"):
        keys = list(self.cocktails.keys())

        if criteria == "Name":
            self.quicksort.original_data = keys
            sorted_keys = self.quicksort.sort()
        else:
            # Key-Funktion für BubbleSort definieren
            if criteria == "Beliebtheit":
                key_func = lambda x: self.popularity_scores.get(x, 0)
            elif criteria == "Preis":
                key_func = lambda x: float(self.prices.get(x, 0))  # Sicherstellen, dass Preise als Zahlen verglichen werden
            elif criteria == "Zutatenanzahl":
                key_func = lambda x: len(self.cocktails[x]["Ingredients"])
            else:
                key_func = lambda x: x  # fallback

            # Temporäre Liste mit Keys und Sortierwerten erstellen
            temp_list = [(key, key_func(key)) for key in keys]
            
            # Manuelles Bubble Sort sortieren basierend auf den Werten, da es sonst ungangen wird 
            n = len(temp_list)
            for i in range(n):
                for j in range(0, n-i-1):
                    if temp_list[j][1] > temp_list[j+1][1]:
                        temp_list[j], temp_list[j+1] = temp_list[j+1], temp_list[j]
            
            sorted_keys = [item[0] for item in temp_list]

        if order == "Absteigend":
            sorted_keys = list(reversed(sorted_keys))

        self.sorted_cocktails = sorted_keys
        self.binarysearch.sorted_data = sorted_keys
        return sorted_keys

    def get_cocktail(self, name):
        return self.hashtable.get(name)  # O(1) Zugriff

    def get_all_cocktails(self):
        return {
            name: {
                **data,
                "Popularity": self.popularity_scores.get(name, 0),
                "Price": self.prices.get(name, 0)
            }
            for name, data in self.cocktails.items()
        }

    def search_cocktail(self, name):
        # Nutzt binary search auf sortierter Namensliste (nur bei Namenssortierung sinnvoll)
        index = self.binarysearch.search(name)
        if index != -1:
            result_name = self.sorted_cocktails[index]
            return self.get_cocktail(result_name)
        return None
