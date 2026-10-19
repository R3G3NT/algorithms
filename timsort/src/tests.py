import pytest
from timsort import *


def test_get_minrun():
    """Проверка корректности вычисления minrun для разных n."""
    # Если n меньше предела (16), minrun должен быть равен n
    assert get_minrun(10) == 10
    assert get_minrun(15) == 15
    # Если n >= 16, вычисляется по логике сдвигов
    assert get_minrun(16) == 8
    assert get_minrun(20) == 10


def test_insertion_sort():
    """Проверка сортировки вставками по убыванию модуля."""
    assert insertion_sort([1, -2, 3]) == [3, -2, 1]
    assert insertion_sort([-5, 0, 10, -3]) == [10, -5, -3, 0]


def test_example_1():
    """Пример 1."""
    arr = [1, -2, 3, -4, 5, 6, -7, -8, 9, -10, 11, -10, -9, 8, 7, -7, -6, 6, 5, 4]
    expected_ans = [11, -10, -10, 9, -9, -8, 8, -7, 7, -7, 6, -6, 6, 5, 5, -4, 4, 3, -2, 1]

    runs, log, result = timsort(arr, minrun_limit=16, min_gallop=3)

    assert result == expected_ans
    assert len(runs) == 2
    assert len(log) == 1
    assert log[0][0] == 0 # это количество галопов в первом слиянии


def test_example_2():
    """Пример 2."""
    arr = [-1, 2, 3, 4, 5, -6, 7, 8, -8, -8, 7, -7, 7, 6, -5, 4]
    expected_ans = [8, -8, -8, 7, 7, -7, 7, 6, -6, 5, -5, 4, 4, 3, 2, -1]

    runs, log, result = timsort(arr, minrun_limit=16, min_gallop=3)

    assert result == expected_ans
    assert len(runs) == 2
    assert len(log) == 1
    assert log[0][0] == 1  # в примере 2 должен быть ровно 1 галоп


def test_empty_and_single():
    """Тест на граничные случаи."""
    # Пустой массив
    _, _, res_empty = timsort([])
    assert res_empty == []

    # Один элемент
    _, _, res_single = timsort([42])
    assert res_single == [42]


def test_already_sorted():
    """Тест на уже отсортированном по убыванию модуля массиве."""
    arr = [100, -50, 20, -5, 1]
    _, _, result = timsort(arr)
    assert result == [100, -50, 20, -5, 1]
