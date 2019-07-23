from utils import *
from nodes import *


class Tree:
    def __init__(self, root=None):
        self.root = root

    def add(self, item):
        node = Node(item)

        if is_empty(self.root):
            self.root = node
        else:
            my_stack = [self.root]

            while True:
                cur_node = my_stack.pop(0)

                if is_empty(cur_node):
                    continue

                if not cur_node.left:
                    cur_node.left = node
                    return
                elif not cur_node.right:
                    cur_node.right = node
                    return
                else:
                    my_stack.append(cur_node.left)
                    my_stack.append(cur_node.right)

    def add_list(self, items):
        for item in items:
            self.add(item)

    def layer_order_tree_walk(self):
        my_stack = [self.root]
        ret = []

        while my_stack:
            node = my_stack.pop(0)
            ret.append(node.val)

            if not is_empty(node.left):
                my_stack.append(node.left)

            if not is_empty(node.right):
                my_stack.append(node.right)

        return ret

    def inorder_tree_walk(self):
        if is_empty(self.root):
            return []

        ret = []

        def loop(node):
            if is_empty(node):
                return

            loop(node.left)
            ret.append(node.val)
            loop(node.right)

        loop(self.root)

        return ret

    def preorder_tree_walk(self):
        if is_empty(self.root):
            return []

        ret = []

        def loop(node):
            if is_empty(node):
                return

            ret.append(node.val)
            loop(node.left)
            loop(node.right)

        loop(self.root)

        return ret

    def postorder_tree_walk(self):
        if is_empty(self.root):
            return []

        ret = []

        def loop(node):
            if is_empty(node):
                return

            loop(node.left)
            loop(node.right)
            ret.append(node.val)

        loop(self.root)

        return ret

    def inorder_tree_walk_stack(self):
        node = self.root

        if is_empty(node):
            return []

        my_stack, ret = [], []

        while not is_empty(node) or my_stack:
            while not is_empty(node):
                my_stack.append(node)
                node = node.left

            node = my_stack.pop()
            ret.append(node.val)
            node = node.right

        return ret

    def preorder_tree_walk_stack(self):
        node = self.root

        if is_empty(node):
            return []

        my_stack, ret = [], []

        while not is_empty(node) or my_stack:
            while not is_empty(node):
                ret.append(node.val)
                my_stack.append(node)
                node = node.left

            node = my_stack.pop()
            node = node.right

        return ret

    def postorder_tree_walk_stack(self):
        node = self.root

        if is_empty(node):
            return []

        my_stack, ret = [], []
        my_stack.append(node)

        while my_stack:
            node = my_stack.pop()

            if not is_empty(node.left):
                my_stack.append(node.left)

            if not is_empty(node.right):
                my_stack.append(node.right)

            ret.append(node.val)

        return ret[::-1]

    def is_valid_tree(self):
        inorder = self.inorder_tree_walk_stack()

        for i in range(len(inorder) - 1):
            if inorder[i] > inorder[i + 1]:
                print('     This is not a valid tree!')
                return False

        print('     This is a valid tree!')
        return True

    def get_successor(self, item):
        inorder = self.inorder_tree_walk_stack()
        item = inorder[inorder.index(item) + 1]
        return self.search(item)

    def get_predecessor(self, item):
        inorder = self.inorder_tree_walk_stack()
        item = inorder[inorder.index(item) - 1]
        return self.search(item)

    def search(self, item):
        node = self.root

        if is_empty(node):
            return Node()

        while not is_empty(node) and item != node.val:
            if item < node.val:
                node = node.left
            else:
                node = node.right

        return node

    def insert(self, item):
        node = self.root
        pre_node = None

        if is_empty(node):
            self.root = Node(item)
            return

        while not is_empty(node) and item != node.val:
            pre_node = node

            if item < node.val:
                node = node.left
            else:
                node = node.right

        if not is_empty(node):
            print('     %d is in the tree!' % item)
        elif item < pre_node.val:
            pre_node.left = Node(item)
        else:
            pre_node.right = Node(item)

    def delete(self, item):
        node = self.root
        pre_node = None

        if is_empty(node):
            self.root = Node(item)
            return

        while not is_empty(node) and item != node.val:
            pre_node = node

            if item < node.val:
                node = node.left
            else:
                node = node.right

        if is_empty(node):
            print('     %d is not in the tree!' % item)
        elif is_leaf(node):
            if item < pre_node.val:
                pre_node.left = None
            else:
                pre_node.right = None
        elif is_two_child_node(node):
            pre_node = self.get_successor(node.val)
            val = pre_node.val
            self.delete(val)
            node.val = val
        else:
            if item < pre_node.val:
                pre_node.left = one_child_node(node)
            else:
                pre_node.right = one_child_node(node)


