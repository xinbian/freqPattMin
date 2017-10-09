# -*- coding: utf-8 -*-

"""Main module."""
import numpy as np
import pandas as pd
import csv

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
        #count as value, data attibutes as key
        c1 = {}
        for attrib in Apriori.dataCol:
            c1[attrib] = {}
        for tran in self.data: #loop over all tranctions
            flag = 0 #mark colomun position
            for item in tran: #loop over all items in a transaction
                key1 = Apriori.dataCol[flag]
                if item in c1[key1].keys():
                    c1[key1][item] += 1
                else:
                    c1[key1].update({item: 1})
                flag += 1 #flag move forward
        return c1
    #prune c1 generate l1
    def prune(self, c1):
        l1 = {}
        for attrib in c1.keys():
           l1[attrib] = {k: v for k , v in c1[attrib].items() if v >= self.minSup}

        #remove empty sub dictionary
        l1 = {k: v for k , v in l1.items() if v != {} }
       
         #to save memoery use c1 denotes l1 here
      
        return l1
    #from l_k generate c_k+1
    def selfJoin(self,lk):
        ckp1 = {}
        for key1 in Apriori.dataCol:
            for key2 in Apriori.dataCol:
                if key1 != key2:                  
                    ckp1[max(key1, key2) +'&' + min(key1, key2)] = {}
        for key1 in lk.keys():
            for key2 in lk.keys():
                if key1 != key2:
                    # next level in the dic
                    for key1Sub in lk[key1].keys():
                        for key2Sub in lk[key2].keys():
                            if key1 > key2:           
                                ckp1[key1 +'&'+ key2].update({key1Sub + '&' + key2Sub: 0})
                            else:
                                ckp1[key2 +'&'+ key1].update({key2Sub + '&' + key1Sub: 0})
        #remove empty sub dictionary
        ckp1 = {k: v for k , v in ckp1.items() if v != {} }
        return ckp1
    def count(self, ckp1):
        #scan data row by row
        k = 2
        for data in self.data:
            #genereate candidate ck set keys
            for key in ckp1.keys():
                #gnerate the sub-dict keys corresponding to ck keys
                for valueSub in ckp1[key].keys():
                    temp = 0
                    #since I store the n-itemset patterns in one key, sperated by '&'
                    #I need to split the patterns here, and count them by comaring with dataset
                    for i in range(k):
                        keysub = key.split('&')[i]
                        #find index in the orignial data list
                        dataIndex = Apriori.dataCol.index(keysub)
                        tempi = valueSub.split('&')[i]                   
                        if data[dataIndex] == tempi:
                            temp = temp + 1
                    #for length n pattern, this temp equals n meaning the pattern appear once
                    if temp == k:                      
                        ckp1[key][valueSub] += 1    
        #prune ck
        ckp1 = self.prune(ckp1)
         
        return ckp1
    #check subset 
    def aprioriCk(self, ck, lkm1):
        k = 2
        for key in ck.keys():
            for valueSub in ck[key].keys():
                #check all subsets
                for i in range(k):
                    tempSubSet = valueSub.split('&')
                    tempSubSet.pop(i)
                    subset = '&'.join(tempSubSet)
                    #if subset not in l_{k-1}, we delete this candidate
                    if not (subset in lkm1[key].keys()):
                        del ck[key][valueSub]
                        #end loop check next candidate
                        break
                
                
        
                
            
        
        
    
ap = Apriori(adData, 2, 2)
c1 = ap.c1Gen()
l1 =ap.prune(c1)

c2=ap.selfJoin(l1)
l2=ap.count(c2)
        


