import random
import statistics
import string
import time
import matplotlib.pyplot as plt


def rk_additive(pattern: str, text: str, P: int = 10**9 + 9):
    """Аддитивный хеш: сумма кодов символов по модулю P."""
    M, N = len(pattern), len(text)

    t0 = time.perf_counter_ns()
    pat_h = sum(ord(ch) - 64 for ch in pattern) % P
    cur_h = sum(ord(text[i]) - 64 for i in range(M)) % P
    prep_ms = (time.perf_counter_ns() - t0) / 1e6

    t1 = time.perf_counter_ns()
    hash_hits = 0
    confirmed = 0

    for i in range(N - M + 1):
        if cur_h == pat_h:
            hash_hits += 1
            if pattern == text[i : i + M]:
                confirmed += 1
        if i < N - M:
            cur_h = (cur_h - (ord(text[i]) - 64) + (ord(text[i + M]) - 64)) % P

    search_ms = (time.perf_counter_ns() - t1) / 1e6
    collisions = hash_hits - confirmed
    return prep_ms, search_ms, hash_hits, collisions, confirmed


def rk_poly_single(pattern: str, text: str, x: int = 61, P: int = 10**9 + 9):
    """Полиномиальный хеш с одним модулем P."""
    M, N = len(pattern), len(text)

    t0 = time.perf_counter_ns()
    pat_h = cur_h = 0
    for i in range(M):
        pat_h = (pat_h * x + (ord(pattern[i]) - 64)) % P
        cur_h = (cur_h * x + (ord(text[i]) - 64)) % P
    max_pow = pow(x, M - 1, P)
    prep_ms = (time.perf_counter_ns() - t0) / 1e6

    t1 = time.perf_counter_ns()
    hash_hits = 0
    confirmed = 0

    for i in range(N - M + 1):
        if cur_h == pat_h:
            hash_hits += 1
            if pattern == text[i : i + M]:
                confirmed += 1
        if i < N - M:
            left_code = ord(text[i]) - 64
            right_code = ord(text[i + M]) - 64
            cur_h = ((cur_h - left_code * max_pow) * x + right_code) % P

    search_ms = (time.perf_counter_ns() - t1) / 1e6
    collisions = hash_hits - confirmed
    return prep_ms, search_ms, hash_hits, collisions, confirmed


def rk_poly_double(
    pattern: str, text: str, x1: int = 61, P1: int = 10**9 + 7, x2: int = 67, P2: int = 10**9 + 9
):
    """Полиномиальный хеш с двумя независимыми модулями."""
    M, N = len(pattern), len(text)

    t0 = time.perf_counter_ns()
    pat_h1 = cur_h1 = pat_h2 = cur_h2 = 0
    for i in range(M):
        c_p = ord(pattern[i]) - 64
        c_t = ord(text[i]) - 64
        pat_h1 = (pat_h1 * x1 + c_p) % P1
        cur_h1 = (cur_h1 * x1 + c_t) % P1
        pat_h2 = (pat_h2 * x2 + c_p) % P2
        cur_h2 = (cur_h2 * x2 + c_t) % P2
    max_pow1 = pow(x1, M - 1, P1)
    max_pow2 = pow(x2, M - 1, P2)
    prep_ms = (time.perf_counter_ns() - t0) / 1e6

    t1 = time.perf_counter_ns()
    hash_hits = 0
    confirmed = 0

    for i in range(N - M + 1):
        if cur_h1 == pat_h1 and cur_h2 == pat_h2:
            hash_hits += 1
            if pattern == text[i : i + M]:
                confirmed += 1
        if i < N - M:
            left_c = ord(text[i]) - 64
            right_c = ord(text[i + M]) - 64
            cur_h1 = ((cur_h1 - left_c * max_pow1) * x1 + right_c) % P1
            cur_h2 = ((cur_h2 - left_c * max_pow2) * x2 + right_c) % P2

    search_ms = (time.perf_counter_ns() - t1) / 1e6
    collisions = hash_hits - confirmed
    return prep_ms, search_ms, hash_hits, collisions, confirmed


