class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None
        self.abierta = True

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3

        z.height = 1 + (self.get_height(z.left) if self.get_height(z.left) > self.get_height(z.right) else self.get_height(z.right))
        y.height = 1 + (self.get_height(y.left) if self.get_height(y.left) > self.get_height(y.right) else self.get_height(y.right))
        return y

    def rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2

        z.height = 1 + (self.get_height(z.left) if self.get_height(z.left) > self.get_height(z.right) else self.get_height(z.right))
        y.height = 1 + (self.get_height(y.left) if self.get_height(y.left) > self.get_height(y.right) else self.get_height(y.right))
        return y

    def insert(self, root, key):
        if not root:
            return AVLNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root

        root.height = 1 + (self.get_height(root.left) if self.get_height(root.left) > self.get_height(root.right) else self.get_height(root.right))
        balance = self.get_balance(root)

        # Casos de desbalanceo
        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def find(self, root, key):
        if not root or root.key == key:
            return root
        if key < root.key:
            return self.find(root.left, key)
        return self.find(root.right, key)

    def get_prefix(self, root, prefix, results):
        if not root:
            return
        if root.key >= prefix:
            self.get_prefix(root.left, prefix, results)
            if root.key.startswith(prefix) and root.abierta:
                results.append(root.key)
            self.get_prefix(root.right, prefix, results)
        else:
            self.get_prefix(root.right, prefix, results)

    def get_range(self, root, start, end, results):
        if not root:
            return
        if root.key > start:
            self.get_range(root.left, start, end, results)
            if start <= root.key <= end and root.abierta:
                results.append(root.key)
        if root.key < end:
            self.get_range(root.right, start, end, results)
