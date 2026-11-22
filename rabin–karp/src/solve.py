def solve_with_rabin_karp(pattern: str, text: str) -> list:
    """Решение с помощью алгоритма Рабина-Карпа."""
    x = 61  # основание
    P = 10 ** 9 + 9  # модуль

    def get_hash(s: str) -> int:
        """Вычисляет полиномиальный хеш для строки s."""
        h = 0
        for i in range(len(s)):
            code = ord(s[i]) - 64
            h = (h * x + code) % P
        return h

    M = len(pattern)
    N = len(text)

    result = []
    pat_h = get_hash(pattern)
    cur_h = get_hash(text[0:M])
    max_pow = pow(x, M - 1, P)
    for i in range(N - M + 1):
        if cur_h == pat_h:
            match = True
            for j in range(M):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                result.append(i)

        if i < N - M:
            left_code = ord(text[i]) - 64
            right_code = ord(text[i + M]) - 64
            cur_h = ((cur_h - left_code * max_pow) * x + right_code) % P

    return result


if __name__ == "__main__":
    pattern = input()
    text = input()
    result = solve_with_rabin_karp(pattern, text)
    print(*result)
