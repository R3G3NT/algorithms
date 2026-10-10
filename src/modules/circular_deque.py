class CircularDeque:
    def __init__(self, n: int, push_force: bool):
        self.__cap = n
        self.__push_force = push_force
        self.__head = 0 # индекс первого элемента в деке
        self.__tail = 0 # индекс последнего элемента в деке
        self.__size = 0 # счётчик количества элементов
        self.items = [None] * n

    def push_front(self, x: int):
        if self.__push_force == False and self.full():
            raise OverflowError("Deque is full")

        self.__head = (self.__head - 1 + self.__cap) % self.__cap
        if self.__tail == self.__head or self.size() == 0:
            self.__tail = (self.__tail - 1 + self.__cap) % self.__cap

        if self.items[self.__head] is None:
            self.__size += 1
        self.items[self.__head] = x

    def push_back(self, x: int):
        if self.__push_force == False and self.full():
            raise OverflowError("Deque is full")

        if self.size() != 0:
            self.__tail = (self.__tail + 1) % self.__cap
            if self.__tail == self.__head:
                self.__head = (self.__head + 1) % self.__cap

        if self.items[self.__tail] is None:
            self.__size += 1
        self.items[self.__tail] = x

    def pop_front(self) -> int:
        if self.empty():
            raise IndexError("Deque is empty")
        
        result = self.items[self.__head]
        self.items[self.__head] = None
        self.__head = (self.__head + 1) % self.__cap
        self.__size -= 1

        if self.empty():
            self.__head = 0
            self.__tail = 0
        return result

    def pop_back(self) -> int:
        if self.empty():
            raise IndexError("Deque is empty")
        
        result = self.items[self.__tail]
        self.items[self.__tail] = None
        self.__tail = (self.__tail - 1 + self.__cap) % self.__cap
        self.__size -= 1
        
        if self.empty():
            self.__head = 0
            self.__tail = 0
        return result

    def front(self) -> int:
        if self.empty():
            raise IndexError("Deque is empty")
        return self.items[self.__head]

    def back(self) -> int:
        if self.empty():
            raise IndexError("Deque is empty")
        return self.items[self.__tail]

    def size(self) -> int:
        return self.__size

    def empty(self) -> bool:
        return self.__size == 0

    def full(self):
        return self.__size == self.__cap

    def resize(self, new_cap: int):
        new_items = [None] * new_cap
        new_size = 0
        for i in range(new_cap):
            new_items[i] = self.items[self.__head]
            new_size += 1
            if self.__head == self.__tail:
                break
            self.__head = (self.__head + 1) % self.__cap

        self.items = new_items
        self.__cap = new_cap
        self.__size = new_size
        self.__head = 0
        self.__tail = new_size - 1