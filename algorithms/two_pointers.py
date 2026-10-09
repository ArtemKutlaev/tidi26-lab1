def two_pointers_search(arr_a: list, arr_b: list) -> bool:
    """
    Проверяет наличие хотя бы одного общего элемента в двух отсортированных массивах
    с помощью метода двух указателей.
    Args:
        arr_a (list): Первый отсортированный по неубыванию массив целых чисел.
        arr_b (list): Второй отсортированный по неубыванию массив целых чисел.

    Returns:
        bool: True, если найден хотя бы один общий элемент, иначе False.
    """
    i, j = 0, 0
    len_a = len(arr_a)
    len_b = len(arr_b)

    while i < len_a and j < len_b:
        if arr_a[i] == arr_b[j]:
            return True
        elif arr_a[i] < arr_b[j]:
            i += 1
        else:
            j += 1
    return False