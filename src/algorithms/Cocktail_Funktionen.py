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


# 🎤 Interaktive Suche mit manueller Sortierung, Zutaten-Suche & Cocktail-Zubereitung
print("\nWillkommen in der Cocktail-Welt! 🍹")
while True:
    suche = input("Wonach suchst du oder möchtest du was tun? (Cocktail-Name, Kategorie, Preisbereich, Zutat, " \
    "'bestand', 'sortieren', 'top', 'zubereiten','zufall','party','custom' oder 'exit' zum Beenden): ").strip().lower()

    # 🔄 Manuelle Sortierung starten
    if suche == "sortieren":
        sortierung = input("\nWie möchtest du die Cocktails sortieren? (name, kategorie, preis oder 'exit' zum Beenden): ").strip().lower()
        
        if sortierung == "exit":
            print("Bis zum nächsten Cocktail-Abenteuer! 🍸")
            break
        elif sortierung in ["name", "kategorie", "preis"]:
            print(f"\n🔄 Cocktails nach {sortierung} sortiert:")
            for c in cocktail_sorter.quick_sort(sortierung):
                print(f"{c['name']} - {c['kategorie']} ({c['preis']}€)")
        else:
            print("❌ Ungültige Eingabe. Bitte wähle 'name', 'kategorie' oder 'preis'.")
        continue  # Gehe zurück zur Hauptschleife



    # 🥤 Cocktails zubereiten
    if suche == "zubereiten":
        cocktail_wunsch = input("\nWelchen Cocktail möchtest du zubereiten? ").strip().lower()
        gefundenes_cocktail = cocktail_searcher.binary_search(cocktail_wunsch)

        if gefundenes_cocktail:
            verfügbar, fehlende_zutat = can_make_cocktail(gefundenes_cocktail)
            if verfügbar:
                for zutat in gefundenes_cocktail["zutaten"]:
                    zutaten_manager.use_ingredient(zutat)
                print(f"✅ {cocktail_wunsch} wurde erfolgreich zubereitet!")
            else:
                print(f"❌ {cocktail_wunsch} kann nicht zubereitet werden. '{fehlende_zutat}' ist nicht mehr verfügbar.")
        else:
            print(f"❌ Kein Cocktail namens '{cocktail_wunsch}' gefunden.")
        continue  # Gehe zurück zur Hauptschleife


    # Liste zustaten bestand anzeigen wie viel noch übrig
    if suche == "bestand":
        zutaten_manager.anzeigen_bestand()
        continue  # Zurück zur Hauptschleife

    # 🔎 Suche nach einer einzelnen Zutat
    zutaten_treffer = ingredient_searcher.search_by_ingredient(suche)
    if isinstance(zutaten_treffer, list):
        print(f"\n🍹 Cocktails mit '{suche}':")
        for c in zutaten_treffer:
            print(f"- {c['name']} ({c['preis']}€)")
        continue
    elif isinstance(zutaten_treffer, dict):
        print(zutaten_treffer["message"])

    # 🔍 Suche nach Cocktail-Namen
    gefundenes_rezept = cocktail_searcher.binary_search(suche)
    if gefundenes_rezept:
        print(f"🎉 Rezept gefunden: {gefundenes_rezept}")
        continue

    # 🍹 Suche nach Kategorie
    kategorien_treffer = [c for c in cocktails if c["kategorie"].lower() == suche.lower()]
    if kategorien_treffer:
        print(f"🍹 Rezepte in der Kategorie '{suche}':")
        for c in kategorien_treffer:
            print(f"- {c['name']} ({c['preis']}€)")
        continue
    if suche == "top":
        cocktail_statistik.anzeigen_top_cocktails()
        continue  # Zurück zur Hauptschleife

    if suche == "zufall":
        zufalls_cocktail()
        continue  # Zurück zur Hauptschleife


    if suche == "exit":
        print("Bis zum nächsten Cocktail-Abenteuer! 🍸")
        break

    if suche == "party":
        try:
            anzahl = int(input("\nWie viele Gäste hast du? "))
            party_modus(anzahl)
        except ValueError:
            print("❌ Bitte eine gültige Anzahl eingeben.")
        continue  # Zurück zur Hauptschleife
    
    # 💰 Suche nach einem Preisbereich
    try:
        preis_limit = float(suche)
        preis_treffer = [c for c in cocktails if c["preis"] <= preis_limit]
        if preis_treffer:
            print(f"💰 Cocktails unter {preis_limit}€:")
            for c in preis_treffer:
                print(f"- {c['name']} ({c['preis']}€)")
            continue
    except ValueError:
        pass  # Falls die Eingabe keine Zahl ist

        print(f"❌ Keine passenden Cocktails für '{suche}' gefunden.")