#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 15:14:18 2017

@author: Xin
"""

# -*- coding: utf-8 -*-

"""Main module."""
import csv
import time
import copy

#initialization class
class Init:
    def __init__(self, filename):
        self.filename = filename
  
    #read as list
    def DataList(self):
        data = []
        with open(self.filename, 'r') as f:
            for row in csv.reader(f):
                row = [col.strip() for col in row]
                data.append(row)
                
        if data[-1] == []:
            del data[-1]
        #rewrite data form as, eg., workclass:State-gov
        for tran in data: #
            flag = 0 #mark colomun position                      
            for i in range(len(tran)):
                tran[i] = dataCol[flag]+ ':'+ tran[i] 
                flag += 1
   
        adData = {}   
        for tran in data:
            #for tran in inData, add frequenct/count/number for data :
            if frozenset(tran) in adData.keys():
                adData[frozenset(tran)] += 1
            else:
                adData[frozenset(tran)] = 1
    
        return adData
    

class tree:
        def __init__(self, parent, title, num):
            #a dictionary containing node child
            #key is child's title, calue is child node tree
            self.child = {}
            #node parent
            self.parent = parent
            #node value
            self.title = title
            #node frequency
            self.num = num
            #linked list for same item
            self.next = None
        def add(self, num):
            self.num += num
          

dataCol = ["age", "workclass", "fnlwgt", "education", "education-num", "martial-status",
		"occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
    	"hours-per-week", "country", "target"]
  
    
def genHeadTb(data, support):
    hdTable = {}
    for tran in data: #loop over all tranctions
        for item in tran: #loop over all attributes in a transaction
            if item in hdTable.keys():
                hdTable[item] += data[tran]
            else:
                hdTable[item] = data[tran]
    hdTable = {k: v for k , v in hdTable.items() if v >= support and v != {}}
   
    #a pointer in head table, pointing to tree node
    for tran in hdTable.keys():
        hdTable[tran] = [hdTable[tran], None]        
    #store frequent items in a set
    freqSet = set(hdTable.keys())
    #if no frequent set, exit
    if freqSet == None:
        return None, None
    #hdTable = sorted(hdTable.items(), key=lambda s: s[1], reverse=True)
      
    return hdTable, freqSet

def genTree(data, freqSet, hdTable):
    
    #generate root tree
    rootTree = tree(None, 'root', None)

    for tran in data: #loop over all tranctions
        tranDict = {}
        num = data[tran]   
                
        for item in tran:
            if item in freqSet:
                    #depends on dataset
                    tranDict[item] = hdTable[item][0]
        # sort transaction based on header table occuraence time
        # note that, it should be sorted by value first then key, otherwise, 
        # there might be bugs. if only sorted by key, eg. the two trans are
        # {'beer', 'diaper', 'ham'}, {'beer', 'ham', 'diaper', 'cookie'}
        # with header table {beer:4, diaper:4, ham:4, cookie:2}
        # this might generate a wrong FP tree, beer diaper ham might beinserted in the
        # tree by differenrt order. 
        #tranDict is a sorted list now rather than dict
        tranDict = sorted(tranDict.items(), key=lambda s: (s[1],s[0]), reverse=True)
        
        # if this tranaction doesn't contain any frequent item, no need to build tree
        if tranDict == []:
            return None, None
        
        #build tree recursively
        #insert each transction to the tree by a helper function
        treeHelper(tranDict, hdTable, rootTree, num)
        
    return rootTree, hdTable
        
        
def treeHelper(tranDict, hdTable, rootTree, num):
    #if node already exists, add how many times it shows: num
    #tranDict[0][0] corresponds to previous key, 
    #while tranDict[0][1] is num in header table, useless
    #for simplicity, use item as node's title
    item = tranDict[0][0]
    if item in rootTree.child:
        rootTree.child[item].add(num)
    #if node is not a child of the parent tree, create a node as current node's child
    else:
        rootTree.child[item]=tree(rootTree, item, num)    
        
        #hdTable[item][1] always points to the first shown node of the same item
        #use head table pointer to create linked list in simmilar tree nodes
        if hdTable[item][1] == None:
            #point to the fist show shown node
            hdTable[item][1] = rootTree.child[item]
        else:
            #store original hdTable pointer in temp
            temp = hdTable[item][1]
            #find the last tree node in linked list (containing same item), 
            #and point that tree node to the lastest tree node
            while hdTable[item][1].next != None:              
                 hdTable[item][1] = hdTable[item][1].next
            #if hdTable[item][1].next == None, the current last element in linked list is found
            hdTable[item][1].next = rootTree.child[item]
            #restore hdTable
            hdTable[item][1] = temp
    #process remianing items
    if len(tranDict) > 1 :  
        treeHelper(tranDict[1::], hdTable, rootTree.child[item], num)


#find conditional tree and path
def pathFinder(item, hdTable):
    #store all paths in a dict, frozenset(path) as key, number as value
    allPath = {}
    while hdTable[item][1] != None:
        # keep orgingal hdTable untouched for each call of the function
        hdTableTemp = copy.deepcopy(hdTable)
        path = []
        #the conditional path support
        num = hdTableTemp[item][1].num
        
        #down - top serach
        #loop until reach root node
        while hdTableTemp[item][1].parent.title != 'root':
            #add path 
            path.append(hdTableTemp[item][1].parent.title)
            #to current node's parent
            hdTableTemp[item][1] = hdTableTemp[item][1].parent
            
        #add path to all path
        allPath[frozenset(path)] = num
        
        #delete unnesccessary files
        if frozenset() in allPath.keys():
            del allPath[frozenset()]
                  
        #to next linked item to find another path
        hdTable[item][1] = hdTable[item][1].next
    return allPath


#find freqent item
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
    # change frequent item set structre, for convenience of mining association rules.
    # put them in a list of dictionary,
    # the same lenth item set has the the same index in the list
    # ======================================================================
    #find maximum frequent item set length fist
    freqList = []
    maxLen = 0
    for item in freqItem.keys():
         maxLen = max(maxLen, len(item.split('&')))
    #inilize frequent item set 'list'
    freqList = [None] * maxLen

    for k, v in freqItem.items():
        #assign frequent item set differnt index based its key length
        #key length
        setLen = len(k.split('&')) - 1
        tempKey = k.split('&')
        tempKey ='&'.join(sorted(tempKey))
        #put the same length frequent item sets in the same position in freqList
        if freqList[setLen] == None:
             freqList[setLen] = {tempKey: v}
        else:
             freqList[setLen][tempKey] = v
    return freqList

start_time = time.time()

read = Init('adult.data')
adData = read.DataList()
value=2  
minSup = 0.6  
#calculate absoulte support  
support = minSup * len(adData)
confidence = 0.7
freqItem = []

 
#first scan: generate header table
hdTable, freqSet = genHeadTb(adData, support)
#second scan: genereate FP tree
rootTree, hdTable = genTree(adData, freqSet, hdTable)

#ming FP tree, find frequent items 
freqItem = freqFinder(rootTree, hdTable, {}, '', support)

APelapsed_time = time.time() - start_time
