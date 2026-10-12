def binary_search(arr: list, target: int, left: int, right: int) -> int:
    """Выполняет локальный бинарный поиск целевого значения в заданном диапазоне.
    Ищет элемент target в срезе индексов [left, right] без создания копий массива.
    Если элемент найден, возвращает его индекс.
    Если элемент отсутствует, возвращает индекс первого элемента, который строго
    больше target(позиция вставки).
    Args:
        arr (list): Отсортированный по неубыванию массив целых чисел.
        target (int): Искомое значение.
        left (int): Левая граница диапазона поиска (включительно).
        right (int): Правая граница диапазона поиска (включительно).

    Returns:
        int: Индекс найденного элемента или индекс позиции вставки.
    """
    while left <= right:
        mid = (left + right) // 2
        mid_val = arr[mid]

        if mid_val == target:
            return mid
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return left


def exp_search(arr_a: list, arr_b: list) -> bool:
    """Проверяет наличие пересечения двух отсортированных массивов экспоненциальным поиском.
    Args:
        arr_a (list): Первый отсортированный по неубыванию массив.
        arr_b (list): Второй отсортированный по неубыванию массив.

    Returns:
        bool: True, если найден хотя бы один общий элемент, иначе False.
    """
    if not arr_a or not arr_b:
        return False

    if len(arr_a) > len(arr_b):
        min_arr, max_arr = arr_b, arr_a
    else:
        min_arr, max_arr = arr_a, arr_b

    n = len(max_arr)
    m = len(min_arr)

    j = 0

    for i in range(m):
        target = min_arr[i]
        if j >= n:
            break

        step = 1
        while j + step < n and max_arr[j + step] < target:
            step *= 2

        left = j
        right = min(j + step, n - 1)

        idx = binary_search(max_arr, target, left, right)

        if idx < n and max_arr[idx] == target:
            return True

        j = idx

    return False