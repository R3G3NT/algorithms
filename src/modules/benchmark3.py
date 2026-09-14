import matplotlib.pyplot as plt
import time
from circular_deque import CircularDeque

SIZES = [100, 1000, 5000, 10_000, 50_000, 100_000, 1_000_000]

time_resize = [None] * len(SIZES)

j = 0
for n in SIZES:
    deq = CircularDeque(n, False)
    for i in range(n):
        deq.push_back(i)

    start_time = time.perf_counter_ns()
    deq.resize(n * 2)
    time_resize[j] = time.perf_counter_ns() - start_time

    j += 1

plt.figure(figsize=(12, 7))

plt.plot(SIZES, time_resize,
         marker='o', markersize=8, linestyle='-', label='resize')

plt.xlabel('Количество элементов (N)', fontsize=12)
plt.ylabel('Время на увеличение (нс)', fontsize=12)

plt.grid(True, linestyle='--', axis='both', alpha=0.7)
plt.xscale('log')
plt.yscale('log')

plt.legend(fontsize=11)
plt.show()