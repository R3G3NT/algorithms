import pytest
from modules.circular_deque import CircularDeque 

# 1. Тесты базовых операций и краевых случаев (пустая / полная дека)

def test_empty_and_initial_state():
    """Проверка начального состояния деки."""
    dq = CircularDeque(3, push_force=False)
    assert dq.empty() is True
    assert dq.full() is False
    assert dq.size() == 0
    
    # Попытка взять элементы или удалить из пустой деки должна вызывать ошибку
    with pytest.raises(IndexError):
        dq.front()
    with pytest.raises(IndexError):
        dq.back()
    with pytest.raises(IndexError):
        dq.pop_front()
    with pytest.raises(IndexError):
        dq.pop_back()

def test_push_pop_basic():
    """Проверка стандартного добавления и удаления без переполнения."""
    dq = CircularDeque(3, push_force=False)
    
    dq.push_back(10)  # [10]
    dq.push_back(20)  # [10, 20]
    dq.push_front(5)  # [5, 10, 20]
    
    assert dq.size() == 3
    assert dq.full() is True
    assert dq.front() == 5
    assert dq.back() == 20
    
    assert dq.pop_front() == 5
    assert dq.pop_back() == 20
    assert dq.pop_front() == 10
    assert dq.empty() is True

# 2. Тесты для push_force = false (блокировка при переполнении)

def test_push_back_overflow_exception():
    """Если push_force=False, push_back в полную деку вызывает OverflowError."""
    dq = CircularDeque(2, push_force=False)
    dq.push_back(1)
    dq.push_back(2)
    
    with pytest.raises(OverflowError):
        dq.push_back(3)

def test_push_front_overflow_exception():
    """Если push_force=False, push_front в полную деку вызывает OverflowError."""
    dq = CircularDeque(2, push_force=False)
    dq.push_front(1)
    dq.push_front(2)
    
    with pytest.raises(OverflowError):
        dq.push_front(3)

# 3. Тесты для push_force = true (перезапись старых элементов)

def test_push_back_with_force():
    """При push_back в полную деку новый элемент затирает front (пример из мудла)."""
    dq = CircularDeque(3, push_force=True)
    dq.push_back(1)
    dq.push_back(2)
    dq.push_back(3) # Дека полная: front=1, back=3
    
    dq.push_back(4) # Перезапись: 4 затирает 1, front=2, back=4
    assert dq.size() == 3
    assert dq.front() == 2
    assert dq.back() == 4
    
    assert dq.pop_front() == 2
    assert dq.pop_front() == 3
    assert dq.pop_front() == 4
    assert dq.empty() is True

def test_push_front_with_force():
    """При push_front в полную деку новый элемент затирает back."""
    dq = CircularDeque(3, push_force=True)
    dq.push_back(1)
    dq.push_back(2)
    dq.push_back(3) # Дека полная: front=1, back=3
    
    dq.push_front(0) # Перезапись: 0 затирает 3, front=0, back=2
    assert dq.size() == 3
    assert dq.front() == 0
    assert dq.back() == 2
    
    assert dq.pop_back() == 2
    assert dq.pop_back() == 1
    assert dq.pop_front() == 0

# 4. Тесты для метода resize

def test_resize_expand():
    """Проверка увеличения размера деки."""
    dq = CircularDeque(2, push_force=False)
    dq.push_back(1)
    dq.push_back(2)
    
    dq.resize(4) # Увеличиваем вместимость до 4
    assert dq.size() == 2
    assert dq.full() is False
    
    dq.push_back(3)
    dq.push_front(0)
    
    assert dq.front() == 0
    assert dq.back() == 3
    assert dq.size() == 4

def test_resize_shrink():
    """Проверка уменьшения размера деки."""
    dq = CircularDeque(3, push_force=False)
    dq.push_back(10)
    dq.push_back(20)
    dq.push_back(30)
    
    dq.resize(2) # Оставляем только 2 первых элемента с начала деки (10 и 20)
    assert dq.size() == 2
    assert dq.full() is True
    assert dq.front() == 10
    assert dq.back() == 20
    
    assert dq.pop_front() == 10
    assert dq.pop_back() == 20
    assert dq.empty() is True

def test_invalid_capacity():
    """Проверка генерации ошибок при некорректной емкости в __init__ и resize."""
    with pytest.raises(ValueError):
        CircularDeque(0, push_force=False)

    with pytest.raises(ValueError):
        CircularDeque(-5, push_force=False)

    dq = CircularDeque(3, push_force=False)
    with pytest.raises(ValueError):
        dq.resize(0)

def test_resize_on_empty_deque():
    """Проверка исправления бага: resize пустой деки не создает фантомный элемент."""
    dq = CircularDeque(3, push_force=False)

    assert dq.size() == 0
    assert dq.empty() is True

    dq.resize(5)

    assert dq.size() == 0
    assert dq.empty() is True

    with pytest.raises(IndexError):
        dq.front()

def test_mixed_operations_with_resize():
    """Проверка смешанных операций с циклическим переходом индексов и последующим resize."""
    dq = CircularDeque(3, push_force=True)

    dq.push_back(1)  # [1, None, None], head = 0, tail = 0
    dq.push_back(2)  # [1, 2, None], head = 0, tail = 1
    dq.push_back(3)  # [1, 2, 3], head = 0, tail = 2
    dq.push_front(0) # [1, 2, 0], head = 2, tail = 1
    dq.push_back(4)  # [1, 2, 4], head = 0, tail = 2

    assert dq.front() == 1
    assert dq.back() == 4
    assert dq.size() == 3

    dq.resize(5) # [1, 2, 4, None, None], head = 0, tail = 2

    assert dq.front() == 1
    assert dq.back() == 4
    assert dq.size() == 3

    dq.push_front(5) # [1, 2, 4, None, 5], head = 4, tail = 2

    assert dq.front() == 5
    assert dq.size() == 4