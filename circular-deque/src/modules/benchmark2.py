import matplotlib.pyplot as plt
import time
from circular_deque import CircularDeque

SIZES = [100, 1000, 5000, 10_000, 50_000, 100_000, 1_000_000]

time_empty = [None] * len(SIZES)
time_full = [None] * len(SIZES)
time_size = [None] * len(SIZES)
time_back = [None] * len(SIZES)
time_front = [None] * len(SIZES)

j = 0
for n in SIZES:
    # Заполняем дек для операций back/front
    deq_filled = CircularDeque(n, False)
    for i in range(n):
        deq_filled.push_back(i)

    # Пустой дек для empty/full/size (empty на пустом, full на пустом = False)
    deq_empty = CircularDeque(n, False)

    # Замер empty (на пустом деке)
    start_time = time.perf_counter_ns()
    for _ in range(n):
        deq_empty.empty()
    time_empty[j] = time.perf_counter_ns() - start_time

    # Замер full (на заполненном деке)
    start_time = time.perf_counter_ns()
    for _ in range(n):
        deq_filled.full()
    time_full[j] = time.perf_counter_ns() - start_time

    # Замер size
    start_time = time.perf_counter_ns()
    for _ in range(n):
        deq_filled.size()
    time_size[j] = time.perf_counter_ns() - start_time

    # Замер back
    start_time = time.perf_counter_ns()
    for _ in range(n):
        deq_filled.back()
    time_back[j] = time.perf_counter_ns() - start_time

    # Замер front
    start_time = time.perf_counter_ns()
    for _ in range(n):
        deq_filled.front()
    time_front[j] = time.perf_counter_ns() - start_time

    j += 1

plt.figure(figsize=(12, 7))

plt.plot(SIZES, [t / n for t, n in zip(time_empty, SIZES)],
         marker='o', markersize=8, linestyle='-', label='empty')
plt.plot(SIZES, [t / n for t, n in zip(time_full, SIZES)],
         marker='o', markersize=8, linestyle='-', label='full')
plt.plot(SIZES, [t / n for t, n in zip(time_size, SIZES)],
         marker='o', markersize=8, linestyle='-', label='size')
plt.plot(SIZES, [t / n for t, n in zip(time_back, SIZES)],
         marker='o', markersize=8, linestyle='-', label='back')
plt.plot(SIZES, [t / n for t, n in zip(time_front, SIZES)],
         marker='o', markersize=8, linestyle='-', label='front')

plt.xlabel('Количество элементов (N)', fontsize=12)
plt.ylabel('Среднее время одной операции (нс)', fontsize=12)

plt.grid(True, linestyle='--', axis='both', alpha=0.7)
plt.xscale('log')
plt.yscale('log')

plt.legend(fontsize=11)
plt.show()