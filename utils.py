def is_empty(node):
    return (not node) or node.val is None


def is_leaf(node):
    return (not node.left) and (not node.right)


def is_two_child_node(node):
    return node.left and node.right


def one_child_node(node):
    if node.right:
        return node.right
    else:
        return node.left


def get_minimum(node):
    pre_node = node

    while not is_empty(node):
        pre_node = node
        node = node.left

    return pre_node


def get_maximum(node):
    pre_node = node

    while not is_empty(node):
        pre_node = node
        node = node.right

    return pre_node
