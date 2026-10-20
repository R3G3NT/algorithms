import random
import time
import matplotlib.pyplot as plt
from timsort.src.timsort import *


def minrun_benchmark():
    n = 100_000
    minruns = [16, 32, 64, 128, 256, 512]

    data = [random.randint(-n, n) for _ in range(n)]

    total_times_ns = []

    print(f"Время сортировки при разных min_run, n = {n}")
    print("-" * 35)
    print(f"{'MINRUN':<10} | {'Время (нс)':<20}")
    print("-" * 35)

    for mr in minruns:
        arr_copy = data[:]

        start_time = time.perf_counter_ns()
        timsort(arr_copy, min_gallop=7, minrun_limit=mr)
        end_time = time.perf_counter_ns()

        execution_time_ns = end_time - start_time
        total_times_ns.append(execution_time_ns)

        print(f"{mr:<10} | {execution_time_ns:<20}")

    print("-" * 35)

    plt.figure(figsize=(8, 8))

    plt.plot(minruns, total_times_ns, marker='o', markersize=8, linestyle='-', linewidth=2, label="minruns")
    plt.xlabel("Значение minrun", fontsize=12)
    plt.ylabel("Время операции (нс)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=11)
    plt.show()


if __name__ == "__main__":
    minrun_benchmark()
