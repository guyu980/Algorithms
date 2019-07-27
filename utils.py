from graphs import *
from random import random
from random import choice


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


def random_graph(n, p, wts=[1]):
    G = WeightedGraph()
    V = [WeightedVertex(i) for i in range(n)]

    for v in V:
        G.add_vertex(v)

    for v in V:
        for w in V:
            if v != w:
                if random() < p:
                    G.add_weighted_dir_edge(v, w, wt=choice(wts))

    return G






