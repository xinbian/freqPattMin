#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 17:47:50 2017

@author: Xin
"""

# -*- coding: utf-8 -*-

"""Main module."""
import numpy as np
import pandas as pd
import csv
import time
import copy
import itertools

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
adData = [['cola', 'egg', 'ham'],['cola','diaper','beer'],['cola','diaper','beer','ham'],['diaper','beer']]

class Apriori:
    dataCol = ["age", "workclass", "fnlwgt", "education", "education-num", "martial-status",
		"occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
        	"hours-per-week", "country", "target"]
    def __init__(self, data, support, confi):
        self.data = data
        self.minSup = support
        self.minConf = confi
    #c1 and l1 generation
    def c1Gen(self):
        #store c1 in a dictionary
        #count as dict's value, data attibutes and value combination as key
        #for example{age:50 : 1} denotes age = 50, and count 1 
        c1 = {}
        for attrib in Apriori.dataCol:
            c1[attrib] = {}
        for tran in self.data: #loop over all tranctions
            flag = 0 #mark colomun position
            for item in tran: #loop over all attributes in a transaction
                #key = attibutes + value
                #test keyCmb = Apriori.dataCol[flag]+':'+item
                keyCmb = item
                if keyCmb in c1.keys():
                    c1[keyCmb] += 1
                else:
                    c1[keyCmb] = 1
                flag += 1 #flag move forward
        return c1
    
    #prune fucntion, generate l1 from c1
    def prune(self, c1):   
        # check minSup
        l1 = {k: v for k , v in c1.items() if v >= self.minSup and v != {}}
      #  l1 = {k: v for k , v in c1.items() if v != {} }
        return l1
    
    #from l1 generate c2
    def selfJoin(self,lk):
        ckp1 = {}
        for key1 in lk.keys():
            for key2 in lk.keys():
               #test if key1 != key2 and key1.split(':')[0] != key2.split(':')[0]: 
                if key1 != key2:  
                    ckp1[min(key1, key2) +'&' + max(key1, key2)] = 0             
        #remove empty sub dictionary
        ckp1 = {k: v for k , v in ckp1.items() if v != {} }
        return ckp1
    
    
    #from l_k generate c_k+1
    def selfJoin2(self,lk):
        ckp1 = {}
        #sort lk based on keys
        lk = sorted(lk.items(), key=lambda s: s[0])
        #lk is tuple now
        for i in range(len(lk)):
            #start from i+1 to avoid duplicates
            for j in range(i+1, len(lk)):
                #break 'merged keys'
                key1 = sorted(lk[i][0].split('&'))
                key2 = sorted(lk[j][0].split('&'))
                #lk ^ lk
                #test if (key1[0:len(key1)-1] == key2[0:len(key1)-1] and key1[-1].split(':')[0]
                #test != key2[-1].split(':')[0]):  
                if (key1[0:len(key1)-1] == key2[0:len(key1)-1]):  
                    key1.append(key2[-1])
                    keySort = '&'.join(sorted(key1))
                    ckp1[keySort]=0
        #remove empty sub dictionary and restore ckp1 to dictionary
        ckp1 = {k: v for k , v in ckp1.items() if v != {} }
        return ckp1
    
    
    def count(self, ckp1):
        #scan data row by row
        RedcData = copy.deepcopy(self.data)
        for tran in self.data:
            tranRedc = True
            #genereate candidate ck set keys
            for key in ckp1.keys():    
                k = len(key.split('&'))
                count = True
                #since I store the n-itemset patterns in one key, sperated by '&'
                #need to split the patterns here, and count them by comparing with dataset
                for i in range(k):
                    #spilt different attributes
                    #eg. get wrokclass:Private
                    keysub = key.split('&')[i]
# =============================================================================
#                     dataIndex = Apriori.dataCol.index(keysub.split(':')[0])
#                     #the pattern only exists in data when it meets all keys, say 
#                     if data[dataIndex] == keysub.split(':')[1]:
#                         count = count & True
# =============================================================================
                    if keysub in tran:
                        count = count & True
                    else:
                        count = count & False
                #all items match the transcation in database   
                if count == True:   
                    ckp1[key] += 1  
                    #if any frequent item is found in this transcation, keep the data
                    tranRedc = False
            #apply transaction reduction here
            #no frequent transcation found in this transcation, delete it
            if tranRedc:              
                RedcData.remove(tran)
        
        self.data =  copy.deepcopy(RedcData)
        return ckp1
    
    
    #check subset
    #ck length k candidate needs to be checked
    #lkm1 length k-1 frequent items 
    def aprioriCk(self, ck, lkm1):
        #generate a list containing items in l_k-1
        temp = []
        for lkm1Key in lkm1.keys():
            temp.append(set(lkm1Key.split('&')))
        for key in ck.keys():
            k = len(key.split('&'))
            #check all subsets
            for i in range(k):
                C1KeySub = key.split('&')
                del C1KeySub[i]
                #get subSet of Ck
                C1KeySub = set(C1KeySub)
                #if subset not in l_{k-1}, delete this candidate          
                if not (C1KeySub in temp):
                    del ck[key]
                    #end loop check next candidate
                    break
        return ck
    def assRule(self, freqItem):
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
                        if conf >= self.minConf:
                            subSetKeyL_S = '&'.join(sorted(itemSet-set(itemS)))
                            assRul.append({'&'.join(sorted(itemS))+'>>>>'
                                           +subSetKeyL_S: conf})
                            print '&'.join(sorted(itemS)), '>>>>', subSetKeyL_S
                            print conf
                
        return assRul


def subSet(S, m):
    # note we return an iterator rather than a list
    return set(itertools.combinations(S, m))
   
support = 2
confidence = 0.5
freqItem = []

#intialize
start_time = time.time()
ap = Apriori(adData, support, confidence)
#generate c1
c1 = ap.c1Gen()
#prunue c1
l1 = ap.prune(c1)
freqItem.append(l1)
#self join l1, generate c2
c2 = ap.selfJoin(l1)
#apriori check c2
c2 = ap.aprioriCk(c2, l1)
#count c2 and prune c2
l2 = ap.count(c2)
l2 = ap.prune(l2)
freqItem.append(l2)

while l2 != {}:
    c2 = ap.selfJoin2(l2)
    c2 = ap.aprioriCk(c2, l2)
    l2 = ap.count(c2)
    l2 = ap.prune(l2)
    freqItem.append(l2)
del freqItem[-1]
# =============================================================================

assRule = ap.assRule(freqItem)
APelapsed_time = time.time() - start_time
