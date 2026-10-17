import csv
from pathlib import Path
from statistics import median
from time import perf_counter

from algorithms.binary_search import binary_search_intersection
from algorithms.exponential_search import exp_search
from algorithms.two_binary_search import has_common_element
from algorithms.two_pointers import two_pointers_search


DATA_DIR = Path("data")
CSV_FILE = DATA_DIR / "results.csv"
REPEATS = 7

ALGORITHMS = {
    "two_pointers": two_pointers_search,
    "binary_search": binary_search_intersection,
    "exponential_search": exp_search,
    "double_binary_search": has_common_element,
}

SCENARIOS = [
    # 1. Массивы одинакового размера
    ("equal_sizes", 100, 100),
    ("equal_sizes", 1_000, 1_000),
    ("equal_sizes", 5_000, 5_000),
    ("equal_sizes", 10_000, 10_000),
    ("equal_sizes", 50_000, 50_000),
    ("equal_sizes", 100_000, 100_000),
    ("equal_sizes", 300_000, 300_000),

    # 2. Маленький массив и большой массив
    ("fixed_m", 50, 500),
    ("fixed_m", 50, 2_000),
    ("fixed_m", 50, 10_000),
    ("fixed_m", 50, 50_000),
    ("fixed_m", 50, 200_000),
    ("fixed_m", 50, 1_000_000),

    # 3. Изменение отношения N / M
    ("varying_ratio", 100, 100),
    ("varying_ratio", 100, 500),
    ("varying_ratio", 100, 2_000),
    ("varying_ratio", 100, 10_000),
    ("varying_ratio", 100, 50_000),
    ("varying_ratio", 100, 200_000),
]


def generate_arrays(m: int, n: int) -> tuple[list[int], list[int]]:
    """Создаёт два отсортированных массива без общих элементов.

    Числа в первом массиве нечётные, во втором — чётные.
    Элементы первого массива равномерно распределены
    по диапазону второго массива.
    """
    if m < 1 or n < m:
        raise ValueError("Требуется 1 <= M <= N")

    arr_a = [
        2 * (i * n // m) + 1
        for i in range(m)
    ]
    arr_b = [
        2 * i
        for i in range(n)
    ]

    return arr_a, arr_b


def benchmark_algorithm(func, arr_a, arr_b) -> list[float]:
    """Возвращает результаты повторных замеров в секундах."""
    if func(arr_a, arr_b) is not False:
        raise AssertionError(
            f"{func.__name__} вернул неправильный результат"
        )

    times = []

    for _ in range(REPEATS):
        start = perf_counter()
        result = func(arr_a, arr_b)
        elapsed = perf_counter() - start

        if result is not False:
            raise AssertionError(
                f"{func.__name__} вернул неправильный результат"
            )

        times.append(elapsed)

    return times


def run_benchmarks() -> None:
    """Запускает все эксперименты и сохраняет сырые данные в CSV."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    columns = [
        "scenario",
        "m",
        "n",
        "ratio",
        "algorithm",
        "repeat",
        "time_sec",
    ]

    total = len(SCENARIOS) * len(ALGORITHMS)

    with CSV_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        experiment = 0

        for scenario, m, n in SCENARIOS:
            arr_a, arr_b = generate_arrays(m, n)
            ratio = n / m

            for name, func in ALGORITHMS.items():
                experiment += 1

                times = benchmark_algorithm(
                    func, arr_a, arr_b
                )

                for repeat, elapsed in enumerate(times, start=1):
                    writer.writerow({
                        "scenario": scenario,
                        "m": m,
                        "n": n,
                        "ratio": ratio,
                        "algorithm": name,
                        "repeat": repeat,
                        "time_sec": elapsed,
                    })

                print(
                    f"[{experiment}/{total}] "
                    f"{scenario}: M={m}, N={n}, "
                    f"{name}, "
                    f"медиана={median(times):.6f} сек"
                )

    print(f"\nРезультаты сохранены в {CSV_FILE}")


if __name__ == "__main__":
    run_benchmarks()
