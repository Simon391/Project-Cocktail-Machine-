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