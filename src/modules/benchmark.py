import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from circular_deque import CircularDeque

SIZES = [100, 1_000, 5_000, 10_000, 50_000, 100_000, 1_000_000]
REPEATS = 2_000
RESIZE_REPEATS = 15

OUT_DIR = Path(__file__).resolve().parent.parent / "benchmarks"

COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
THEORY_COLOR = "#6b6b66"

GRID_KW = dict(color="#d8d8d4", linewidth=0.8)
LINE_KW = dict(linewidth=2.0, marker="o", markersize=8)


def make_deque(n: int) -> CircularDeque:
    deque = CircularDeque(n, False)
    for i in range(n):
        deque.push_back(i)
    return deque


def measure(setup, operation, repeats: int = REPEATS) -> float:
    state = setup()
    start = time.perf_counter_ns()
    for _ in range(repeats):
        operation(state)
    elapsed = time.perf_counter_ns() - start
    return elapsed / repeats


def bench_push_pop(n: int) -> dict:
    full = make_deque(n)

    def push_back_op(d):
        d.pop_front()
        d.push_back(0)

    def push_front_op(d):
        d.pop_back()
        d.push_front(0)

    def pop_front_op(d):
        d.pop_front()
        d.push_back(0)

    def pop_back_op(d):
        d.pop_back()
        d.push_front(0)

    return {
        "push_back": measure(lambda: full, push_back_op),
        "push_front": measure(lambda: full, push_front_op),
        "pop_front": measure(lambda: full, pop_front_op),
        "pop_back": measure(lambda: full, pop_back_op),
    }


def bench_access(n: int) -> dict:
    full = make_deque(n)
    return {
        "front": measure(lambda: full, lambda d: d.front()),
        "back": measure(lambda: full, lambda d: d.back()),
        "size": measure(lambda: full, lambda d: d.size()),
        "empty": measure(lambda: full, lambda d: d.empty()),
        "full": measure(lambda: full, lambda d: d.full()),
    }


def bench_resize(n: int) -> float:
    total = 0.0
    for _ in range(RESIZE_REPEATS):
        deque = make_deque(n)
        start = time.perf_counter_ns()
        deque.resize(n)
        total += time.perf_counter_ns() - start
    return total / RESIZE_REPEATS


def style_axes(ax, title: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=12, color="#1a1a19", pad=12)
    ax.set_xlabel("Число элементов в деке", fontsize=10, color="#4a4a46")
    ax.set_ylabel(ylabel, fontsize=10, color="#4a4a46")
    ax.set_xscale("log")
    ax.grid(True, which="major", **GRID_KW)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color("#b5b5b0")
    ax.tick_params(colors="#4a4a46", labelsize=9)


def plot_constant_group(results: dict, title: str, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)

    for index, (name, series) in enumerate(results.items()):
        ax.plot(SIZES, series, label=name, color=COLORS[index % len(COLORS)], **LINE_KW)

    all_values = [value for series in results.values() for value in series]
    theory_level = sum(all_values) / len(all_values)
    ax.axhline(theory_level, color=THEORY_COLOR, linewidth=1.5, linestyle="--",
               label="теоретическая оценка O(1)")

    ax.set_ylim(bottom=0, top=max(all_values) * 1.35)

    style_axes(ax, title, "Среднее время операции, нс")
    ax.legend(frameon=False, fontsize=9, labelcolor="#1a1a19")
    fig.tight_layout()
    fig.savefig(OUT_DIR / filename, facecolor="white")
    plt.close(fig)


def plot_resize(values: list) -> None:
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)

    ax.plot(SIZES, values, label="resize (замер)", color=COLORS[0], **LINE_KW)

    scale = values[0] / SIZES[0]
    theory = [scale * n for n in SIZES]
    ax.plot(SIZES, theory, color=THEORY_COLOR, linewidth=1.5, linestyle="--",
            label="теоретическая оценка O(n)")

    ax.set_yscale("log")
    style_axes(ax, "Время выполнения resize", "Время выполнения, нс")
    ax.legend(frameon=False, fontsize=9, labelcolor="#1a1a19")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "bench_resize.png", facecolor="white")
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    push_pop = {name: [] for name in ("push_back", "push_front", "pop_front", "pop_back")}
    access = {name: [] for name in ("front", "back", "size", "empty", "full")}
    resize_values = []

    for n in SIZES:
        print(f"n = {n:>9} ...", end=" ", flush=True)

        for name, value in bench_push_pop(n).items():
            push_pop[name].append(value)
        for name, value in bench_access(n).items():
            access[name].append(value)
        resize_values.append(bench_resize(n))

        print("готово")

    plot_constant_group(push_pop, "Операции добавления и удаления", "bench_push_pop.png")
    plot_constant_group(access, "Операции доступа и проверки состояния", "bench_access.png")
    plot_resize(resize_values)

    print()
    print("Таблица замеров (нс на операцию):")
    header = "n".rjust(10) + "".join(name.rjust(12) for name in list(push_pop) + list(access)) + "resize".rjust(14)
    print(header)
    for row, n in enumerate(SIZES):
        line = str(n).rjust(10)
        for name in push_pop:
            line += f"{push_pop[name][row]:12.1f}"
        for name in access:
            line += f"{access[name][row]:12.1f}"
        line += f"{resize_values[row]:14.1f}"
        print(line)

    print()
    print(f"Графики сохранены в {OUT_DIR}")


if __name__ == "__main__":
    main()