class BSTree(Tree):
    def __init__(self, root=None):
        super().__init__()
        self.root = root

    def add(self, item):
        node = BSNode(item)

        if is_empty(self.root):
            self.root = node
        else:
            my_stack = [self.root]

            while True:
                cur_node = my_stack.pop(0)

                if is_empty(cur_node):
                    continue

                if not cur_node.left:
                    cur_node.left = node
                    node.parent = cur_node
                    return
                elif not cur_node.right:
                    cur_node.right = node
                    node.parent = cur_node
                    return
                else:
                    my_stack.append(cur_node.left)
                    my_stack.append(cur_node.right)

    def search(self, item):
        node = self.root

        if is_empty(node):
            return BSNode()

        while not is_empty(node) and item != node.val:
            if item < node.val:
                node = node.left
            else:
                node = node.right

        return node

    def insert(self, item):
        node = self.root

        if is_empty(node):
            self.root = BSNode(item)
            return

        while not is_empty(node) and item != node.val:
            if item < node.val:
                node = node.left
            else:
                node = node.right

        if not is_empty(node):
            print('     %d is in the tree!' % item)
        elif item < node.parent.val:
            node.parent.left = BSNode(item)
        else:
            node.parent.right = BSNode(item)

    def delete(self, item):
        node = self.search(item)

        if is_empty(node):
            print('     %d is not in the tree!' % item)
        elif is_leaf(node):
            if item < node.parent.val:
                node.parent.left = None
            else:
                node.parent.right = None
        elif is_two_child_node(node):
                pre_node = self.get_successor(node.val)
                val = pre_node.val
                self.delete(val)
                node.val = val
        else:
            if item < node.parent.val:
                node.parent.left = one_child_node(node)
            else:
                node.parent.right = one_child_node(node)

    def get_successor(self, item):
        node = self.search(item)

        if is_empty(node):
            print('     %d is not in the tree!' % item)
            return BSNode()
        elif not is_empty(node.right):
            return get_minimum(node.right)
        else:
            parent = node.parent

            while not is_empty(parent) and node.val == parent.right.val:
                node = parent
                parent = parent.parent

        return parent

    def get_predecessor(self, item):
        node = self.search(item)

        if is_empty(node):
            print('     %d is not in the tree!' % item)
            return BSNode()
        elif not is_empty(node.left):
            return get_maximum(node.left)
        else:
            parent = node.parent

            while not is_empty(parent) and node.val == parent.left.val:
                node = parent
                parent = parent.parent

        return parent


class RBTree(BSTree):
    def __init__(self, root=None):
        super().__init__()
        self.root = root


if __name__ == '__main__':
    print('=============== Example of Binary Search Tree ==============')

    items = [5, 3, 7, 2, 4, None, 8, 1]
    print('     - Input:\n          ', str(items))

    tree = BSTree()
    tree.add_list(items)
    print('     - Successor of 2 is: %d' % tree.get_successor(2).val)
    print('     - Predecessor of 7 is: %d' % tree.get_predecessor(7).val)

    print('     - Layer Order Tree Walk:\n          ', str(tree.layer_order_tree_walk()))
    print('     - Post Order Tree Walk:\n          ', str(tree.postorder_tree_walk_stack()))
    print('     - Pre Order Tree Walk:\n          ', str(tree.preorder_tree_walk_stack()))
    print('     - In Order Tree Walk:\n          ', str(tree.inorder_tree_walk_stack()))

    tree.insert(6)
    print('     - In Order Tree Walk after inserting 6:\n          ',
          str(tree.inorder_tree_walk_stack()))

    tree.delete(3)
    print('     - In Order Tree Walk after deleting 3:\n          ',
          str(tree.inorder_tree_walk_stack()))
    print('============================================================\n')
