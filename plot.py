
import csv
from collections import defaultdict
from pathlib import Path
from statistics import median

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "data" / "results.csv"
PLOTS_DIR = BASE_DIR / "plots"

ALGORITHM_LABELS = {
    "two_pointers": "Two pointers",
    "binary_search": "Binary search",
    "exponential_search": "Exponential search",
    "double_binary_search": "Double binary search",
}


def load_results() -> list[dict]:
    """Читает сырые результаты измерений из CSV."""
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"Файл с результатами не найден: {CSV_FILE}\n"
            "Сначала запустите test_time.py."
        )

    with CSV_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)
        required_columns = {
            "scenario", "m", "n", "ratio",
            "algorithm", "time_sec",
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                "CSV не содержит все необходимые столбцы: "
                f"{required_columns}"
            )

        results = []

        for row in reader:
            row["m"] = int(row["m"])
            row["n"] = int(row["n"])
            row["ratio"] = float(row["ratio"])
            row["time_sec"] = float(row["time_sec"])

            if row["time_sec"] <= 0:
                raise ValueError(
                    "Время выполнения должно быть больше нуля "
                    "для логарифмической шкалы."
                )

            results.append(row)

    if not results:
        raise ValueError("CSV не содержит результатов измерений.")

    return results


def calculate_medians(
    results: list[dict],
) -> list[dict]:
    """Вычисляет медианное время для каждой комбинации параметров."""
    groups = defaultdict(list)

    for row in results:
        key = (
            row["scenario"],
            row["m"],
            row["n"],
            row["ratio"],
            row["algorithm"],
        )
        groups[key].append(row["time_sec"])

    medians = []

    for key, times in groups.items():
        scenario, m, n, ratio, algorithm = key

        medians.append({
            "scenario": scenario,
            "m": m,
            "n": n,
            "ratio": ratio,
            "algorithm": algorithm,
            "time_sec": median(times),
        })

    return medians


def plot_scenario(
    medians: list[dict],
    scenario: str,
    x_field: str,
    x_label: str,
    title: str,
    filename: str,
) -> None:
    """Строит график времени выполнения для одного сценария."""
    data = [
        row for row in medians
        if row["scenario"] == scenario
    ]

    if not data:
        print(
            f"Предупреждение: сценарий '{scenario}' "
            "не найден, график пропущен."
        )
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    algorithms = sorted({
        row["algorithm"] for row in data
    })

    for algorithm in algorithms:
        algorithm_data = sorted(
            (
                row for row in data
                if row["algorithm"] == algorithm
            ),
            key=lambda row: row[x_field],
        )

        x_values = [
            row[x_field] for row in algorithm_data
        ]
        y_values = [
            row["time_sec"] for row in algorithm_data
        ]

        ax.plot(
            x_values,
            y_values,
            marker="o",
            linewidth=2,
            markersize=5,
            label=ALGORITHM_LABELS.get(
                algorithm, algorithm
            ),
        )

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel(x_label)
    ax.set_ylabel("Median execution time (seconds)")
    ax.set_title(title)

    ax.grid(True, which="both", linestyle="--", alpha=0.4)
    ax.legend()
    fig.tight_layout()

    output_file = PLOTS_DIR / filename
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"График сохранён: {output_file}")


def main() -> None:
    """Строит три графика по результатам экспериментов."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    results = load_results()
    medians = calculate_medians(results)

    plot_scenario(
        medians=medians,
        scenario="equal_sizes",
        x_field="m",
        x_label="Array size (M = N)",
        title="Performance with equal array sizes",
        filename="equal_sizes.png",
    )

    plot_scenario(
        medians=medians,
        scenario="fixed_m",
        x_field="n",
        x_label="Large array size (N), M = 50",
        title="Performance with fixed M = 50",
        filename="fixed_m.png",
    )

    plot_scenario(
        medians=medians,
        scenario="varying_ratio",
        x_field="ratio",
        x_label="Array size ratio (N / M)",
        title="Performance with varying N / M ratio",
        filename="varying_ratio.png",
    )


if __name__ == "__main__":
    main()
