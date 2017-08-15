# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 23:33:26 2017

@author: Vatsal Shah
"""
import re
import json
import sys

train_reviews = open("train-text.txt","r").read()
train_labels = open("train-labels.txt","r").read()
stop_words = open("stop-word-list.txt","r").read()
#train_reviews = open(sys.argv[1],"r").read()
#train_labels = open(sys.argv[2],"r").read()
#stop_words = open("stop-word-list.txt","r").read()


stop_words_list = [word for word in stop_words.split('\n')]
stop_words_dict = {}

for word in stop_words_list:
    stop_words_dict[word]=1

reviews = [review for review in train_reviews.split('\n') ]

labels = [label for label in train_labels.split('\n')]

train_merged = [item for item in zip(reviews,labels)]

cleaned_reviews = []
cleaned_labels = []

for (review,label) in train_merged:
     cleaned_reviews.append(review.split(None,1)[1:])
     cleaned_labels.append(label.split(None,2)[1:])

del cleaned_reviews[-1]
del cleaned_labels[-1]


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

sentiment = [cleaned_labels[i][1] for i in range(len(cleaned_labels))]
authenticity = [cleaned_labels[i][0] for i in range(len(cleaned_labels))]

data_sentiment = [item for item in zip(cleaned_reviews,sentiment)]

data_authenticity = [item for item in zip(cleaned_reviews,authenticity)]

positive_reviews = [x[0] for x in data_sentiment if x[1]=='positive']
negative_reviews = [x[0] for x in data_sentiment if x[1]=='negative']
authentic_reviews = [x[0] for x in data_authenticity if x[1]=='truthful']
fake_reviews = [x[0] for x in data_authenticity if x[1]=='deceptive']


prior_positive = len(positive_reviews)/len(data_sentiment)
prior_negative = len(positive_reviews)/len(data_sentiment)
prior_aut = len(authentic_reviews)/len(data_authenticity)
prior_fake = len(fake_reviews)/len(data_authenticity)



total_pos_words=0
for text in positive_reviews:
    for word in text.split(" "):
        total_pos_words+=1

total_neg_words=0
for text in negative_reviews:
    for word in text.split(" "):
        total_neg_words+=1

total_fake_words=0
for text in fake_reviews:
    for word in text.split(" "):
        total_fake_words+=1

total_aut_words=0
for text in authentic_reviews:
    for word in text.split(" "):
        total_aut_words+=1



word_freq_pos = {}
word_freq_neg = {}
word_freq_aut = {}
word_freq_fake = {}



for review in positive_reviews:
    for word in review.split(" "):
        if word not in word_freq_pos:
            word_freq_pos[word]=1
        else:
            word_freq_pos[word]+=1
            

for review in negative_reviews:
    for word in review.split(" "):
        if word not in word_freq_neg:
            word_freq_neg[word]=1
        else:
            word_freq_neg[word]+=1

for review in authentic_reviews:
    for word in review.split(" "):
        if word not in word_freq_aut:
            word_freq_aut[word]=1
        else:
            word_freq_aut[word]+=1

for review in fake_reviews:
    for word in review.split(" "):
        if word not in word_freq_fake:
            word_freq_fake[word]=1
        else:
            word_freq_fake[word]+=1

# Calculate Probabilities     


#Perform Laplace Smoothing

all_words_dict = {}
for word in all_words:
    if word not in all_words_dict:
        all_words_dict[word]=1
    else:
        all_words_dict[word]+=1

all_words_dict.pop('',0)
all_words_dict.pop('a',0)
all_words_dict.pop('aaa',0)
all_words_dict.pop('aaahed',0)

    
for every_word in all_words_dict:
    
    if every_word in word_freq_pos:
        word_freq_pos[every_word]+=1
    else:
        word_freq_pos[every_word]=1
        
    if every_word in word_freq_neg:
        word_freq_neg[every_word]+=1
    else:
        word_freq_neg[every_word]=1

    if every_word in word_freq_aut:
        word_freq_aut[every_word]+=1
    else:
        word_freq_aut[every_word]=1

    if every_word in word_freq_fake:
        word_freq_fake[every_word]+=1
    else:
        word_freq_fake[every_word]=1
        

model = {}



for word in all_words_dict:
    temp = []
    
    temp.append(prior_positive*word_freq_pos[word]/(total_pos_words+len(all_words_dict)))
    temp.append(prior_negative*word_freq_neg[word]/(total_neg_words+len(all_words_dict)))
    temp.append(prior_aut*word_freq_aut[word]/(total_aut_words+len(all_words_dict)))
    temp.append(prior_fake*word_freq_fake[word]/(total_fake_words+len(all_words_dict)))   
    
    model[word] = temp


import json
with open('nbmodel.json', 'w') as output:
    json.dump(model,output )









      
"""
sorted_pos = []
for w in sorted(word_freq_pos, key=word_freq_pos.get, reverse=True):
  sorted_pos.append((w, word_freq_pos[w]))

for review in negative_reviews:
    for word in review.split(" "):
        if word not in word_freq_neg:
            word_freq_neg[word]=2
        else:
            word_freq_neg[word]+=1
            
sorted_neg = [] 
for w in sorted(word_freq_neg, key=word_freq_neg.get, reverse=True):
  sorted_neg.append((w, word_freq_neg[w]))
  
prior_positive = len(positive_reviews)/len(data_sentiment)

prior_negative = len(negative_reviews)/len(data_sentiment) 


for word,freq in word_freq_pos.items():
    word_freq_pos[word] = word_freq_pos.get(word)/(total_pos_words+total_pos_words+total_neg_words)

for word,freq in word_freq_neg.items():
    word_freq_neg[word] = word_freq_neg.get(word)/(total_neg_words+total_pos_words+total_neg_words)


with open('nbmodel.txt', 'w') as f:
    for key, value in word_freq_pos.items():
        f.write('%s:%s\n' % (key, value))
"""


"""
test_string = ["05P7vUPmaePGNE1MbNnr My fiancee and I were looking for a modern, upscale venue for our wedding reception. We have found the perfect location at The James. From the ballroom to the personal attention to detail, each step was handled with care. Now that we have locked in our date, we are more excited than ever. Thank you staff at The James for making our day even more special!"]

temp = re.sub(r'[^\w\s]','',test_string[0])
temp = re.sub(r'\d+','',temp)    
temp = temp.split(' ')
for word in temp:
    all_words.append(word.lower())
temp = [word.lower() for word in temp if word.lower() not in stop_words_dict]
temp = " ".join(temp)
temp
pos = 1
neg = 1
for word in temp.split(' '):
    if word in model:
        pos = pos * model[word][0]
        neg = neg * model[word][1]
pos>neg

my_dict = {}
for i in range(len(cleaned_reviews)):     
     my_string = cleaned_reviews[i][0].lower().split()
     for item in my_string:
        if item in my_dict:
            my_dict[item] += 1
        else:
            my_dict[item] = 1
print(len(my_dict))
"""