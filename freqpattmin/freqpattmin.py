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
        with open(self.filename, 'r') as f:
            data = list(csv.reader(f))
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
    def prune(self):
        self.c1Gen()
        for attrib in Apriori.dataCol:
           c1[attrib] = {k: v for k , v in c1[attrib].items() if v >= self.minSup}
        return c1
ap = Apriori(adData, 2, 2)
c1 = ap.c1Gen()

l1= ap.prune()
        


