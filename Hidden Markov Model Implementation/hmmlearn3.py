# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 20:57:50 2017

@author: Vatsal Shah
"""
import time
from math import log
start_time = time.time()
import codecs
import json
import sys

#filename=sys.argv[1]
filename = 'hw5-data-corpus/catalan_corpus_train_tagged.txt'
train_text = codecs.open(filename,"r",encoding="utf8").read()

"""-------------------- Preprocess Data ------------------------ """

sentences = [word for word in (sentence.split(' ') for sentence in train_text.split('\n')) ]


new_sentence=[]

for sentence in sentences:
    new_words=[]
    for words in sentence:
        (word,tag)=words[:-3],words[-2:]
        new_words.append((word,tag))
    new_sentence.append(new_words)
new_sentence.pop()

all_words = [word for sentence in new_sentence for word in sentence]


"""-------------------- Get Tag Frequencies ------------------- """


tags={}    
for sentence in new_sentence:
    for (word,tag) in sentence:
        if tag not in tags:
            tags[tag]=1
        else:
            tags[tag]+=1
            



""" ------------------ Calculate Emission Probabilities -----------"""



emission_counts = {}
for (word,tag) in all_words:
    if tag not in emission_counts:
        emission_counts[tag]={}
    
    if word not in emission_counts[tag]:
        emission_counts[tag][word]=1
    else:
        emission_counts[tag][word]+=1
            

        
for every_tag,dictionary in emission_counts.items():
    count_of_tag = tags[every_tag]
    for (word,val) in dictionary.items():
        emission_counts[every_tag][word]=log(val/count_of_tag)
        


""" -------------- Calculate Transition Probabilities  ------------ """
transition_prob = {}
transition_prob['q0']={}
for every_sentence in new_sentence:
    
    first_tag=every_sentence[0][1]
    if first_tag not in transition_prob['q0']:
        transition_prob['q0'][first_tag]=1
    else:
        transition_prob['q0'][first_tag]+=1
  
    for i in range(len(every_sentence)):
       
        currentTag =  every_sentence[i][1]
        if i+1<len(every_sentence):
            nextTag = every_sentence[i+1][1]
        else:
            nextTag = None
        
        if nextTag is not None:
            if currentTag not in transition_prob:
                transition_prob[currentTag]={}
            
            if nextTag not in transition_prob[currentTag]:
                transition_prob[currentTag][nextTag]=1
            else:
                transition_prob[currentTag][nextTag]+=1
                
""" ---------------- Smoothing -------------- """
for trans_tag,dic in transition_prob.items():
    count=0
    for (tag,val) in dic.items():
        transition_prob[trans_tag][tag]= val+1
        count+=val+1
        
    for main_tag in tags :
        if main_tag not in transition_prob[trans_tag]:
            transition_prob[trans_tag][main_tag]=1
            count+=1
    
    for (tag,val) in dic.items():
        transition_prob[trans_tag][tag] = log(val/count)
        
""" ------------ Write Model File --------------- """

write_model = {
                
                "Transition_Probability" : transition_prob,
                "Emission_Probability" : emission_counts,
                "All_Words" : list(set(pair[0] for pair in all_words)),        
                "Tag_Frequencies" : tags        
        
              }
            
with open('hmmmodel.txt', 'w') as file:
            json.dump(write_model, file,indent=2)    
        
 
            
print("--- %s seconds ---" % (time.time() - start_time))       
        
    



