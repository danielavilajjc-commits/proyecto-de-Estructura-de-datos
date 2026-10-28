def merge_sort(arr):
    """
    Ordenamiento Merge Sort implementado desde cero.
    Garantiza O(n log n) en todos los casos.
    """
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
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Agregar el resto de los elementos
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result

def binary_search_next(arr, target):
    """
    Busca el primer elemento en la lista ordenada que sea mayor o igual al objetivo.
    O(log n).
    """
    low = 0
    high = len(arr) - 1
    res = None

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] >= target:
            res = arr[mid]
            high = mid - 1
        else:
            low = mid + 1
    return res
