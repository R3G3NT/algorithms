MAX_LEAF_LEN = 8


class RopeNode:
    def __init__(
        self, text: str = None,
        left = None, right = None
    ) -> None:
        self.text = text
        self.left = left
        self.right = right
        self.weight = 0  # Длина левого поддерева (или текста, если это лист)
        self.size = 0    # Общая длина всего поддерева
        self.height = 0  # Высота узла (0 для листа, -1 для пустоты)
        self.update()

    def is_leaf(self) -> bool:
        return self.text is not None

    def update(self) -> None:
        if self.is_leaf():
            self.weight = len(self.text)
            self.size = len(self.text)
            self.height = 0
        else:
            left_size = self.left.size if self.left is not None else 0
            right_size = self.right.size if self.right is not None else 0
            left_h = self.left.height if self.left is not None else -1
            right_h = self.right.height if self.right is not None else -1

            self.weight = left_size
            self.size = left_size + right_size
            self.height = 1 + max(left_h, right_h)


class Rope:
    def __init__(self, data: str | RopeNode) -> None:
        if isinstance(data, str):
            self.root = self.build_from_string(data)
        else:
            self.root = data

    def build_from_string(self, s: str) -> RopeNode:
        if not s:
            return None
        leaves = [RopeNode(text=s[i:i + MAX_LEAF_LEN]) for i in range(0, len(s), MAX_LEAF_LEN)]

        while len(leaves) > 1:
            next_level = []
            for i in range(0, len(leaves), 2):
                if i + 1 < len(leaves):
                    next_level.append(RopeNode(left=leaves[i], right=leaves[i + 1]))
                else:
                    next_level.append(leaves[i])
            leaves = next_level

        return leaves[0]

    def get_height(self, node: RopeNode | None) -> int:
        if node is None:
            return -1
        return node.height

    def get_balance(self, node: RopeNode | None) -> int:
        if node is None or node.is_leaf():
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, z: RopeNode) -> RopeNode:
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.update()
        y.update()
        return y

    def rotate_left(self, z: RopeNode) -> RopeNode:
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.update()
        y.update()
        return y

    def rebalance(self, node: RopeNode) -> RopeNode:
        if node.is_leaf():
            return node
        node.update()
        balance = self.get_balance(node)

        # Перевес влево (LL и LR)
        if balance > 1:
            if self.get_balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Перевес вправо (RR и RL)
        if balance < -1:
            if self.get_balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def merge_nodes(self, left: RopeNode | None, right: RopeNode | None) -> RopeNode:
        if left is None:
            return right
        if right is None:
            return left

        if left.is_leaf() and right.is_leaf():
            if len(left.text) + len(right.text) <= MAX_LEAF_LEN:
                return RopeNode(text=left.text + right.text)

        lh = self.get_height(left)
        rh = self.get_height(right)

        if abs(lh - rh) <= 1:
            return RopeNode(left=left, right=right)

        if lh > rh:
            new_right = self.merge_nodes(left.right, right)
            return self.rebalance(RopeNode(left=left.left, right=new_right))
        else:
            new_left = self.merge_nodes(left, right.left)
            return self.rebalance(RopeNode(left=new_left, right=right.right))

    def split_node(self, node: RopeNode | None, idx: int) -> tuple:
        if node is None:
            return None, None
        if idx <= 0:
            return None, node
        if idx >= node.size:
            return node, None

        if node.is_leaf():
            return RopeNode(text=node.text[:idx]), RopeNode(text=node.text[idx:])

        if idx < node.weight:
            l_part, r_part = self.split_node(node.left, idx)
            return l_part, self.merge_nodes(r_part, node.right)
        elif idx > node.weight:
            l_part, r_part = self.split_node(node.right, idx - node.weight)
            return self.merge_nodes(node.left, l_part), r_part
        else:
            return node.left, node.right

    def concat(self, other):
        return Rope(self.merge_nodes(self.root, other.root))

    def split(self, i: int) -> tuple:
        left_root, right_root = self.split_node(self.root, i)
        return Rope(left_root), Rope(right_root)

    def insert(self, i: int, s: str):
        if not s:
            return Rope(self.root)
        left_rope, right_rope = self.split(i)
        mid_rope = Rope(s)
        return left_rope.concat(mid_rope).concat(right_rope)

    def delete(self, i: int, k: int):
        if k <= 0:
            return Rope(self.root)
        left_rope, temp_rope = self.split(i)
        _, right_rope = temp_rope.split(k)
        return left_rope.concat(right_rope)

    def index(self, i: int) -> str:
        curr = self.root
        while curr is not None:
            if curr.is_leaf():
                return curr.text[i]
            if i < curr.weight:
                curr = curr.left
            else:
                i -= curr.weight
                curr = curr.right
        raise IndexError("Index out of range")

    def to_string(self, node: RopeNode | None) -> str:
        if node is None:
            return ""
        if node.is_leaf():
            return node.text
        return self.to_string(node.left) + self.to_string(node.right)

    def __str__(self) -> str:
        return self.to_string(self.root)


if __name__ == "__main__":
    rope = Rope(input().rstrip("\r\n"))
    q = int(input().strip())
    print(rope)
    for _ in range(q):
        parts = input().rstrip("\r\n").split("|")
        cmd = parts[0]

        if cmd == "concat":
            s = parts[1]
            rope = rope.concat(Rope(s))
            print(rope)

        elif cmd == "split":
            i = int(parts[1])
            prefix, suffix = rope.split(i)
            print(f"{prefix}|{suffix}")

        elif cmd == "index":
            i = int(parts[1])
            print(rope.index(i))

        elif cmd == "insert":
            i = int(parts[1])
            s = parts[2]
            rope = rope.insert(i, s)
            print(rope)

        elif cmd == "delete":
            i = int(parts[1])
            k = int(parts[2])
            rope = rope.delete(i, k)
            print(rope)
