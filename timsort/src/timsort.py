MINRUN_LIMIT = 16
MIN_GALLOP = 3


def get_minrun(n: int, minrun_limit: int=MINRUN_LIMIT) -> int:
    """Вычисляет minrun."""
    r = 0
    while n >= minrun_limit:
        r |= n & 1
        n >>= 1
    return n + r


def insertion_sort(run: list) -> list:
    """Сортирует run вставками по убыванию модуля."""
    for i in range(1, len(run)):
        cur = run[i]
        j = i
        while j > 0 and abs(run[j - 1]) < abs(cur):
            run[j] = run[j - 1]
            j -= 1
        run[j] = cur
    return run


def cut_runs(arr: list, minrun: int) -> list:
    """Делит массив на блоки run."""
    runs = []
    start = 0
    size = len(arr)
    while start < size:
        stop = start + 1
        rising = stop < size and abs(arr[stop]) > abs(arr[start])
        while stop < size:
            if rising and abs(arr[stop]) <= abs(arr[stop - 1]):
                break
            if not rising and abs(arr[stop]) > abs(arr[stop - 1]):
                break
            stop += 1
        run = arr[start:stop]

        if rising:
            run = run[::-1]
        if stop - start < minrun:
            stop = min(start + minrun, size)
            run += arr[start + len(run): stop]

        runs.append(insertion_sort(run))
        start = stop
    return runs


def gallop_search(run: list, start: int, target: int) -> int:
    """Бинарный поиск с галопом."""
    size = len(run)
    i, j, step = start, start + 1, 1
    while j < size and abs(run[j]) >= abs(target):
        i = j
        j += step
        step *= 2

    low, high = i, min(j, size)
    while low < high:
        mid = (low + high) // 2
        if abs(run[mid]) >= abs(target):
            low = mid + 1
        else:
            high = mid
    return low


def merge(left: list, right: list, min_gallop: int) -> tuple:
    """Сливает массивы left и right в один, и возвращает количество галопов."""
    res = []
    l = r = 0
    win_left = win_right = 0
    gallops_count = 0
    while l < len(left) and r < len(right):
        if win_left >= min_gallop:
            gallops_count += 1
            k = gallop_search(left, l, right[r])
            res.extend(left[l:k])
            l = k
            win_left = 0

        elif win_right >= min_gallop:
            gallops_count += 1
            k = gallop_search(right, r, left[l])
            res.extend(right[r:k])
            r = k
            win_right = 0

        elif abs(left[l]) >= abs(right[r]):
            res.append(left[l])
            l += 1
            win_left += 1
            win_right = 0
        else:
            res.append(right[r])
            r += 1
            win_right += 1
            win_left = 0

    if win_left >= min_gallop or win_right >= min_gallop:
        gallops_count += 1

    return res + left[l:] + right[r:], gallops_count


def join(stack: list, pos: int, log: list, min_gallop: int):
    """Объединяет два массива в стеке."""
    merged, gallops_count = merge(stack[pos], stack[pos + 1], min_gallop)
    stack[pos:pos + 2] = [merged]
    log.append((gallops_count, merged))


def invariant(stack: list, log: list, min_gallop: int):
    """Тот самый инвариант timsort."""
    while len(stack) >= 2:
        x = len(stack[-1])
        y = len(stack[-2])
        z = None
        if len(stack) >= 3:
            z = len(stack[-3])

        if y <= x:
            join(stack, len(stack) - 2, log, min_gallop)
        elif z is not None and z <= x + y:
            if z < x:
                join(stack, len(stack) - 3, log, min_gallop)
            else:
                join(stack, len(stack) - 2, log, min_gallop)
        else:
            break


def merge_all(runs: list, min_gallop: int) -> tuple:
    """Сливает все run в один массив."""
    stack = []
    log = []
    for run in runs:
        stack.append(run)
        invariant(stack, log, min_gallop)
    while len(stack) > 1:
        join(stack, len(stack) - 2, log, min_gallop)

    if stack:
        return stack[0], log
    return [], log


def timsort(arr: list, minrun_limit: int = MINRUN_LIMIT, min_gallop: int = MIN_GALLOP) -> tuple:
    """Точка входа в timsort."""
    minrun = get_minrun(len(arr), minrun_limit)
    runs = cut_runs(arr, minrun)
    result, log = merge_all(runs, min_gallop)
    return runs, log, result


def print_log(runs, log, result):
    for i, run in enumerate(runs):
        print(f"Part {i}:", *run)

    for i, (gallops_count, merged) in enumerate(log):
        print(f"Gallops {i}: {gallops_count}")
        print(f"Merge {i}:", *merged)

    print("Answer:", *result)


def main():
    n = int(input())
    arr = [int(i) for i in input().split()[:n]]
    runs, log, result = timsort(arr)
    print_log(runs, log, result)


if __name__ == "__main__":
    main()
