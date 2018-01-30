# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 12:31:51 2017

@author: Iven
9"""

import ijson
import io
import pandas as pd
import numpy as np
import RAKE as rk
from rake_nltk import Rake
import gensim
from sklearn.cluster import KMeans
from collections import Counter
import datetime
import pickle
#from langdetect import detect

biz=[];texts=[]
review_path = r"C:\Serious\1stterm\Compsci516\projects\review.json"
with open(r"C:\Serious\1stterm\Compsci516\projects\review.json", 'rb') as json_file:
        for line in json_file:
            for val in ijson.items(io.BytesIO(line), ""):
                texts.append(val["text"])
                biz.append(val["business_id"])
'''filter by language'''
#langs=[]
    #for text in texts:
        #langs.append(detect(text))

data={"biz":biz,"text":texts}
review=pd.DataFrame(data)


#eng_reviw=review[review.language=="en"]

'''tagging separately'''
sampl=range(4000000)
train=review.loc[sampl]
print(datetime.datetime.now())#0
uniqbiz=set(list(train.biz))#
reviws=[]#review grouped by each restaurant
for biz in uniqbiz:
    biz_reviw=list(train.loc[train.biz==biz,"text"])
    biz_onestr=" ".join(biz_reviw)
    reviws.append(biz_onestr)

print(datetime.datetime.now())#1

keywords=[]
for rev in reviws:
    #r=Rake()
    #r.extract_keywords_from_text(rev)
    #keywords.append(r.get_ranked_phrases()[0:5])
    Rake = rk.Rake(rk.SmartStopList())
    kw=Rake.run(rev)
    kwap=[]
    counter=0
    invalid = ['+', '=', '/', '@', '*','_']
    for k in kw:
        if len(k[0].split(" "))==1 and counter<=9 and len(k[0])<=15:
            flag = False
            for i in invalid:
                if i in k[0]:
                    flag = True
                    break
            if  not flag:
                kwap.append(k[0])
                counter=counter+1
            
    keywords.append(kwap)

biztag=pd.DataFrame({'restaurant':list(uniqbiz),'tag':keywords})

print(datetime.datetime.now())#2

#transfer format for word2vec
def sentencize(text,biztxt=[]):
    if(text=="."):
        return biztxt
    sentences=text.replace('!','.').replace('?','.').split(".")
    
    for sentence in sentences:
        if sentence!='' and sentence!=' ':
            sentence=sentence.replace(',', ' ').replace(';',' ').replace(':',' ').replace('!',' ')
            txtlist=sentence.split(' ')
            txtlist=[t for t in txtlist if t!='' and t!=' ']
            biztxt.append(txtlist)
    return biztxt

print(datetime.datetime.now())#3

alltext="".join(list(train['text']))

sentences=sentencize(alltext,[])

m=gensim.models.Word2Vec(sentences, size=15, window=5, min_count=0, workers=4)

allkeywords=set([kw for l in keywords for kw in l])

keyvecs=[]
havv=[]
print(datetime.datetime.now())#4
for word in allkeywords:
    try:
        keyvecs.append(m.wv[word].tolist())
        havv.append(True)
    except:
        keyvecs.append([])
        havv.append(False)

wordvec=pd.DataFrame({'word':list(allkeywords),'vec':keyvecs,'value':havv})

wvclus=wordvec.loc[wordvec.value].vec
words=wordvec.loc[wordvec.value].word

print(datetime.datetime.now())#5

nclus=300
kmeans = KMeans(n_clusters=nclus, random_state=0).fit(wvclus.tolist())
centers=kmeans.cluster_centers_

cluster=pd.DataFrame({'word':words,'label':kmeans.labels_})
'''Define the representative words for each cluster'''
'''repre=[]
for i in range(nclus):
    cluster.loc[cluster.label==i].word.tolist()
    repre.append(cluster.loc[cluster.label==i].word.tolist()[0])

repword=pd.DataFrame({'label':[i for i in range(nclus)],'repword':repre}).set_index('label')

reptab=cluster.set_index("label").join(repword)


newtags=[]

for i in range(len(biztag)):
    newtag=[]
    tags=biztag.tag.loc[i]
    for tag in tags:
        if tag in words.tolist():
            newtag.append(reptab[reptab.word==tag].repword.tolist()[0])
    newtags.append(list(set(newtag)))

finalbiztag=({"biz":uniqbiz,"tags":newtags})'''

types=[]
for i in range(len(biztag)):
    belong=[]
    tags=biztag.tag.loc[i]
    for tag in tags:
        if tag in words.tolist():
            belong.append(cluster[cluster.word==tag].label.tolist()[0])
    types.append(list(belong))
print(datetime.datetime.now())#

def encode(types):
    return [types.count(i) for i in range(300)]

encodes=[encode(type) for type in types]

biztype=pd.DataFrame({'biz':list(uniqbiz),'type':types,'encode':encodes})

#retn={'biz':list(uniqbiz),'encode':encodes}
listbiz = list(uniqbiz)
result = {}
for i in range(len(listbiz)):
    result[listbiz[i]] = encodes[i]    
output = open('data1.pkl', 'wb')
pickle.dump(result, output)
output.close()