def make_datasets(N: int, M: int) -> dict:
    t1 = list(random.choices(string.ascii_letters, k=N))
    p1 = "".join(random.choices(string.ascii_letters, k=M))
    t1[N // 2:N // 2 + M] = list(p1)

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


def run_5_times(func, pat: str, txt: str, **kwargs):
    preps, searches = [], []
    hits = cols = conf = 0
    for _ in range(5):
        p_ms, s_ms, hits, cols, conf = func(pat, txt, **kwargs)
        preps.append(p_ms)
        searches.append(s_ms)
    return statistics.median(preps), statistics.median(searches), hits, cols, conf


random.seed(42)

print("=== 1. СРАВНЕНИЕ 3 ХЕШ-ФУНКЦИЙ НА РАЗНЫХ РАЗМЕРАХ N И M (медиана 5 запусков) ===")
for N, M in [(50_000, 10), (100_000, 30), (200_000, 50)]:
    print(f"\n--- Размер текста N = {N}, размер образца M = {M} ---")
    print(f"{'Тип данных':<20} | {'Хеш-функция':<18} | {'Prep(мс)':<8} | {'Search(мс)':<10} | {'Hits':<7} | {'Коллизии':<8} | {'Найдено'}")
    print("-" * 92)
    for ds_name, (pat, txt) in make_datasets(N, M).items():
        for h_name, func in [
            ("Аддитивный", rk_additive),
            ("Полином (1 mod)", rk_poly_single),
            ("Полином (2 mod)", rk_poly_double),
        ]:
            prep, srch, hits, cols, conf = run_5_times(func, pat, txt)
            print(f"{ds_name:<20} | {h_name:<18} | {prep:<8.4f} | {srch:<10.2f} | {hits:<7} | {cols:<8} | {conf}")

print("\n=== 2. ВЛИЯНИЕ ОСНОВАНИЯ x И МОДУЛЯ P НА КОЛЛИЗИИ (Случайный текст, N = 100 000, M = 10) ===")
pat_r, txt_r = make_datasets(100_000, 10)["Случайный"]
configs = [
    ("x=2, P=101 (малые)", 2, 101),
    ("x=31, P=101 (малый P)", 31, 101),
    ("x=10, P=10007 (плохой x)", 10, 10007),
    ("x=61, P=10007 (средний P)", 61, 10007),
    ("x=61, P=10^9+9 (большой P)", 61, 10**9 + 9),
]
for label, x_val, p_val in configs:
    _, srch, hits, cols, conf = run_5_times(rk_poly_single, pat_r, txt_r, x=x_val, P=p_val)
    print(f"{label:<28} -> Коллизий: {cols:<6} | Время поиска: {srch:.2f} мс")

datasets_plot = make_datasets(100_000, 20)
cols_for_plot = {
    "Аддитивный\n(P=10007)": 0,
    "Полином 1 mod\n(x=61, P=10007)": 0,
    "Полином 2 mod\n(P1=10007, P2=10009)": 0,
}
for pat, txt in datasets_plot.values():
    cols_for_plot["Аддитивный\n(P=10007)"] += rk_additive(pat, txt, P=10007)[3]
    cols_for_plot["Полином 1 mod\n(x=61, P=10007)"] += rk_poly_single(pat, txt, x=61, P=10007)[3]
    cols_for_plot["Полином 2 mod\n(P1=10007, P2=10009)"] += rk_poly_double(pat, txt, P1=10007, P2=10009)[3]

plt.figure(figsize=(8, 5))
bars = plt.bar(list(cols_for_plot.keys()), list(cols_for_plot.values()), color=["#d9534f", "#f0ad4e", "#5cb85c"])
plt.title("Количество коллизий в зависимости от выбора хеш-функции")
plt.ylabel("Суммарное число коллизий (по 5 типам текстов)")
top_val = max(cols_for_plot.values()) if max(cols_for_plot.values()) > 0 else 1
for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, y + top_val * 0.01, str(y), ha="center")
plt.tight_layout()
plt.savefig("graph_collisions.png", dpi=200)
print("\nГрафик сохранён: graph_collisions.png")
