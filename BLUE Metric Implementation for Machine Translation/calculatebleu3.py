# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 16:58:56 2017

@author: Vatsal Shah
"""
import codecs
import math
import os 
from os import listdir
from os.path import isfile, join
import sys



def get_ngram_count(sentence,n_gram_count):
    count_dictionary = {}
    count_ngrams = 0
    for j in range(len(sentence)-n_gram_count+1):
        count_ngrams+=1
        g = ' '.join(sentence[j:j+n_gram_count])
        count_dictionary.setdefault(g, 0)
        count_dictionary[g] += 1
     
    return count_dictionary,count_ngrams

def get_clippings(can_ngram_counts,ref_ngram_counts):
    
    count_clippings = 0
    
    for (ngram,freq) in can_ngram_counts.items():
        if ngram in ref_ngram_counts:
            count_clippings+= min(can_ngram_counts[ngram],ref_ngram_counts[ngram])
    
    
    return count_clippings

def get_brevity_penalty(candidate,list_references):
    
    r=0
    c=0
    
    for i in range(len(candidate)):
        
        min_length=sys.maxsize     
        
        candidate_sentence = candidate[i].strip().split(' ')
        c+=len(candidate_sentence)
        
        for each_reference in list_references:
            reference = each_reference[i].strip().split(' ')
            difference = abs( len(candidate_sentence) - len(reference) )
            
            if difference<min_length:
                min_length=difference
                best_match = len(reference)
        
        r+=best_match
        
#    print (r,c)
                          
    return 1.0 if c>r else math.exp(1-(r/c))
    

def get_bleu_score(scores):
    
    geometric_mean=0
    for score in scores:
        geometric_mean+=(0.25*math.log(score))
    
    return math.exp(geometric_mean)



def main():
    path_to_reference= "reference-1.txt"
    path_to_candidate="Candidate/candidate-1.txt"

#    path_to_reference= sys.argv[2]
#    path_to_candidate=sys.argv[1]

    candidate=codecs.open(path_to_candidate,"r",encoding="utf-8")
    candidate_sentences = [sentence for sentence in candidate]

    list_of_reference=[]
    
    if os.path.isdir(path_to_reference):
        onlyfiles = [f for f in listdir(path_to_reference) if isfile(join(path_to_reference, f))]
        
        for file in onlyfiles:
            reference=codecs.open(join(path_to_reference,file),"r",encoding="utf-8")
            reference_sentences = [sentence for sentence in reference]
            list_of_reference.append(reference_sentences)
            
    else:
        reference=codecs.open(path_to_reference,"r",encoding="utf-8")
        reference_sentences = [sentence for sentence in reference]
        list_of_reference.append(reference_sentences)
    
    
    brevity_penalty=get_brevity_penalty(candidate_sentences,list_of_reference)
#    print(brevity_penalty)
    
    
    scores=[]
    for k in range(1,5): 
        total_clippings=0
        total_ngram_tokens=0
        
        for i in range(len(candidate_sentences)):
           curr_candidate = candidate_sentences[i].strip().split(' ')
           can_clipped,can_count_ngram = get_ngram_count(curr_candidate,k)
           
           max_clipping=-sys.maxsize
           for each_reference in list_of_reference:       
               curr_reference = each_reference[i].strip().split(' ')           
               ref_clipped,ref_count_ngram = get_ngram_count(curr_reference,k)
               temp_clippings=get_clippings(can_clipped,ref_clipped)
               max_clipping=max(temp_clippings,max_clipping)
            
           total_clippings+=max_clipping
           total_ngram_tokens+=can_count_ngram
           
        scores.append(float(total_clippings)/total_ngram_tokens)

    
    bleu_score = get_bleu_score(scores)
    
    bleu_score=(bleu_score)*brevity_penalty
    print (bleu_score)
    text_file = open("bleu_out.txt", "w")
    text_file.write(str(bleu_score))
    text_file.close()
        
if __name__ == "__main__":
    main()
