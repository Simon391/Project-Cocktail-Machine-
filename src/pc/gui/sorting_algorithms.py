def quicksort(arr):
    """Case-insensitive quicksort implementation"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2].lower()
    left = [x for x in arr if x.lower() < pivot]
    middle = [x for x in arr if x.lower() == pivot]
    right = [x for x in arr if x.lower() > pivot]
    return quicksort(left) + middle + quicksort(right)

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
                if self.zutaten[j] > self.zutaten[j + 1]:
                    self.zutaten[j], self.zutaten[j + 1] = self.zutaten[j+1], self.zutaten[j]
        return self.zutaten

