class quicksort:
    @classmethod
    def quicksort(arr):
        """Case-insensitive quicksort implementation"""
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2].lower()
        left = [x for x in arr if x.lower() < pivot]
        middle = [x for x in arr if x.lower() == pivot]
        right = [x for x in arr if x.lower() > pivot]
        return quicksort(left) + middle + quicksort(right)

class merge_sort:
    @classmethod
    def merge_sort(arr):
        """Case-insensitive merge sort implementation"""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        
        return merge(left, right)

    def merge(left, right):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i].lower() <= right[j].lower():
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class Bubble_Sort:
    def __init__(self, zutaten):
        self.zutaten = zutaten

    def bubble_sort(self):
        n = len(self.zutaten)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.zutaten[j].lower() > self.zutaten[j + 1].lower():
                    self.zutaten[j], self.zutaten[j + 1] = self.zutaten[j+1], self.zutaten[j]

class IngredientCocktailSearcher:
    """ Sucht Cocktails basierend auf mehreren Zutaten """

    def __init__(self, cocktails):
        self.cocktails = cocktails

    def search_by_ingredients(self, zutaten_liste):
        """ Findet alle Cocktails, die ALLE angegebenen Zutaten enthalten """
        matching_cocktails = [
            c for c in self.cocktails if all(z.lower() in [zut.lower() for zut in c["zutaten"]] for z in zutaten_liste)
        ]

        return matching_cocktails if matching_cocktails else False
    

class CocktailStatistik:
    """ Verfolgt die Nutzungshäufigkeit von Cocktails und zeigt die Top 3 an """
    
    def __init__(self):
        self.statistik = {}  # Speichert die Anzahl der Zubereitungen pro Cocktail

    def update_statistik(self, cocktail_name):
        """ Aktualisiert die Nutzungshäufigkeit eines Cocktails """
        if cocktail_name in self.statistik:
            self.statistik[cocktail_name] += 1
        else:
            self.statistik[cocktail_name] = 1

    def anzeigen_top_cocktails(self):
        """ Zeigt die Top 3 am häufigsten zubereiteten Cocktails an """
        if not self.statistik:
            
            return False # noch keine Cocktails zubereitet für die Statistik
        
        top_cocktails = sorted(self.statistik.items(), key=lambda x: x[1], reverse=True)[:3]
        
        
        for name, anzahl in top_cocktails:
            return name, anzahl

class ZutatenAlternative:
    """ Bietet Alternativen für fehlende Zutaten """
    
    def __init__(self):
        self.alternativen = {
            "Rum": ["Brandy", "Whiskey"],
            "Zitrone": ["Limette", "Orange"],
            "Tonic Water": ["Leitungswasser"],
            "Mint": ["Basilikum", "Rosmarin"]
        }

    def get_alternative(self, zutat):
        """ Gibt eine Alternative für eine fehlende Zutat zurück """
        return self.alternativen.get(zutat, [])