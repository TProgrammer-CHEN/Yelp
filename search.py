# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 10:32:47 2017

@author: Iven
"""
import math

inp=['nur']

def distance(vec1,vec2):
        if(len(vec1)!=len(vec2)):
            print("your ass!")
            return"Error"
        else:
            sqsum=0
            for i in range(len(vec1)):
                sqsum=(vec1[i]-vec2[i])**2+sqsum
            return math.sqrt(sqsum)

def search(inpt):
    vecs=[m.wv[tag].tolist() for tag in inpt]

    inputtypes=[]
    for vec in vecs:
        diss=[distance(vec,center) for center in centers]
        inputtypes.append(diss.index(min(diss)))

    #query is the vector for input
    query=encode(inputtypes)
    
    return query



'''space=biztype.encode.tolist()

compare=[distance(query,vec) for vec in space]

res=biztag
res["rank"]=compare
res.sort_values('rank')'''
