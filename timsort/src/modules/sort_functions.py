def insertin_sort(arr: list):
    for i in range(len(arr)):
        j = i
        while j > 0 and arr[j - 1] > arr[j]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1

def quicksort(arr: list) -> list:
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    less = [i for i in arr if i < pivot]
    equal = [i for i in arr if i == pivot]
    greater = [i for i in arr if i > pivot]

    return quicksort(less) + equal + quicksort(greater)

def merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    # Сравниваем элементы из левой и правой частей и добавляем меньший в результат
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result

def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)