class AVLTree:
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.height = 1

    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self.insert_node(self.root, key)

    def clear(self):
        self.root = None

    def delete(self, key):
        self.root = self.delete_node(self.root, key)

    def insert_node(self, node, key):
        if not node:
            return self.Node(key)

        if key < node.key:
            node.left = self.insert_node(node.left, key)
        elif key > node.key:
            node.right = self.insert_node(node.right, key)
        else:
            return node

        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))

        return self.balance_node(node, key)

    def delete_node(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self.delete_node(node.left, key)
        elif key > node.key:
            node.right = self.delete_node(node.right, key)
        else:
            if node.left is None: return node.right
            elif node.right is None: return node.left

            temp = self.get_min_node(node.right)
            node.key = temp.key
            node.right = self.delete_node(node.right, temp.key)

        if node is None: return node

        node.height = self.update_height(node)

        return self.balance_node(node, key)

    def balance_node(self, node, key):
        if node is None:
            return node

        balance = self.get_balance(node)

        # Левый-левый случай
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # Правый-правый случай
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # Левый-правый случай
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Правый-левый случай
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def left_rotate(self, z):
        y = z.right
        T = y.left
        y.left = z
        z.right = T
        z.height = self.update_height(z)
        y.height = self.update_height(y)
        return y

    def right_rotate(self, z):
        y = z.left
        T = y.right
        y.right = z
        z.left = T
        z.height = self.update_height(z)
        y.height = self.update_height(y)
        return y

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        if not node:
            return 0

        left_height = self.get_height(node.left) if node.left else 0
        right_height = self.get_height(node.right) if node.right else 0

        return left_height - right_height

    def get_min_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current


    def update_height(self, node):
        return 1 + max(self.get_height(node.left), self.get_height(node.right))

    #даёт глубину для визуализации
    def get_depth(self, node=None):
        if node is None:
            node = self.root
        if not node:
            return 0
        left_depth = self.get_depth(node.left) if node.left else 0
        right_depth = self.get_depth(node.right) if node.right else 0
        return 1 + max(left_depth, right_depth)