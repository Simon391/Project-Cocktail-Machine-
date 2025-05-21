class ZutatenSorter:
    """ Klasse zum Sortieren von Zutaten mit Bubble Sort """
    def __init__(self, zutaten):
        self.zutaten = zutaten

    def bubble_sort(self):
        """ Sortiert die Zutaten alphabetisch """
        n = len(self.zutaten)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.zutaten[j] > self.zutaten[j + 1]:
                    self.zutaten[j], self.zutaten[j + 1] = self.zutaten[j+1], self.zutaten[j]
        return self.zutaten


class CocktailSorter:
    """ Klasse zum Sortieren der Cocktails nach Name, Kategorie oder Preis mit Quick Sort """
    def __init__(self, cocktails):
        self.cocktails = cocktails

    def quick_sort(self, key):
        """ Sortiert Cocktails nach einem gegebenen Schlüssel (name, kategorie oder preis) """
        def sort(arr):
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x[key] < pivot[key]]
            middle = [x for x in arr if x[key] == pivot[key]]
            right = [x for x in arr if x[key] > pivot[key]]
            return sort(left) + middle + sort(right)

        self.cocktails = sort(self.cocktails)
        return self.cocktails


class CocktailSearcher:
    """ Klasse zum schnellen Finden von Rezepten mit Binärer Suche """
    def __init__(self, cocktails):
        self.cocktails = sorted(cocktails, key=lambda x: x["name"])  # Sortieren nach Namen

    def binary_search(self, target_name):
        """ Findet ein Rezept anhand des Namens mit Binärer Suche """
        left, right = 0, len(self.cocktails) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.cocktails[mid]["name"].lower() == target_name.lower():
                return self.cocktails[mid]
            elif self.cocktails[mid]["name"].lower() < target_name.lower():
                left = mid + 1
            else:
                right = mid - 1
        return None


class IngredientCocktailSearcher:
    """ Sucht Cocktails basierend auf einer bestimmten Zutat """
    
    def __init__(self, cocktails):
        self.cocktails = cocktails

    def search_by_ingredient(self, ingredient):
        """ Findet alle Cocktails, die eine bestimmte Zutat enthalten """
        matching_cocktails = [c for c in self.cocktails if ingredient.lower() in (z.lower() for z in c["zutaten"])]

        if matching_cocktails:
            return matching_cocktails
        else:
            return 


class ZutatenManager:
    """ Verwaltet die Mengen der verfügbaren Zutaten """
    
    def __init__(self, zutaten_mengen):
        self.zutaten_mengen = zutaten_mengen  # Dictionary mit Zutaten und ihren Mengen

    def check_ingredient(self, ingredient):
        """ Prüft, ob eine Zutat verfügbar ist """
        return self.zutaten_mengen.get(ingredient, 0) > 0
    
    def anzeigen_bestand(self):
        """ Zeigt die aktuelle Menge aller Zutaten, sortiert nach kleinster Menge zuerst """
        sortierter_bestand = sorted(self.zutaten_mengen.items(), key=lambda x: x[1])  # Sortieren nach Menge

        print("\n📦 Zutatenbestand (aufsteigend nach Menge sortiert):")
        for zutat, menge in sortierter_bestand:
         print(f"{zutat}: {menge} Einheiten")


    def use_ingredient(self, ingredient):
        """ Verwendet eine Zutat und reduziert ihre Menge """
        if self.check_ingredient(ingredient):
            self.zutaten_mengen[ingredient] -= 1
            return True
        return False
    
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
            print("\n📊 Noch keine Cocktails zubereitet.")
            return
        
        top_cocktails = sorted(self.statistik.items(), key=lambda x: x[1], reverse=True)[:3]
        
        print("\n🏆 Top 3 meist gemixte Cocktails:")
        for name, anzahl in top_cocktails:
            print(f"{name}: {anzahl} Mal zubereitet")

class ZutatenAlternative:
    """ Bietet Alternativen für fehlende Zutaten """
    
    def __init__(self):
        self.alternativen = {
            "Rum": ["Brandy", "Whiskey"],
            "Gin": ["Wodka", "Tequila"],
            "Zitrone": ["Limette", "Orange"],
            "Grenadine": ["Himbeersirup", "Erdbeersirup"],
            "Honig": ["Ahornsirup", "Zucker"],
            "Tonic Water": ["Soda", "Ginger Beer"],
            "Minze": ["Basilikum", "Rosmarin"]
        }

    def get_alternative(self, zutat):
        """ Gibt eine Alternative für eine fehlende Zutat zurück """
        return self.alternativen.get(zutat, [])








