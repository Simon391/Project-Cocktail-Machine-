#Sortieralgorithmen
# sorting_algorithms.py
class QuickSort:
    def __init__(self, data):
        self.original_data = data.copy()
        self.sorted_data = None
    
    def sort(self):
        self.sorted_data = self._quicksort(self.original_data.copy())
        return self.sorted_data
    
    def _quicksort(self, arr):
        # Rekursive QuickSort Implementierung
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2].lower()
        left = [x for x in arr if x.lower() < pivot]
        middle = [x for x in arr if x.lower() == pivot]
        right = [x for x in arr if x.lower() > pivot]
        return self._quicksort(left) + middle + self._quicksort(right)

class BubbleSort:
    def __init__(self, data):
        self.data = data

    def sort(self, key=lambda x: x, reverse=False):
        data = self.data[:]
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if (key(data[j]) > key(data[j + 1])) ^ reverse:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data


class BinarySearch:
    def __init__(self, sorted_list):
        self.sorted_list = sorted_list
    
    def search(self, target):
        # Binäre Suche auf sortierter Liste
        left = 0
        right = len(self.sorted_list) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.sorted_list[mid] == target:
                return mid
            elif self.sorted_list[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

class HashTable:
    def __init__(self, size=20):  # Standardgröße von 20
        """Erstellt eine Hashtabelle mit einer festen Größe"""
        self.size = size
        self.table = [[] for _ in range(size)]  # Kollisionslösung durch Verkettung

    def _hash(self, key):
        """Erzeugt einen Hash-Wert für einen gegebenen Schlüssel"""
        return hash(key) % self.size

    def insert(self, data):
        """
        Fügt ein oder mehrere Cocktails in die Hashtabelle ein.
        Akzeptiert:
        - dict mit mehreren Cocktails
        - einzelner Cocktail mit Schlüssel und Daten
        """
        if isinstance(data, dict):
            # Mehrere Cocktails einfügen
            for key, value in data.items():
                self._insert_single(key, value)
        else:
            raise ValueError("Insert erwartet ein Dictionary von Cocktails")

    def _insert_single(self, key, value):
        """Hilfsfunktion zum Einfügen eines einzelnen Cocktails"""
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value  # Überschreibt bestehenden Eintrag
                return
        self.table[index].append([key, value])  # Neuen Cocktail hinzufügen

    def get(self, key):
        """Gibt die Informationen zu einem Cocktail zurück"""
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return "Cocktail nicht gefunden"

    def remove(self, key):
        """Löscht einen Cocktail aus der Hashtabelle"""
        index = self._hash(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                return
        return "Cocktail nicht gefunden"

#Queue (First in first aus )

from collections import deque

class CocktailQueue:
    def __init__(self):

        self.queue = deque()

    def enqueue(self, name, ingredients, notes, category):
        #Fügt einen Cocktail am Ende der Warteschlange hinzu
        self.queue.append({
            "Name": name,
            "Ingredients": ingredients,
            "Notes": notes,
            "Category": category
        })

    def dequeue(self):

        if self.queue:
            return self.queue.popleft()
        return None  # Gibt `None` zurück, wenn die Queue leer ist

    def peek(self):
        #Zeigt den nächsten Cocktail, ohne ihn zu entfernen
        if self.queue:
            return self.queue[0]
        return None  # Gibt `None` zurück, wenn die Queue leer ist

    def get_queue(self):
        #Gibt die gesamte Warteschlange als Liste zurück
        return list(self.queue)

# Stack (First in last out)

# linked list 

# duble linked list 
    


    #Stack

    #Linked List 

    # Dobble Linket List 