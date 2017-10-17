#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:14:18 2017

@author: Xin
"""

# -*- coding: utf-8 -*-

"""Main module."""
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
                
        if data[-1] == []:
            del data[-1]
        #rewrite data form as eg. workclass:State-gov
        for tran in data: #
            flag = 0 #mark colomun position                      
            for i in range(len(tran)):
                tran[i] = dataCol[flag]+ ':'+ tran[i] 
                flag += 1
   
        adData = {}   
        for tran in data:
            #for tran in inData, add count for data :
            if frozenset(tran) in adData.keys():
                adData[frozenset(tran)] += 1
            else:
                adData[frozenset(tran)] = 1
    
        return adData
    


class tree:
        def __init__(self, parent, value, count):
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
        for item in tran: #loop over all attributes in a transaction
# =============================================================================
#             # keyCmb = dataCol[flag]+':'+item
             #key = attibutes:value, eg,  key = sex:male, value = 1          
#             #test case,not used here, 
# =============================================================================
            keyCmb = item
            if keyCmb in hdTable.keys():
                hdTable[keyCmb] += data[tran]
            else:
                hdTable[keyCmb] = data[tran]
           # flag += 1 #flag move forward
    hdTable = {k: v for k , v in hdTable.items() if v >= support and v != {}}
    
    #a pointer in head table, pointing to tree node
    for tran in hdTable.keys():
        hdTable[tran] = [hdTable[tran], None]
        
    #store frequent items in a set
    freqSet = set(hdTable.keys())
     

    
    #hdTable = sorted(hdTable.items(), key=lambda s: s[1], reverse=True)
      
    return hdTable, freqSet

def genTree(data, freqSet, hdTable):
    #generate root tree
    rootTree = tree(None, 'root', None)
    for tran in data: #loop over all tranctions
        tranDict = {}
        count = data[tran]       
        #if no frequent set, exit
        if freqSet == None:
            return None, None
        
        for item in tran:
            if item in freqSet:
                    #depends on dataset
                    tranDict[item] = hdTable[item][0]
        # sort transaction based on header table occuraence time
        # it should be noted that, should sort by value first then key, otherwise, 
        # there might be bugs. if only sort by key, 
        # eg. the two trans are
        # {'beer', 'diaper', 'ham'}, {'beer', 'ham', 'diaper', 'cookie'}
        # with header table {beer:4, diaper:4, ham:4, cookie:2}
        # this will generate a wrong FP tree, beer diaper ham are inserted in the
        # tree by differenrt order. 
        tranDict = sorted(tranDict.items(), key=lambda s: (s[1],s[0]), reverse=True)
        #insert each transction to the tree by a helper function
        #this part alogrithm implementation learned from open source code//
        
        if tranDict == []:
            return None, None
        
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
        if frozenset() in allPath.keys():
            del allPath[frozenset()]
        hdTableTemp = copy.deepcopy(hdTable)
        #to next linked item
        hdTable[item][1] = hdTable[item][1].next
    return allPath


#find freqent item function
def freqFinder(fpTree, hdTable, freqItem, suffix, support):
    #freq item in header table
    item = []
    for tran in sorted(hdTable.items(), key=lambda s: s[1]):
        item.append(tran[0])
    
    for element in item:
        prefix = copy.deepcopy(suffix)
        if prefix == '':
            prefix = element
        else:
            prefix = prefix + '&' + element
        freqItem[prefix] = hdTable[element][0]
        allPath = pathFinder(element, hdTable)
        hdTable2, freqSet = genHeadTb(allPath, support)
        condTree, hdTable2 = genTree(allPath, freqSet, hdTable2)
        if hdTable2 != None:
            freqFinder(condTree, hdTable2, freqItem, prefix, support)
    
    # ======================================================================
    # change frequent item set structre, for mining association rules.
    # put them in a list of dictionary,
    # the same lenth item set has the the same index in the list
    # ======================================================================
    #find maximum set length fist
    freqList = []
    maxLen = 0
    for item in freqItem.keys():
         maxLen = max(maxLen, len(item.split('&')))
    #inilize frequent item set 'list'
    freqList = [None] * maxLen

    for k, v in freqItem.items():
        #assign frequent item set differnt index based its(key) length
        setLen = len(k.split('&')) - 1
        if freqList[setLen] == None:
             freqList[setLen] = {k: v}
        else:
             freqList[setLen][k] = v
    return freqList

start_time = time.time()

value=2     
support = 5
confidence = 0.7
freqItem = []
read = Init('adult.data')
adData = read.DataList()
 
#first scan: generate header table
hdTable, freqSet = genHeadTb(adData, support)
#second scan: genereate FP tree
rootTree, hdTable = genTree(adData, freqSet, hdTable)

print rootTree.disp()

#ming FP tree, find frequent items 
freqItem = freqFinder(rootTree, hdTable, {}, '', support)

APelapsed_time = time.time() - start_time



# =============================================================================
# some test data


#adData = {}

#for tran in inData:
#    if frozenset(tran) in adData.keys():
#        adData[frozenset(tran)] += 1
#    else:
#        adData[frozenset(tran)] = 1
# inData=[['r', 'z', 'h', 'j', 'p'],
#                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
#                ['z'],
#                ['r', 'x', 'n', 'o', 's'],
#                ['y', 'r', 'x', 'z', 'q', 't', 'p'],
#                ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
# 
# inData=[['1', '2', '5'],
#               ['2','4'],
#                ['2','3'],
#                ['1', '2', '4'],
#                ['1', '3'],
#                ['2', '3'],
#                ['1','3'],
#                ['1','2','3','5'],
#                ['1','2','3']]
# inData = [['cola', 'egg', 'ham'],['cola','diaper','beer'],['cola','diaper','beer','ham'],['diaper','beer']]
# 
# =============================================================================

