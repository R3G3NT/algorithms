import pytest
from rope import *

def test_example_from_task():
    r = Rope("This is a text")
    assert str(r) == "This is a text"

    assert r.index(0) == "T"

    prefix, suffix = r.split(7)
    assert f"{prefix}|{suffix}" == "This is| a text"
    assert str(r) == "This is a text"  # исходная строка не изменилась

    r = r.insert(7, "_not")
    assert str(r) == "This is_not a text"

    r = r.delete(14, 3)
    assert str(r) == "This is_not a t"

    r = r.concat(Rope("!"))
    assert str(r) == "This is_not a t!"

def test_empty_and_long_strings():
    # Пустая строка
    r = Rope("")
    assert str(r) == ""
    assert r.root is None

    # Длинная строка
    r = r.concat(Rope("Hello, world! This is a long string."))
    assert str(r) == "Hello, world! This is a long string."
    assert r.index(7) == "w"

    # Удаление куска из середины
    r = r.delete(5, 8)
    assert str(r) == "Hello This is a long string."

def test_split_edges():
    r = Rope("Python")

    left, right = r.split(0)
    assert str(left) == ""
    assert str(right) == "Python"

    left, right = r.split(6)
    assert str(left) == "Python"
    assert str(right) == ""

def test_full_delete_and_rebuild():
    r = Rope("1234567890")
    r = r.delete(0, 10)
    assert str(r) == ""
    assert r.root is None

    r = r.concat(Rope("New text"))
    assert str(r) == "New text"

def test_avl_invariants():
    r = Rope("Initial_long_string_for_avl_check")
    r = r.insert(7, "_INSERTED_")
    r = r.delete(15, 6)
    r = r.concat(Rope("_END"))

    def check_height(node):
        if node is None:
            return -1
        if node.is_leaf():
            assert 1 <= len(node.text) <= 8
            assert node.height == 0
            return 0

        lh = check_height(node.left)
        rh = check_height(node.right)

        assert abs(lh - rh) <= 1              # АВЛ-баланс соблюдён
        assert node.height == 1 + max(lh, rh) # Высота записана верно
        return node.height

    check_height(r.root)
    check_height(r.root.left)
    check_height(r.root.right)
    check_height(r.root.left.left)
    check_height(r.root.left.right)
    check_height(r.root.right.left)
    check_height(r.root.right.right)