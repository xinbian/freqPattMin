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
import json
import itertools

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
        for tran in data: #
            flag = 0 #mark colomun position                      
            for i in range(len(tran)):
                #data cleaning: 
                #1. partitioning age data
                #2. there are missing data in this dataset, which is already denoted by '?'
                #since total missing data is very few, '?' won't form frequent items.
                #we can still use this method: global constant to fill in the missing value
                if i == 0:
                    try:
                        if int(tran[0]) <= 20:
                            tran[0] = 'young'
                        elif int(tran[0]) <= 45 and int(tran[0]) > 20:
                            tran[0] = 'mid-age'            
                        elif int(tran[0]) > 45:
                            tran[0] = 'elder'
                    except ValueError:
                        print  'miss data or invalid data'
                #rewrite data form as, eg., workclass:State-gov
                tran[i] = dataCol[flag]+ ':'+ tran[i] 
                flag += 1
            
   
        adData = {}   
        for tran in data:
            #for tran in inData, add frequency/count/number for data :
            if frozenset(tran) in adData.keys():
                adData[frozenset(tran)] += 1
            else:
                adData[frozenset(tran)] = 1
    
        return adData
    

class tree:
        def __init__(self, parent, title, num):
            #a dictionary containing node child
            #key is child's title, value is child node tree
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
    for tran in data: #loop over all transactions
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

    return hdTable, freqSet

def genTree(data, freqSet, hdTable):
    
    #generate root tree
    rootTree = tree(None, 'root', None)

    for tran in data: #loop over all transactions
        tranDict = {}
        num = data[tran]   
                
        for item in tran:
            if item in freqSet:
                    #depends on dataset
                    tranDict[item] = hdTable[item][0]
        # sort transaction based on header table occurrence time
        # note that, it should be sorted by value first then key, otherwise, 
        # there might be bugs. if only sorted by key, eg. the two trans are
        # {'beer', 'diaper', 'ham'}, {'beer', 'ham', 'diaper', 'cookie'}
        # with header table {beer:4, diaper:4, ham:4, cookie:2}
        # this might generate a wrong FP tree, beer diaper ham might be inserted in the
        # tree by different order. 
        #tranDict is a sorted list now rather than dict
        tranDict = sorted(tranDict.items(), key=lambda s: (s[1],s[0]), reverse=True)
        
        # if this tranaction doesn't contain any frequent item, no need to build tree
        if tranDict == []:
            return None, None
        
        #build tree recursively
        #insert each transaction to the tree by a helper function
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
        #use head table pointer to create linked list in similar tree nodes
        if hdTable[item][1] == None:
            #point to the fist show shown node
            hdTable[item][1] = rootTree.child[item]
        else:
            #store original hdTable pointer in temp
            temp = hdTable[item][1]
            #find the last tree node in linked list (containing same item), 
            #and point that tree node to the latest tree node
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
        
        #down - top search
        #loop until reach root node
        while hdTableTemp[item][1].parent.title != 'root':
            #add path 
            path.append(hdTableTemp[item][1].parent.title)
            #to current node's parent
            hdTableTemp[item][1] = hdTableTemp[item][1].parent
            
        #add path to allPath
        allPath[frozenset(path)] = num
        
        #delete unnecessary files
        if frozenset() in allPath.keys():
            del allPath[frozenset()]
                  
        #to next linked item to find another path
        hdTable[item][1] = hdTable[item][1].next
    return allPath


#find frequent item
def freqFinder(fpTree, hdTable, freqItem, suffix, support):
    #freq item in header table
    item = []
    for tran in sorted(hdTable.items(), key=lambda s: s[1]):
        item.append(tran[0])
    
    for element in item:
        prefix = copy.deepcopy(suffix)
        if prefix == '':
            prefix = element
        #attach new element to prefix
        else:
            prefix = prefix + '&' + element
        #store freq item sets
        freqItem[prefix] = hdTable[element][0]
        #mine conditional tree recursively
        allPath = pathFinder(element, hdTable)
        hdTable2, freqSet = genHeadTb(allPath, support)
        condTree, hdTable2 = genTree(allPath, freqSet, hdTable2)
        if hdTable2 != None:
            freqFinder(condTree, hdTable2, freqItem, prefix, support)
    
    # ======================================================================
    # change frequent item set structure, for convenience of mining association rules.
    # put them in a list of dictionary,
    # the same length item set has the the same index in the list
    # ======================================================================
    #find maximum frequent item set length fist
    freqList = []
    maxLen = 0
    for item in freqItem.keys():
         maxLen = max(maxLen, len(item.split('&')))
    #initialize frequent item set 'list'
    freqList = [None] * maxLen

    for k, v in freqItem.items():
        #assign frequent item set different index based its key length
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




def assRule(freqItem):
    assRul =[]
    for i in range(len(freqItem)):
        for item in freqItem[-1-i]:
            itemSet = set(item.split('&'))
            #generate all nonempty subset 
            for j in range(len(itemSet)-1, 0, -1):
                #start from longest subset
                for itemS in subSet(itemSet, j):
                    subSetKey = '&'.join(sorted(itemS))
                    conf = freqItem[-1-i][item]/float(freqItem[j-1][subSetKey])
                    if conf >= confidence:
                        subSetKeyL_S = '&'.join(sorted(itemSet-set(itemS)))
                        assRul.append({'&'.join(sorted(itemS))+'>>>>'
                                       +subSetKeyL_S: conf})
                       # print '&'.join(sorted(itemS)), '>>>>', subSetKeyL_S
                       # print conf
            
    return assRul
                
#a function finding subset        
def subSet(S, m):
    # note we return an iterator rather than a list
    return set(itertools.combinations(S, m))







start_time = time.time()

read = Init('adult.data')
adData = read.DataList()

minSup = 0.6
confidence = 0.8
#calculate absolute support  
support = minSup * len(adData)
freqItem = []

#first scan: generate header table
hdTable, freqSet = genHeadTb(adData, support)
#second scan: generate FP tree
rootTree, hdTable = genTree(adData, freqSet, hdTable)

#ming FP tree, find frequent items 
freqItem = freqFinder(rootTree, hdTable, {}, '', support)
assRule = assRule(freqItem)


#output function
def output(filename, filename2):
    for i in range(len(freqItem)):
        temp = 'length ' + str(i+1) + ' item sets:' 
        json.dump(temp, file(filename, 'a'), indent =0)
        json.dump(freqItem[i], file(filename, 'a'), indent = 4)
    for i in assRule:
        json.dump(i, file(filename2, 'a'), indent = 0)
        
#output("fi.txt", "rule.txt")

APelapsed_time = time.time() - start_time
