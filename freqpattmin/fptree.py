#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:14:18 2017

@author: Xin
"""

# -*- coding: utf-8 -*-

"""Main module."""
import numpy as np
import pandas as pd
import csv
import time
import copy

#initialization class
class Init:
    def __init__(self, filename):
        self.filename = filename
    #read as pandas data frame
    def DataPD(self):
        data = pd.read_csv(self.filename, sep = ',', na_values = ".", header=None)
        data.columns = (["age", "workclass", "fnlwgt", "education", "education-num", "martial-status",
		"occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
        	"hours-per-week", "country", "target"]) 
        return data
    #read as list
    def DataList(self):
        data = []
        with open(self.filename, 'r') as f:
            for row in csv.reader(f):
                row = [col.strip() for col in row]
                data.append(row)
        return data
   # def DataClean(self):
    
		

read = Init('adult.data')
adData = read.DataList()

class tree:
        def __init__(self, parent, value, count = 1):
            self.children = {}
            #node parent
            self.parent = parent
            #node name
            self.value = value
            #
            self.count = count
            #linked list
            self.next = None
        def add(self, count):
            self.count += count
            
        def disp(self, ind = 1):
            print "  " * ind, self.value, "  ",self.count
            for child in self.children.values():
                child.disp(ind + 1)
        
    

dataCol = ["age", "workclass", "fnlwgt", "education", "education-num", "martial-status",
		"occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
    	"hours-per-week", "country", "target"]
  
    
def genHeadTb(data, support):
    hdTable = {}
    for tran in data: #loop over all tranctions
        flag = 0 #mark colomun position
        for item in tran: #loop over all attributes in a transaction
            #key = attibutes:value, eg,  key = sex:male, value = 1
            #for test
            #keyCmb = dataCol[flag]+':'+item
            keyCmb = item
            if keyCmb in hdTable.keys():
                hdTable[keyCmb] += data[tran]
            else:
                hdTable[keyCmb] = data[tran]
            flag += 1 #flag move forward
    hdTable = {k: v for k , v in hdTable.items() if v >= support and v != {}}
 
    #a pointer in head table, pointing to tree node
    for tran in hdTable.keys():
        hdTable[tran] = [hdTable[tran], None]
        
    #store frequent items in a set
    freqSet = set(hdTable.keys())
     
    if len(freqSet) == 0:
        return None, None
    
    #hdTable = sorted(hdTable.items(), key=lambda s: s[1], reverse=True)
      
    return hdTable, freqSet

def genTree(data, freqSet, hdTable):
    #generate root tree
    rootTree = tree(None, 'root')
    for tran in data: #loop over all tranctions
        flag = 0 #mark colomun position
        tranDict = {}
        count = data[tran]
        for item in tran:
            #for test
            #keyCmb = dataCol[flag]+':'+item
            keyCmb = item
            if keyCmb in freqSet:
                    #depends on dataset
                    tranDict[keyCmb] = hdTable[keyCmb][0]
            flag += 1
        #need to sort 
        tranDict = sorted(tranDict.items(), key=lambda s: s[1], reverse=True)
        #insert each transction to the tree by a helper function
        #this part alogrithm implementation learned from open source code//
        treeHelper(tranDict, hdTable, rootTree, count)
    return rootTree, hdTable
        
        
def treeHelper(tranDict, hdTable, rootTree, count):
    #if node already exists, add 1 to count
    if tranDict[0][0] in rootTree.children:
        rootTree.children[tranDict[0][0]].add(count)
    #if node is not a child of the parent tree, create a node as its child
    else:
        rootTree.children[tranDict[0][0]]=tree(rootTree, tranDict[0][0],count) 
        
        #use head table pointer to create linked list in tree node
        if hdTable[tranDict[0][0]][1] == None:
            hdTable[tranDict[0][0]][1] = rootTree.children[tranDict[0][0]]
        else:
            updateHeader(hdTable[tranDict[0][0]][1], rootTree.children[tranDict[0][0]])
           # while hdTable[tranDict[0][0]][1] != None:
           #      hdTable[tranDict[0][0]][1] = hdTable[tranDict[0][0]][1].next
           # hdTable[tranDict[0][0]][1] = rootTree.children[tranDict[0][0]]
    #process remianing items
    if len(tranDict) > 1 :  
        treeHelper(tranDict[1::], hdTable, rootTree.children[tranDict[0][0]], count)

def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.next != None):
        nodeToTest = nodeToTest.next
    nodeToTest.next = targetNode    

#find conditional path
def pathFinder(item, hdTable):
    #store all pathes in a dict
    allPath = {}
    print hdTable[item]
    while hdTable[item][1] != None:
        hdTableTemp = copy.deepcopy(hdTable)
        path = []
        count = hdTableTemp[item][1].count
        
        while hdTableTemp[item][1].parent.value != 'root':
            path.append(hdTableTemp[item][1].parent.value)
            hdTableTemp[item][1] = hdTableTemp[item][1].parent
        #add path to all path
        #reverse path
        allPath[frozenset(path)] = count
        hdTableTemp = copy.deepcopy(hdTable)
        #to next linked item
        hdTable[item][1] = hdTable[item][1].next
    return allPath


value=2     
support = 3  
confidence = 0.7
freqItem = []
read = Init('adult.data')


adData = read.DataList()


inData=[['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]

adData = {}
for tran in inData:
    adData[frozenset(tran)] = 1
    
hdTable, freqSet = genHeadTb(adData, support)
#FPtree genereate
rootTree, hdTable = genTree(adData, freqSet, hdTable)

print rootTree.disp()
# =============================================================================
# allPath=pathFinder('t', hdTable)
# hdTable2, freqSet2 = genHeadTb(allPath, support)
# myTree2, hdTable2 = genTree(allPath, freqSet2, hdTable2)
# print myTree2.disp()
# =============================================================================


freqItem = []
path = set([])


def freqFinder(fpTree, hdTable, freqItem, path, support):
    #freq item in header table in reversed order
    item = []
    for trans in sorted(hdTable.items(), key=lambda s: s[1]):
        item.append(trans[0])
    
    for element in item:
        pathInc = copy.deepcopy(path)
        pathInc.add(element)
        freqItem.append(pathInc)
        allPath = pathFinder(element, hdTable)
        hdTable2, freqSet = genHeadTb(allPath, support)
        condTree, hdTable2 = genTree(allPath, freqSet, hdTable2)
        if hdTable2 != {}:
            print 'conditional tree for:', freqItem
            condTree.disp()
            freqFinder(condTree, hdTable2, freqItem, pathInc, support)
            
freqFinder(rootTree, hdTable, freqItem, path, support)
