from dataclasses import dataclass 
import sys
import os

INPUT = open(os.path.join(sys.path[0], 'input')).read()


@dataclass
class Node:
    id: str
    parents: []
    children: []
    depth: 0


def tree_from_input(input: str):
    edges = input.split('\n')
    tree = {}
    for edge in edges:
        parent_child = edge.split(')')
        tree[parent_child[1]] = parent_child[0]
    return tree


def sum_depths(tree):
    depths_sum = 0
    for key in tree.keys():
        key_depth = 0
        while key != 'COM':
            key_depth += 1
            key = tree[key]
        depths_sum += key_depth
    return depths_sum

tree = tree_from_input(INPUT)
print(sum_depths(tree))