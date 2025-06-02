#Sortieralgorithmen

class QuickSort:
    def __init__(self, data):
        self.original_data = data.copy()
        self.sorted_data = None
    
    def sort(self):
        self.sorted_data = self._quicksort(self.original_data.copy())
        return self.sorted_data
    
    def _quicksort(self, arr):
        """Rekursive Quicksort-Implementierung"""
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2].lower()
        left = [x for x in arr if x.lower() < pivot]
        middle = [x for x in arr if x.lower() == pivot]
        right = [x for x in arr if x.lower() > pivot]
        return self._quicksort(left) + middle + self._quicksort(right)
    
    def get_original_data(self):
        return self.original_data
    
    def get_sorted_data(self):
        if self.sorted_data is None:
            raise ValueError("Daten wurden noch nicht sortiert")
        return self.sorted_data

class MergeSort:
    def __init__(self, data):
        self.original_data = data.copy()
        self.sorted_data = None
    
    def sort(self):

        self.sorted_data = self._merge_sort(self.original_data.copy())
        return self.sorted_data
    
    def _merge_sort(self, arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left, right):
        """Führt zwei sortierte Teillisten zusammen (case-insensitive)"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if str(left[i]).lower() <= str(right[j]).lower():
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def get_original_data(self):
        """Gibt die ursprünglichen Daten zurück"""
        return self.original_data
    
    def get_sorted_data(self):
        """Gibt die sortierten Daten zurück"""
        if self.sorted_data is None:
            raise ValueError("Daten wurden noch nicht sortiert")
        return self.sorted_data

class BubbleSort:
    def __init__(self, data):
        self.data = data.copy()  # Originaldaten bleiben unverändert
        self.sorted_data = None
    
    def sort(self):
        lst = self.data.copy()  # Arbeite auf einer Kopie der Daten
        unsorted_until_index = len(lst) - 1
        is_sorted = False
        
        while not is_sorted:
            is_sorted = True
            for i in range(unsorted_until_index):
                if lst[i] > lst[i + 1]:
                    # Elemente tauschen
                    lst[i], lst[i + 1] = lst[i + 1], lst[i]
                    is_sorted = False
            unsorted_until_index -= 1
        
        self.sorted_data = lst
        return self.sorted_data
    
    def get_original_data(self):
        """Gibt die ursprünglichen, unsortierten Daten zurück"""
        return self.data
    
    def get_sorted_data(self):
        """Gibt die sortierten Daten zurück"""
        if self.sorted_data is None:
            raise ValueError("Daten wurden noch nicht sortiert")
        return self.sorted_data

class InsertionSort:
    def __init__(self, data):
        self.original_data = data.copy()  # Originaldaten bleiben erhalten
        self.sorted_data = None
    
    def sort(self):
        """Führt den Insertion-Sort Algorithmus aus"""
        arr = self.original_data.copy()  # Arbeite auf einer Kopie
        
        for i in range(1, len(arr)):
            key = arr[i]  # Das einzufügende Element
            j = i - 1
            
            # Verschiebe Elemente des sortierten Teils, die größer als 'key' sind
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            
            # Füge 'key' an der korrekten Position ein
            arr[j + 1] = key
        
        self.sorted_data = arr
        return self.sorted_data
    
    def get_original_data(self):
        """Gibt die ursprünglichen Daten zurück"""
        return self.original_data
    
    def get_sorted_data(self):
        """Gibt die sortierten Daten zurück"""
        if self.sorted_data is None:
            raise ValueError("Daten wurden noch nicht sortiert")
        return self.sorted_data
    
    def get_max_value(self):
        """Gibt den größten Wert zurück (nach dem Sortieren)"""
        if self.sorted_data is None:
            self.sort()
        return self.sorted_data[-1] if len(self.sorted_data) > 0 else None


#Suchalgorithmus

class BinarySearch:
    def __init__(self, sorted_list):
        self.sorted_list = sorted_list
    
    def search(self, target):
        left = 0
        right = len(self.sorted_list) - 1

        while left <= right:
            mid = (left + right) // 2  # Mittleres Element finden
            if self.sorted_list[mid] == target:
                return mid  # Zielwert gefunden
            elif self.sorted_list[mid] < target:
                left = mid + 1  # Suche rechts fortsetzen
            else:
                right = mid - 1  # Suche links fortsetzen

        return -1  # Wert nicht gefunden


    
# Datenstruckturen 


#Hashtable 

#Queue (First in first aus )

# Stack (First in last out)

# linked list 

# duble linked list 