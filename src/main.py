from modules.circular_deque import CircularDeque

cd = CircularDeque(5, True)
cd.push_front(1)
assert cd.front() == cd.back()
print(cd.front())