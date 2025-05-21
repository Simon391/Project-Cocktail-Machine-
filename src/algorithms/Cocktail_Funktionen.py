# Importieren der Algorithmen

from Cocktail_Algorithmen import ZutatenSorter
from Cocktail_Algorithmen import CocktailSorter
from Cocktail_Algorithmen import CocktailSearcher
from Cocktail_Algorithmen import IngredientCocktailSearcher
from Cocktail_Algorithmen import ZutatenManager
from Cocktail_Algorithmen import CocktailStatistik
from Cocktail_Algorithmen import ZutatenAlternative
from custom_cocktail_manager import CustomCocktailManager

# Importieren der Datenbank

from Cocktail_Datenbank import cocktails
from Cocktail_Datenbank import zutaten_mengen

zutaten_manager = ZutatenManager(zutaten_mengen)
zutaten_sorter = ZutatenSorter(list(zutaten_mengen.keys()))
cocktail_sorter = CocktailSorter(cocktails)
cocktail_searcher = CocktailSearcher(cocktails)
ingredient_searcher = IngredientCocktailSearcher(cocktails)
cocktail_statistik = CocktailStatistik()
zutaten_alternative = ZutatenAlternative()
custom_manager = CustomCocktailManager()





# 🍹 Funktion zur Cocktail-Zubereitung
def can_make_cocktail(cocktail):
    """ Prüft, ob alle Zutaten verfügbar sind oder Alternativen vorgeschlagen werden, aber mixt nur bei Originalzutaten """
    fehlende_zutaten = []
    alternative_gefunden = False  # Neue Variable zur Überprüfung, ob eine Alternative vorgeschlagen wurde
    
    for zutat in cocktail["zutaten"]:
        if not zutaten_manager.check_ingredient(zutat):
            alternative = zutaten_alternative.get_alternative(zutat)
            if alternative:
                print(f"⚠️ '{zutat}' fehlt, aber du kannst {alternative[0]} verwenden.")
                alternative_gefunden = True  # Setze Alternative-Flag auf True
            else:
                fehlende_zutaten.append(zutat)

    # Nur wenn KEINE Zutat fehlt UND keine Alternative benötigt wurde, darf gemixt werden
    return len(fehlende_zutaten) == 0 and not alternative_gefunden, fehlende_zutaten


# 🫢 Funktion Zufall Cocktail
import random

def zufalls_cocktail():
    """ Wählt zufällig einen Cocktail aus, aber nur, wenn alle Zutaten verfügbar sind """
    verfügbare_cocktails = [c for c in cocktails if can_make_cocktail(c)[0] == True]  # Sicherstellen, dass nur True überprüft wird

    if verfügbare_cocktails:
        gewählter_cocktail = random.choice(verfügbare_cocktails)  # Zufällige Auswahl
        print(f"\n🎲 Zufälliger Cocktail: {gewählter_cocktail['name']} ({gewählter_cocktail['preis']}€)")
    else:
        print("\n❌ Kein Cocktail kann aktuell zubereitet werden, es fehlen Zutaten.")


# 🎉 Funktion Party-Modus

import random

def party_modus(anzahl_gaeste):
    """ Erstellt eine zufällige Cocktail-Kombination basierend auf der Gästeanzahl und verfügbaren Zutaten """
    verfügbare_cocktails = [c for c in cocktails if can_make_cocktail(c)[0]]

    if not verfügbare_cocktails:
        print("\n❌ Leider sind keine Cocktails verfügbar, es fehlen Zutaten.")
        return

    print(f"\n🎉 Party-Modus aktiviert! Zufällige Getränkeempfehlung für {anzahl_gaeste} Gäste:")

    random.shuffle(verfügbare_cocktails)  # Zufällige Reihenfolge der verfügbaren Cocktails
    
    vorgeschlagene_cocktails = []
    verbleibende_gaeste = anzahl_gaeste

    for cocktail in verfügbare_cocktails:
        if verbleibende_gaeste <= 0:
            break
        portionen = random.randint(1, min(verbleibende_gaeste, min([zutaten_manager.zutaten_mengen[z] // 1 for z in cocktail["zutaten"]])))
        vorgeschlagene_cocktails.append((cocktail["name"], portionen))
        verbleibende_gaeste -= portionen  

    if vorgeschlagene_cocktails:
        for name, portionen in vorgeschlagene_cocktails:
            print(f"✅ {portionen}x {name}")
    else:
        print("⚠️ Nicht genügend Zutaten für die gesamte Gruppe – vielleicht auffüllen oder wieder nach Hause gehen")


