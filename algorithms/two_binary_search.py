def binary_search_split(arr: list, left: int, right: int, target: int):
    """
    Бинарный поиск.
    Возвращает (True, индекс), если target найден.
    Иначе возвращает (False, индекс_вставки).
    """
    low, high = left, right
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return (True, mid)
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return (False, low)


def dual_binary_search(
    a: list, a_left: int, a_right: int,
    b: list, b_left: int, b_right: int
) -> bool:
    if a_left > a_right or b_left > b_right:
        return False
    len_a = a_right - a_left + 1
    len_b = b_right - b_left + 1
    if len_a > len_b:
        return dual_binary_search(b, b_left, b_right, a, a_left, a_right)
    
    mid_a = (a_left + a_right) // 2
    pivot = a[mid_a]
    found, split_b = binary_search_split(b, b_left, b_right, pivot)
    if found:
        return True

    if dual_binary_search(a, a_left, mid_a - 1, b, b_left, split_b - 1):
        return True

    return dual_binary_search(a, mid_a + 1, a_right, b, split_b, b_right)


def has_common_element(a: list, b: list) -> bool:
    """Точка входа"""
    if not a or not b:
        return False
    return dual_binary_search(a, 0, len(a) - 1, b, 0, len(b) - 1)