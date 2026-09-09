# Класс ошибок операций над декой
class DequeOperationError(Exception):
    pass

class CircularDeque:
    def __init__(self, n: int, push_force: bool):
        self.n = n
        self.push_force = push_force
        self.deque = [0] * n
        self.begin = 0 # указатель на первый элемент в деке
        self.end = 0   # указатель на последний элемент в деке
        self.size_of_deque = 0

    def push_front(self, x: int):
        pass

    def push_back(self, x: int):
        pass

    def pop_front(self) -> int:
        pass

    def pop_back(self) -> int:
        pass

    def front(self) -> int:
        return self.deque[self.begin]

    def back(self) -> int:
        return self.deque[self.end]

    def size(self) -> int:
        return self.size_of_deque

    def empty(self) -> bool:
        return self.size_of_deque == 0

    def full(self):
        return self.size_of_deque == self.n

    def resize(self, new_cap: int):
        pass