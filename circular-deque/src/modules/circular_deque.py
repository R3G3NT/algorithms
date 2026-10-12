class CircularDeque:
    def __init__(self, n: int, push_force: bool):
        if n <= 0:
            raise ValueError("Deque capacity must be greater than 0")
        self.cap = n
        self.push_force = push_force
        self.head = 0 # индекс первого элемента в деке
        self.tail = 0 # индекс последнего элемента в деке
        self.item_count = 0 # счётчик количества элементов
        self.items = [None] * n

    def push_front(self, x: int):
        if self.push_force == False and self.full():
            raise OverflowError("Deque is full")

        self.head = (self.head - 1 + self.cap) % self.cap
        if self.tail == self.head or self.size() == 0:
            self.tail = (self.tail - 1 + self.cap) % self.cap

        if self.items[self.head] is None:
            self.item_count += 1
        self.items[self.head] = x

    def push_back(self, x: int):
        if self.push_force == False and self.full():
            raise OverflowError("Deque is full")

        if self.size() != 0:
            self.tail = (self.tail + 1) % self.cap
            if self.tail == self.head:
                self.head = (self.head + 1) % self.cap

        if self.items[self.tail] is None:
            self.item_count += 1
        self.items[self.tail] = x

    def pop_front(self) -> int:
        if self.empty():
            raise IndexError("Deque is empty")

        result = self.items[self.head]
        self.items[self.head] = None
        self.head = (self.head + 1) % self.cap
        self.item_count -= 1

        if self.empty():
            self.head = 0
            self.tail = 0
        return result

    def pop_back(self) -> int:
        if self.empty():
            raise IndexError("Deque is empty")

        result = self.items[self.tail]
        self.items[self.tail] = None
        self.tail = (self.tail - 1 + self.cap) % self.cap
        self.item_count -= 1

        if self.empty():
            self.head = 0
            self.tail = 0
        return result

    def front(self) -> int:
        if self.empty():
            raise IndexError("Deque is empty")
        return self.items[self.head]

    def back(self) -> int:
        if self.empty():
            raise IndexError("Deque is empty")
        return self.items[self.tail]

    def size(self) -> int:
        return self.item_count

    def empty(self) -> bool:
        return self.item_count == 0

    def full(self):
        return self.item_count == self.cap

    def resize(self, new_cap: int):
        if new_cap <= 0:
            raise ValueError("Deque capacity must be greater than 0")

        if self.empty():
            self.items = [None] * new_cap
            self.cap = new_cap
            self.head = 0
            self.tail = 0
            self.item_count = 0
            return

        new_items = [None] * new_cap
        new_size = 0
        for i in range(new_cap):
            new_items[i] = self.items[self.head]
            new_size += 1
            if self.head == self.tail:
                break
            self.head = (self.head + 1) % self.cap

        self.items = new_items
        self.cap = new_cap
        self.item_count = new_size
        self.head = 0
        self.tail = new_size - 1