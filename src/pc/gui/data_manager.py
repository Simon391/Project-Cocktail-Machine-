from sorting_algorithms import QuickSort,BubbleSort


class CocktailDataManager:
    def __init__(self):
        self.cocktails = {}
        self.popularity_scores = {}
        self.prices = {}
        self.sorted_cocktails = []
        self.quicksort =  QuickSort([])
        self.bubbelsort = BubbleSort ([])
        self.load_sample_data()
        self.sort_data()

    def load_sample_data(self):
        """Load sample cocktail data with popularity scores and prices"""
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
    

        self.popularity_scores = {cocktail: 7 + index % 3 for index, cocktail in enumerate(self.cocktails.keys())}
        self.prices = {cocktail: 8 + index % 5 for index, cocktail in enumerate(self.cocktails.keys())}


    def update_popularity_scores(self, scores):
        """Update popularity scores"""
        self.popularity_scores.update(scores)
        self.sort_data ()

    def update_prices(self, prices):
        """Update prices"""
        self.prices.update(prices)
        self.sort_data()

    def add_cocktail(self, name, ingredients, notes, category="Other", popularity=5, price=10):
        """Add new cocktail"""
        self.cocktails[name] = {
            "Ingredients": ingredients,
            "Notes": notes,
            "Category": category
        }
        self.popularity_scores[name] = popularity
        self.prices[name] = price
        self.sort_data()

    def sort_data(self, criteria="Name", order="Aufsteigend"):
        """Sort data by different criteria"""
        if criteria == "Name":
            self.quicksort.original_data = list(self.cocktails.keys())
            sorted_data = self.quicksort.sort()
        elif criteria == "Beliebtheit":
            sorted_data = sorted(
                self.cocktails.keys(),
                key=lambda x: self.popularity_scores.get(x, 0),
                reverse=True
            )
        elif criteria == "Preis":
            sorted_data = sorted(
                self.cocktails.keys(),
                key=lambda x: self.prices.get(x, 0)
            )
        elif criteria == "Zutatenanzahl":
            sorted_data = sorted(
                self.cocktails.keys(),
                key=lambda x: len(self.cocktails[x]["Ingredients"])
            )
        
        if order == "Absteigend":
            sorted_data = sorted_data[::-1]
        
        self.sorted_cocktails = sorted_data
        return sorted_data

    def get_cocktail(self, name):
        """Get specific cocktail"""
        return self.cocktails.get(name)

    def get_all_cocktails(self):
        """Get all cocktails"""
        return {
            name: {
                **data,
                "Popularity": self.popularity_scores.get(name, 0),
                "Price": self.prices.get(name, 0)
            }
            for name, data in self.cocktails.items()
        }
    