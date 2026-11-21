class Node:
    def __init__(self, key: int) -> None:
        self.key = key
        self.left = None
        self.right = None
        self.height = 0  # Высота нового узла (листа) равна 0


class AVLTree:
    def __init__(self) -> None:
        self.root = None

    # --- Вспомогательные методы ---

    def get_height(self, node: Node | None) -> int:
        if node is None:
            return -1  # Высота пустого поддерева равна -1
        return node.height

    def get_balance(self, node: Node | None) -> int:
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node: Node) -> None:
        node.height = 1 + max(
            self.get_height(node.left),
            self.get_height(node.right)
        )

    def get_min_value_node(self, node: Node) -> Node:
        current = node
        while current.left is not None:
            current = current.left
        return current

    # --- Повороты ---

    def rotate_right(self, z: Node) -> Node:
        y = z.left
        T3 = y.right

        # Выполняем поворот
        y.right = z
        z.left = T3

        # Обновляем высоты (сначала опустившемуся узлу, затем поднявшемуся)
        self.update_height(z)
        self.update_height(y)

        return y

    def rotate_left(self, z: Node) -> Node:
        y = z.right
        T2 = y.left

        # Выполняем поворот
        y.left = z
        z.right = T2

        # Обновляем высоты
        self.update_height(z)
        self.update_height(y)

        return y

    # --- Балансировка узла ---

    def rebalance(self, node: Node) -> Node:
        self.update_height(node)
        balance = self.get_balance(node)

        # Случай LL (перевес влево)
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)

        # Случай LR (зигзаг влево-вправо)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Случай RR (перевес вправо)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)

        # Случай RL (зигзаг вправо-влево)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    # --- Основные операции ---

    def insert(self, key: int) -> None:
        self.root = self.insert_node(self.root, key)

    def insert_node(self, node: Node | None, key: int) -> Node:
        if node is None:
            return Node(key)
        elif key < node.key:
            node.left = self.insert_node(node.left, key)
        elif key > node.key:
            node.right = self.insert_node(node.right, key)
        else:
            return node

        return self.rebalance(node)

    def delete(self, key: int) -> None:
        self.root = self.delete_node(self.root, key)

    def delete_node(self, node: Node | None, key: int) -> Node | None:
        if node is None:
            return node

        if key < node.key:
            node.left = self.delete_node(node.left, key)
        elif key > node.key:
            node.right = self.delete_node(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self.get_min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete_node(node.right, temp.key)

        return self.rebalance(node)

    def search(self, key: int) -> Node | None:
        return self.search_node(self.root, key)

    def search_node(self, node: Node | None, key: int) -> Node | None:
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self.search_node(node.left, key)
        return self.search_node(node.right, key)

    # --- Наглядная визуализация в консоли ---

    def print(
        self,
        node: Node | None = None,
        prefix: str = "",
        is_left: bool = True,
        is_root: bool = True
    ) -> None:
        """Выводит дерево в консоль в виде наглядной ветвистой структуры."""
        if is_root:
            node = self.root
            if node is None:
                print("<Пустое дерево>")
                return

        if node is None:
            return

        if node.right is not None:
            new_prefix = prefix + ("│   " if is_left and not is_root else "    ")
            self.print(node.right, new_prefix, False, False)

        branch = "" if is_root else ("└── " if is_left else "┌── ")
        bf = self.get_balance(node)
        print(f"{prefix}{branch}[{node.key}] (h={node.height}, BF={bf})")

        if node.left is not None:
            new_prefix = prefix + ("    " if is_left or is_root else "│   ")
            self.print(node.left, new_prefix, True, False)


# --- Пример запуска ---
if __name__ == "__main__":
    tree = AVLTree()
    for num in [1, 2, 3, 4]:
        tree.insert(num)
    tree.delete(2)

    print("Сбалансированное АВЛ-дерево:")
    tree.print()
