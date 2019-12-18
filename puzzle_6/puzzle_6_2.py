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


def get_distances(tree, vertex):
    distances = {}
    vertex_depth = 0
    while vertex != 'COM':
        distances[vertex] = vertex_depth
        vertex_depth += 1
        vertex = tree[vertex]
    return distances


def get_first_common_vertex(tree1, tree2):
    tree2_keys = tree2.keys()
    for vertex in tree1:
        if vertex in tree2_keys:
            return vertex

tree = tree_from_input(INPUT)
you_distances = get_distances(tree, 'YOU')
san_distances = get_distances(tree, 'SAN')
common_vertex = get_first_common_vertex(you_distances, san_distances)

print(you_distances[common_vertex] + san_distances[common_vertex] - 2)