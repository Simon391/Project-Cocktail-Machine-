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
            "Margarita": {
                "Ingredients": {"Tequila": "50", "Triple Sec": "20", "Lime Juice": "30", "Salt Rim": "--"},
                "Notes": "Rim glass with salt",
                "Category": "Classic"
            },
            "Mojito": {
                "Ingredients": {"Rum": "50", "Mint": "5", "Lime": "1", "Soda": "100"},
                "Notes": "Garnish with mint and lime",
                "Category": "Classic"
            },
            "Cosmopolitan": {
                "Ingredients": {"Vodka": "40", "Triple Sec": "15", "Cranberry Juice": "30", "Lime Juice": "15"},
                "Notes": "Serve in a chilled martini glass",
                "Category": "Modern"
            }
        }

        self.popularity_scores = {
            "Margarita": 8,
            "Mojito": 9,
            "Cosmopolitan": 7
        }

        self.prices = {
            "Margarita": 12,
            "Mojito": 10,
            "Cosmopolitan": 14
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