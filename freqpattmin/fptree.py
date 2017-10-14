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
        def __init__(self, children, parent, count, value):
            self.children = {}
            self.parent = parent
            self.count = count
            self.value = value
        def add(self, count):
            self.count += count
        def disp(self, ind = 1):
           # print "  " * ind, self.name, "  ",self.count
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
            #key = attibutes:value
            keyCmb = dataCol[flag]+':'+item
            if keyCmb in hdTable.keys():
                hdTable[keyCmb] += 1
            else:
                hdTable[keyCmb] = 1
            flag += 1 #flag move forward
    hdTable = {k: v for k , v in hdTable.items() if v >= support and v != {}}
    freqSet = set(hdTable.keys())
    #hdTable = sorted(hdTable.items(), key=lambda s: s[1], reverse=True)
    #return a sorted list(contain count) and a set containing frequent items(no count)       
    return hdTable, freqSet

def genTree(data, freqSet, hdTable):
    for tran in data: #loop over all tranctions
        flag = 0 #mark colomun position
        tranDict = {}
        #generate root tree
        rootTree = tree(None, None, 1, 'root')
        for item in tran:
            keyCmb = dataCol[flag]+':'+item
            if keyCmb in freqSet:
                    #depends on dataset
                    tranDict[keyCmb] = hdTable[keyCmb]
            flag += 1
        #need to sort 
        tranDict = sorted(tranDict.items(), key=lambda s: s[1], reverse=True)
        #insert each transction to the tree by a helper function
        #this part alogrithm implementation learned from open source code
        treeHelper(tranDict, hdTable, rootTree)
    return rootTree, hdTable
        
        
def treeHelper(tranDict, hdTable, rootTree):
    if tranDict[0] in rootTree.children:
        #this tranDict[1] will be 1 for this particular dataset
        #for compatible, keep it as tranDict[1]
        rootTree.children[tranDict[0]].add(tranDict[1])
    else:
        rootTree.children=tree(rootTree, None, tranDict[1], tranDict[0])
    
    while tranDict[0] != []:
        treeHelper(tranDict[1::], hdTable, rootTree.children[tranDict[0]])

        

value=2     
support = 5  
confidence = 0.7
freqItem = []
read = Init('adult.data')
adData = read.DataList()
hdTable, freqSet = genHeadTb(adData, support)
rootTree, hdTable = genTree(adData, freqSet, hdTable)

print rootTree.disp()
