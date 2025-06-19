from abc import ABC, abstractmethod
from collections import deque
from typing import List, Any, Callable, Optional, Union, Dict, Tuple

class Algorithm(ABC):
    #Abstrakte Basisklasse für alle Algorithmen
    def __init__(self, data: List[Any]):
        self.original_data = data.copy()
        self.sorted_data: Optional[List[Any]] = None
        self.comparisons = 0
        self.swaps = 0
        self.execution_time = 0.0

    @abstractmethod
    def sort(self, reverse: bool = False, key: Optional[Callable] = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Any]:
        return {
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'time': self.execution_time
        }

    def reset_stats(self):
        self.comparisons = 0
        self.swaps = 0
        self.execution_time = 0.0

class QuickSort(Algorithm):
    def sort(self, reverse: bool = False, key: Optional[Callable] = None) -> List[Any]:
        import time
        start = time.time()
        
        self.reset_stats()
        self.sorted_data = self._quicksort(self.original_data.copy(), reverse, key)
        
        self.execution_time = time.time() - start
        return self.sorted_data
    
    def _quicksort(self, arr: List[Any], reverse: bool, key: Callable) -> List[Any]:
        if len(arr) <= 1:
            return arr
        
        # Median-of-Three Pivot Auswahl
        first, mid, last = arr[0], arr[len(arr)//2], arr[-1]
        pivot = sorted([first, mid, last], key=key)[1] if key else sorted([first, mid, last])[1]
        
        left = [x for x in arr if self._compare(x, pivot, reverse, key)]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if self._compare(pivot, x, reverse, key)]
        
        return self._quicksort(left, reverse, key) + middle + self._quicksort(right, reverse, key)
    
    def _compare(self, a: Any, b: Any, reverse: bool, key: Callable) -> bool:
        self.comparisons += 1
        a_val = key(a) if key else a
        b_val = key(b) if key else b
        
        if reverse:
            return a_val > b_val
        return a_val < b_val

class MergeSort(Algorithm):
    def sort(self, reverse: bool = False, key: Optional[Callable] = None) -> List[Any]:
        import time
        start = time.time()
        
        self.reset_stats()
        self.sorted_data = self._merge_sort(self.original_data.copy(), reverse, key)
        
        self.execution_time = time.time() - start
        return self.sorted_data
    
    def _merge_sort(self, arr: List[Any], reverse: bool, key: Callable) -> List[Any]:
        if len(arr) <= 1:
            return arr
            
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid], reverse, key)
        right = self._merge_sort(arr[mid:], reverse, key)
        
        return self._merge(left, right, reverse, key)
    
    def _merge(self, left: List[Any], right: List[Any], reverse: bool, key: Callable) -> List[Any]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            self.comparisons += 1
            left_val = key(left[i]) if key else left[i]
            right_val = key(right[j]) if key else right[j]
            
            if (not reverse and left_val <= right_val) or (reverse and left_val > right_val):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
                
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class BubbleSort(Algorithm):
    def sort(self, reverse: bool = False, key: Optional[Callable] = None) -> List[Any]:
        import time
        start = time.time()
        
        self.reset_stats()
        arr = self.original_data.copy()
        n = len(arr)
        
        for i in range(n):
            swapped = False
            for j in range(0, n-i-1):
                self.comparisons += 1
                a_val = key(arr[j]) if key else arr[j]
                b_val = key(arr[j+1]) if key else arr[j+1]
                
                if (not reverse and a_val > b_val) or (reverse and a_val < b_val):
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    self.swaps += 1
                    swapped = True
            
            if not swapped:
                break
                
        self.execution_time = time.time() - start
        self.sorted_data = arr
        return self.sorted_data

class InsertionSort(Algorithm):
    def sort(self, reverse: bool = False, key: Optional[Callable] = None) -> List[Any]:
        import time
        start = time.time()
        
        self.reset_stats()
        arr = self.original_data.copy()
        
        for i in range(1, len(arr)):
            key_item = arr[i]
            j = i - 1
            
            # Finde die Einfügeposition mit binary search
            pos = self._binary_search(arr, key_item, 0, j, reverse, key)
            
            while j >= pos:
                self.comparisons += 1
                arr[j + 1] = arr[j]
                self.swaps += 1
                j -= 1
                
            arr[j + 1] = key_item
            
        self.execution_time = time.time() - start
        self.sorted_data = arr
        return self.sorted_data
    
    def _binary_search(self, arr: List[Any], item: Any, low: int, high: int, 
                      reverse: bool, key: Callable) -> int:
        while low <= high:
            mid = (low + high) // 2
            mid_val = key(arr[mid]) if key else arr[mid]
            item_val = key(item) if key else item
            
            self.comparisons += 1
            if (not reverse and mid_val < item_val) or (reverse and mid_val > item_val):
                low = mid + 1
            else:
                high = mid - 1
        return low

class SearchAlgorithm(ABC):
    #Abstrakte Basisklasse für Suchalgorithmen
    def __init__(self, data: List[Any]):
        self.data = data
    
    @abstractmethod
    def search(self, target: Any) -> Union[int, None]:
        pass

class BinarySearch(SearchAlgorithm):
    def search(self, target: Any, key: Optional[Callable] = None) -> Union[int, None]:
        low = 0
        high = len(self.data) - 1
        
        while low <= high:
            mid = (low + high) // 2
            mid_val = key(self.data[mid]) if key else self.data[mid]
            target_val = key(target) if key else target
            
            if mid_val == target_val:
                return mid
            elif mid_val < target_val:
                low = mid + 1
            else:
                high = mid - 1
                
        return None

class HashTable:
    def __init__(self, size: int = 16, max_load_factor: float = 0.75):
        self.size = size
        self.max_load_factor = max_load_factor
        self.table = [[] for _ in range(size)]
        self.count = 0
    
    def _hash(self, key: Any) -> int:
        return hash(key) % self.size
    
    def _resize(self):
        new_size = self.size * 2
        new_table = [[] for _ in range(new_size)]
        
        for bucket in self.table:
            for key, value in bucket:
                new_index = hash(key) % new_size
                new_table[new_index].append([key, value])
                
        self.table = new_table
        self.size = new_size
    
    def insert(self, data: Dict[Any, Any]):
        for key, value in data.items():
            if self.count / self.size > self.max_load_factor:
                self._resize()
                
            index = self._hash(key)
            for pair in self.table[index]:
                if pair[0] == key:
                    pair[1] = value
                    break
            else:
                self.table[index].append([key, value])
                self.count += 1
    
    def get(self, key: Any) -> Any:
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        raise KeyError(f"Key '{key}' not found")
    
    def delete(self, key: Any) -> bool:
        index = self._hash(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                self.count -= 1
                return True
        return False

class CocktailQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, name, ingredients, notes, category):
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
        if self.queue:
            return self.queue[0]
        return None  # Gibt `None` zurück, wenn die Queue leer ist

    def get_queue(self):
        return list(self.queue)

cocktail_q = CocktailQueue()

# Stack (First in last out)

# linked list 

# duble linked list 
    


    #Stack

    #Linked List 

    # Dobble Linket List 