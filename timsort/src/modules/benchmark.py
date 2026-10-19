import random
import time
import matplotlib.pyplot as plt
from timsort.src.timsort import *


def generate_data(size: int, case_type: str) -> list:
    if case_type == "sort":
        # Уже отсортирован по убыванию модуля
        return list(range(size, 0, -1))
    elif case_type == "reverse":
        # Полностью перевернутый массив (по возрастанию модуля)
        return list(range(1, size + 1))
    else:
        # Cлучайные числа
        return [random.randint(-size, size) for _ in range(size)]


def run_benchmarks():
    sizes = [10, 1000, 100000]
    cases = ["sort", "chaotic", "reverse"]
    results = {case: [] for case in cases}

    print("Запуск исследования производительности TimSort:")
    for size in sizes:
        print(f"Тестирование размера N = {size}:")
        for case in cases:
            arr = generate_data(size, case)

            # Измеряем точное время выполнения
            start_time = time.perf_counter()
            timsort(arr, minrun_limit=64, min_gallop=7)
            end_time = time.perf_counter()

            execution_time_ms = (end_time - start_time) * 1000
            results[case].append(execution_time_ms)
            print(f"  - {case}: {execution_time_ms:.4f} ms")

    plt.figure(figsize=(10, 6))

    plt.plot(sizes, results["sort"], marker='o', linestyle='-', label="Отсортированный (O(N))")
    plt.plot(sizes, results["reverse"], marker='o', linestyle='-', label="Обратный (O(N))")
    plt.plot(sizes, results["chaotic"], marker='o', linestyle='-', label="Случайный (O(N log N))")

    plt.xscale('log')
    plt.yscale('log')

    plt.title("Исследование времени выполнения", fontsize=14)
    plt.xlabel("Размер входного массива (N)", fontsize=12)
    plt.ylabel("Время выполнения (мс)", fontsize=12)
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend(fontsize=11)
    plt.show()


if __name__ == "__main__":
    run_benchmarks()
