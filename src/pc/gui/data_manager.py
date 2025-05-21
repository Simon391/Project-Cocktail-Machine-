from sorting_algorithms import quicksort, merge_sort

class CocktailDataManager:
    def __init__(self):
        self.cocktails = {}
        self.popularity_scores = {}
        self.prices = {}
        self.sorted_cocktails = []
        self.current_sort_method = quicksort
        self.load_sample_data()
        self.sort_data()

    def load_sample_data(self):
        """Load sample cocktail data with popularity scores and prices"""
        self.cocktails = {
            "Rum & Cola Classic": {
                "Ingredients": {"Rum": "50", "Cola": "100", "Lime Juice": "10", "Ice": "--"},
                "Notes": "Mit Limettenscheibe garnieren",
                "Category": "Classic"
            },
            "Vodka Tonic Breeze": {
                "Ingredients": {"Vodka": "40", "Tonic Water": "100", "Lime": "1", "Ice": "--"},
                "Notes": "Eiswürfel hinzufügen und gut umrühren",
                "Category": "Modern"
            },
            "Fusion Fizz": {
                "Ingredients": {"Rum": "30", "Vodka": "30", "Cola": "80", "Tonic Water": "20"},
                "Notes": "Mit Minzblatt garnieren",
                "Category": "Creative"
            }
        }

        self.popularity_scores = {
            "Rum & Cola Classic": 9,
            "Vodka Tonic Breeze": 8,
            "Fusion Fizz": 7
        }

        self.prices = {
            "Rum & Cola Classic": 10,
            "Vodka Tonic Breeze": 12,
            "Fusion Fizz": 11
        }


    def update_popularity_scores(self, scores):
        """Update popularity scores"""
        self.popularity_scores.update(scores)
        self.sort_data()

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
            sorted_data = self.current_sort_method(list(self.cocktails.keys()))
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