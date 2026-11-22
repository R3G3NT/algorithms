import random
import statistics
import string
import time
import matplotlib.pyplot as plt
from solve import solve_with_rabin_karp


def solve_with_find(pattern: str, text: str) -> list:
    """Поиск всех вхождений с помощью повторных вызовов find."""
    result = []
    pos = text.find(pattern, 0)
    while pos != -1:
        result.append(pos)
        pos = text.find(pattern, pos + 1)
    return result


def find_first_rabin_karp(pattern: str, text: str) -> int:
    """Поиск первой позиции вхождения (аналог text.find(pattern, 0))."""
    M, N = len(pattern), len(text)
    if M > N:
        return -1

    x = 61
    P = 10**9 + 9

    pat_h = cur_h = 0
    for i in range(M):
        pat_h = (pat_h * x + (ord(pattern[i]) - 64)) % P
        cur_h = (cur_h * x + (ord(text[i]) - 64)) % P

    max_pow = pow(x, M - 1, P)

    for i in range(N - M + 1):
        if cur_h == pat_h and pattern == text[i : i + M]:
            return i
        if i < N - M:
            left_code = ord(text[i]) - 64
            right_code = ord(text[i + M]) - 64
            cur_h = ((cur_h - left_code * max_pow) * x + right_code) % P

    return -1


def in_rabin_karp(pattern: str, text: str) -> bool:
    """Проверка наличия вхождения (аналог pattern in text)."""
    return find_first_rabin_karp(pattern, text) != -1


def make_datasets(N: int, M: int) -> dict:
    alpha = string.ascii_letters

    t1 = list(random.choices(alpha, k=N))
    p1 = "".join(random.choices(alpha, k=M))
    t1[N // 2 : N // 2 + M] = list(p1)

    p5 = ("abcdefghij" * (M // 10 + 1))[:M]
    block = list(p5)
    t5 = []
    while len(t5) < N:
        random.shuffle(block)
        t5.extend(block)

    return {
        "Случайный": (p1, "".join(t1)),
        "Много совпадений": ("a" * M, "a" * N),
        "Длинные повторы": ("a" * (M - 1) + "b", "a" * N),
        "Отсутствует": ("Z" * M, "".join(random.choices(string.ascii_lowercase, k=N))),
        "Аддитивные коллизии": (p5, "".join(t5[:N])),
    }


def measure(func, pat: str, txt: str, runs: int = 5) -> float:
    times = []
    for _ in range(runs):
        start = time.perf_counter_ns()
        func(pat, txt)
        times.append(time.perf_counter_ns() - start)
    return statistics.median(times) / 1e6


random.seed(42)
sizes_N = [20_000, 50_000, 100_000, 200_000]
sizes_M = [10, 30, 100, 300]
rk_plot = {name: [] for name in make_datasets(100, 10)}
find_plot = []

print("--- 1. СРАВНЕНИЕ НА 5 ТИПАХ ДАННЫХ (N = 100 000, M = 30, мс) ---")
for name, (pat, txt) in make_datasets(100_000, 30).items():
    t_rk_in = measure(in_rabin_karp, pat, txt)
    t_py_in = measure(lambda p, t: p in t, pat, txt)

    t_rk_1 = measure(find_first_rabin_karp, pat, txt)
    t_py_1 = measure(lambda p, t: t.find(p, 0), pat, txt)

    t_rk_all = measure(solve_with_rabin_karp, pat, txt)
    t_py_all = measure(solve_with_find, pat, txt)

    print(
        f"{name:<20} | in: RK={t_rk_in:.2f}, Py={t_py_in:.2f} | "
        f"1st: RK={t_rk_1:.2f}, Py={t_py_1:.2f} | "
        f"all: RK={t_rk_all:.2f}, Py={t_py_all:.2f}"
    )

print("\n--- 2. РАЗНЫЕ РАЗМЕРЫ ОБРАЗЦА M (N = 100 000, Случайный текст) ---")
for M in sizes_M:
    pat, txt = make_datasets(100_000, M)["Случайный"]
    print(f"M = {M:<3} -> RK all: {measure(solve_with_rabin_karp, pat, txt):.2f} мс | find all: {measure(solve_with_find, pat, txt):.2f} мс")

for N in sizes_N:
    data = make_datasets(N, 30)
    for name, (pat, txt) in data.items():
        rk_plot[name].append(measure(solve_with_rabin_karp, pat, txt))
    find_plot.append(measure(solve_with_find, *data["Случайный"]))

plt.figure(figsize=(9, 5))
for name, times in rk_plot.items():
    plt.plot(sizes_N, times, marker="o", label=f"RK: {name}")
plt.plot(sizes_N, find_plot, marker="s", linestyle="--", color="black", label="Python find (Случайный)")

plt.title("Зависимость времени поиска от длины текста (M = 30)")
plt.xlabel("Длина текста N")
plt.ylabel("Медианное время (мс)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("graph_time.png", dpi=200)
print("\nГрафик сохранён: graph_time.png")
