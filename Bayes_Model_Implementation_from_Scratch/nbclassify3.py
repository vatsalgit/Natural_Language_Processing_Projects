# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 20:04:24 2017

@author: Vatsal Shah
"""
import json
import re
import sys


model = open('nbmodel.json','r').read()
model = json.loads(model)
model.pop('',0)

test_reviews = open(sys.argv[1],"r").read()
#train_labels = open("hw2-data-corpus/train-labels.txt","r").read()

stop_words = open("stop-word-list.txt","r").read()


stop_words_list = [word for word in stop_words.split('\n')]
stop_words_dict = {}

for word in stop_words_list:
    stop_words_dict[word]=1

reviews = [review for review in test_reviews.split('\n') ]

#labels = [label for label in train_labels.split('\n')]

#train_merged = [item for item in zip(reviews,labels)]

cleaned_reviews = []
review_id = []
#cleaned_labels = []
del reviews[-1]
for review in reviews:
     temp  = review.split(None,1)   
     review_id.append(temp[0])
     cleaned_reviews.append(temp[1:])
     
#cleaned_labels.append(label.split(None,2)[1:])


#del cleaned_labels[-1]


x = []
all_words= []
for i in range(len(cleaned_reviews)):
    temp = cleaned_reviews[i][0]
    temp = re.sub(r'[^\w\s]','',temp)
    temp = re.sub(r'\d+','',temp)    
    temp = temp.split(' ')
    for word in temp:
        all_words.append(word.lower())
    temp = [word.lower() for word in temp if word.lower() not in stop_words_dict]
    temp = " ".join(temp)
    x.append(temp)


cleaned_reviews = x

#test_reviews = cleaned_reviews[0:10]



predictions = []

text_file = open("nboutput.txt", "w")


i=0
for review in cleaned_reviews:
    pos_prob = 1
    neg_prob = 1
    aut_prob = 1
    fake_prob = 1
    
    for word in review.split(' '):
        if word in model:
            pos_prob = pos_prob*model[word][0]
            neg_prob = neg_prob*model[word][1]
            aut_prob = aut_prob*model[word][2]
            fake_prob = fake_prob*model[word][3]
    
    text_file.write(review_id[i]+' ')
    
    if aut_prob>fake_prob:
        text_file.write('truthful ')
    else:
        text_file.write('deceptive ')
        
    if pos_prob>neg_prob:
        text_file.write('positive')
    else:
        text_file.write('negative')
    
    text_file.write('\n')
    i+=1


    
text_file.close()    
    

