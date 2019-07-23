class Node:
    def __init__(self, x=None, left=None, right=None):
        self.val = x
        self.left = left
        self.right = right


class BSNode(Node):
    def __init__(self, x=None, left=None, right=None, parent=None):
        super(BSNode, self).__init__(x, left, right)
        self.parent = parent


class RBNode(BSNode):
    def __init__(self, x=None, left=None, right=None, parent=None, color='Black'):
        super(RBNode, self).__init__(x, left, right, parent)
        self.color = color

