# Класс ошибок операций над декой
class DequeOperationError(Exception):
    pass

class CircularDeque:
    def __init__(self, n: int, push_force: bool):
        self.n = n
        self.push_force = push_force
        self.items = [None] * n
        self.head = 0 # индекс первого элемента в деке
        self.tail = 0 # индекс последнего элемента в деке
        self.cap = 0  # размер деки

    def push_front(self, x: int):
        if self.push_force == False and self.full():
            raise DequeOperationError("Кольцевая дека заполнена!")

        self.head = (self.head - 1 + self.n) % self.n
        if self.tail == self.head:
            self.tail = (self.tail - 1 + self.n) % self.n

        if self.items[self.head] is None:
            self.cap += 1
        self.items[self.head] = x

    def push_back(self, x: int):
        if self.push_force == False and self.full():
            raise DequeOperationError("Кольцевая дека заполнена!")

        if self.cap != 0:
            self.tail = (self.tail + 1) % self.n
            if self.tail == self.head:
                self.head = (self.head + 1) % self.n

        if self.items[self.tail] is None:
            self.cap += 1
        self.items[self.tail] = x

    def pop_front(self) -> int:
        if self.empty():
            raise DequeOperationError("Кольцевая дека пуста")
        result = self.items[self.head]
        self.items[self.head] = None
        self.head = (self.head + 1) % self.n
        self.cap -= 1
        return result

    def pop_back(self) -> int:
        if self.empty():
            raise DequeOperationError("Кольцевая дека пуста")
        result = self.items[self.tail]
        self.items[self.tail] = None
        self.tail = (self.tail - 1 + self.n) % self.n
        self.cap -= 1
        return result

    def front(self) -> int:
        if self.empty():
            raise DequeOperationError("Кольцевая дека пуста!")
        return self.items[self.head]

    def back(self) -> int:
        if self.empty():
            raise DequeOperationError("Кольцевая дека пуста!")
        return self.items[self.tail]

    def size(self) -> int:
        return self.cap

    def empty(self) -> bool:
        return self.cap == 0

    def full(self):
        return self.cap == self.n

    def resize(self, new_cap: int):
        pass