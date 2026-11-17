import math
import time
import matplotlib.pyplot as plt
from rope.src.rope import *

def measure_us(func, repeats: int = 500) -> float:
    """Замеряет среднее время выполнения функции в микросекундах (мкс)."""
    start = time.perf_counter_ns()
    for _ in range(repeats):
        func()
    end = time.perf_counter_ns() - start
    return (end / repeats) / 1000.0

def run_benchmarks() -> None:
    sizes = [100, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    repeats = 500

    # Словарь для накопления результатов каждой операции
    results = {
        "index": [],
        "concat": [],
        "split": [],
        "insert": [],
        "delete": [],
    }

    header = f"{'Длина n':>10} | {'index':>9} | {'concat':>9} | {'split':>9} | {'insert':>9} | {'delete':>9}"
    print(header)
    print("-" * len(header))

    for n in sizes:
        text = "a" * n
        rope = Rope(text)
        extra_char = Rope("X")
        mid = n // 2

        t_index = measure_us(lambda: rope.index(mid), repeats)
        t_concat = measure_us(lambda: rope.concat(extra_char), repeats)
        t_split = measure_us(lambda: rope.split(mid), repeats)
        t_insert = measure_us(lambda: rope.insert(mid, "X"), repeats)
        t_delete = measure_us(lambda: rope.delete(mid, 1), repeats)

        results["index"].append(t_index)
        results["concat"].append(t_concat)
        results["split"].append(t_split)
        results["insert"].append(t_insert)
        results["delete"].append(t_delete)

        print(
            f"{n:>10} | "
            f"{t_index:>6.2f} мкс | "
            f"{t_concat:>6.2f} мкс | "
            f"{t_split:>6.2f} мкс | "
            f"{t_insert:>6.2f} мкс | "
            f"{t_delete:>6.2f} мкс"
        )

    plot_results(sizes, results)


def plot_results(sizes: list, results: dict) -> None:
    """Строит и сохраняет график времени выполнения всех операций."""
    plt.figure(figsize=(10, 6))

    # Рисуем кривые для всех 5 операций
    for op_name, times in results.items():
        plt.plot(sizes, times, marker="o", linewidth=2, label=op_name)

    # Добавляем пунктирную теоретическую кривую c * log2(n) для ориентира
    theory = [0.5 * math.log2(n) for n in sizes]
    plt.plot(sizes, theory, linestyle="--", color="gray", alpha=0.8, label="Теория: c · log₂(n)")

    plt.xscale("log")
    plt.yscale("log")
    plt.title("Время операций структуры Rope в зависимости от длины строки n", fontsize=12)
    plt.xlabel("Длина строки n (символов)", fontsize=11)
    plt.ylabel("Среднее время операции (мкс)", fontsize=11)
    plt.grid(True, which="both", linestyle=":", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_benchmarks()
