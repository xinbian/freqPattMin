#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 23:04:33 2017

@author: Xin
"""

from ete3 import Tree
t = Tree()
# We create a random tree topology
t.populate(15)
print t
print t.children
print t.get_children()
print t.up
print t.name
print t.dist
print t.is_leaf()
print t.get_tree_root()
print t.children[0].get_tree_root()
print t.children[0].children[0].get_tree_root()
# You can also iterate over tree leaves using a simple syntax
for leaf in t:
  print leaf.name