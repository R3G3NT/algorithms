from modules.circular_deque import CircularDeque

dq = CircularDeque(3, push_force=False)

print("до resize:", dq.size(), dq.empty())

dq.resize(5)

print("после resize:", dq.size(), dq.empty())