import pytest
from solve import solve_with_rabin_karp


def test_example_from_task():
    assert solve_with_rabin_karp("aba", "abacaba") == [0, 4]


def test_overlapping_matches():
    assert solve_with_rabin_karp("aa", "aaaa") == [0, 1, 2]


def test_case_sensitivity():
    assert solve_with_rabin_karp("AbA", "abacabaAbAc") == [7]
    assert solve_with_rabin_karp("aba", "ABACABA") == []


def test_not_found():
    assert solve_with_rabin_karp("xyz", "abacaba") == []


def test_edge_cases():
    assert solve_with_rabin_karp("a", "abacaba") == [0, 2, 4, 6]
    assert solve_with_rabin_karp("abacaba", "abacaba") == [0]
    assert solve_with_rabin_karp("abacaba", "aba") == []
