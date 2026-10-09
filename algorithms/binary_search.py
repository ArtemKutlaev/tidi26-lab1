def binary_search(arr: list, target: int) -> bool:
    """Классический бинарный поиск(вспомогательная функция)"""
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_val = arr[mid]

        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


def binary_search_intersection(arr_a: list, arr_b: list) -> bool:
    """Проверяет пересечение двух отсортированных массивов через бинарный поиск.

    Args:
        arr_a (list): Первый отсортированный массив.
        arr_b (list): Второй отсортированный массив.

    Returns:
        bool: True, если есть хотя бы один общий элемент, иначе False.
    """
    if len(arr_a) > len(arr_b):
        min_arr, max_arr = arr_b, arr_a
    else:
        min_arr, max_arr = arr_a, arr_b

    for elem in min_arr:
        if binary_search(max_arr, elem):
            return True

    return False