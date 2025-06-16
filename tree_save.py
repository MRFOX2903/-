import json
from avl_tree import AVLTree

class Tree_Save:
    def __init__(self, tree: AVLTree):
        self.tree = tree
        self.save_file = "avl_tree_file.json"

    def save_to_file(self):
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.pack_node(self.tree.root), f)
            return True, "Дерево сохранено!"
        except Exception as e:
            return False, f"Ошибка сохранения: {str(e)}"

    def load_from_file(self):
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
            self.tree.root = self.unpack_node(data)
            return True, "Дерево загружено!"
        except Exception as e:
            self.tree.root = None
            return False, f"Ошибка загрузки: {str(e)}"

    def pack_node(self, node):
        if not node: return None

        return {'key': node.key,
                'height': node.height,
                'left': self.pack_node(node.left),
                'right': self.pack_node(node.right)}

    def unpack_node(self, data):
        if not data: return None

        node = self.tree.Node(data['key'])
        node.height = data['height']
        node.left = self.unpack_node(data['left'])
        node.right = self.unpack_node(data['right'])
        return node