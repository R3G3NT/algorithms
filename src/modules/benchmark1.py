import matplotlib.pyplot as plt
import time
from circular_deque import CircularDeque

SIZES = [100, 1000, 5000, 10_000, 50_000, 100_000, 1_000_000]

# Создаем списки для хранения времени каждой операции
time_push_back = [None] * len(SIZES)
time_push_front = [None] * len(SIZES)
time_pop_back = [None] * len(SIZES)
time_pop_front = [None] * len(SIZES)

j = 0
for n in SIZES:
    # Замер push_back
    deq_pb = CircularDeque(n, False)
    start_time = time.perf_counter_ns()
    for i in range(n):
        deq_pb.push_back(i)
    time_push_back[j] = time.perf_counter_ns() - start_time

    # Замер push_front
    deq_pf = CircularDeque(n, False)
    start_time = time.perf_counter_ns()
    for i in range(n):
        deq_pf.push_front(i)
    time_push_front[j] = time.perf_counter_ns() - start_time

    # Замер pop_back
    deq_pob = CircularDeque(n, False)
    for i in range(n):
        deq_pob.push_back(i)
        
    start_time = time.perf_counter_ns()
    for i in range(n):
        deq_pob.pop_back()
    time_pop_back[j] = time.perf_counter_ns() - start_time

    # Замер pop_front
    deq_pof = CircularDeque(n, False)
    for i in range(n):
        deq_pof.push_back(i)
        
    start_time = time.perf_counter_ns()
    for i in range(n):
        deq_pof.pop_front()
    time_pop_front[j] = time.perf_counter_ns() - start_time

    j += 1

plt.figure(figsize=(12, 7))

# Делим общее время t на количество элементов n, чтобы получить время ОДНОЙ операции
plt.plot(SIZES, [t / n for t, n in zip(time_push_back, SIZES)], marker='o', markersize=8, linestyle='-', label='push_back')
plt.plot(SIZES, [t / n for t, n in zip(time_push_front, SIZES)], marker='o', markersize=8, linestyle='-', label='push_front')
plt.plot(SIZES, [t / n for t, n in zip(time_pop_back, SIZES)], marker='o', markersize=8, linestyle='-', label='pop_back')
plt.plot(SIZES, [t / n for t, n in zip(time_pop_front, SIZES)], marker='o', markersize=8, linestyle='-', label='pop_front')

plt.xlabel('Количество элементов (N)', fontsize=12)
plt.ylabel('Среднее время одной операции (нс)', fontsize=12)

plt.grid(True, linestyle='--', axis='both', alpha=0.7)
plt.xscale('log') 
plt.yscale('log') 

plt.legend(fontsize=11)
plt.show()