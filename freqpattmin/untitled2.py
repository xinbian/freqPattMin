#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 14:30:19 2017

@author: Xin
"""

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
 
    def inc(self, numOccur):
        self.count += numOccur
 
    def disp(self, ind=1):
        print ' ' * ind, self.name, ' ', self.count
        for child in self.children.values():
            child.disp(ind + 1)
rootNode = treeNode('pyramid', 9, None)
rootNode.children['eye'] = treeNode('eye', 13, None)
rootNode.children['phoenix'] = treeNode('phoenix', 3, None)
rootNode.disp()


dataSet = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]

headerTable = {}
for trans in dataSet:
    for item in trans:
        headerTable[item] = headerTable.get(item, 0) + dataSet[trans]