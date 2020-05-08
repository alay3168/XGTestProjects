#!/usr/bin/env python
# -*- coding: utf-8 -*-

def binary_tree(r):
    return [r, [], []]
def insert_left(root, new_branch):
    t = root.pop(1)   # The left child position
    if len(t) > 1:   # if not empty
        # The origin left child turn to be the left child of new_branch
        root.insert(1, [new_branch, t, []])
    else:
        root.insert(1, [new_branch, [], []])
    return root
def insert_right(root, new_branch):
    t = root.pop(2)
    if len(t) > 1:
        root.insert(2, [new_branch, [], t])
    else:
        root.insert(2, [new_branch, [], []])
    return root
def get_root_val(root):
    return root[0]
def set_root_val(root, new_val):
    root[0] = new_val
def get_left_child(root):
    return root[1]
def get_right_child(root):
    return root[2]

x = binary_tree('a')
print(x)
insert_left(x,'b')
print(x)
insert_right(x,'c')
insert_right(get_right_child(x), 'd')  # important!
insert_left(get_right_child(get_right_child(x)), 'e')
print(x)