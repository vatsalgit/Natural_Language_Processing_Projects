# -*- coding: utf-8 -*-
import time
import json
import sys
import codecs
from math import log
import os
from multiprocessing import Pool

filename = sys.argv[1]
#filename='hw5-data-corpus/catalan_corpus_dev_raw.txt'


start_time = time.time()
test_text = codecs.open(filename,"r",encoding="utf8").read()


with open('hmmmodel.txt','r') as file:
    my_hmm_model=json.load(file)   

transition_prob = my_hmm_model["Transition_Probability"]
emission_prob = my_hmm_model["Emission_Probability"]
all_words = set(my_hmm_model["All_Words"])
tag_freq = my_hmm_model["Tag_Frequencies"]
tags = [tag for (tag,freq) in tag_freq.items()]
known_tags = {}
for i in range(len(tags)):
    known_tags[i] = tags[i]
    
output = []
test_sentences = [word for word in (sentence.split(' ') for sentence in test_text.split('\n'))]

def handle_unseen_emissions(tag,word):
    if word not in all_words:
        return 0.0
    
    if word in emission_prob[tag]:
        return emission_prob[tag][word]
    
    else:
        return -sys.maxsize

def get_max(state):
    most_probable_state=None
    max_prob = -999999999999
    for pairs in state:
        if pairs[0]>max_prob:
            max_prob=pairs[0]
            most_probable_state=pairs
    back_pointer = most_probable_state[1]
    most_probable_tag=known_tags[state.index(most_probable_state)]
    return most_probable_tag,back_pointer
        

def viterbi_decoding(words):
    """-------------------- Front Propogation ----------------------"""
    probability_matrix = []
    start_state = []
    for i in range(len(known_tags)):
        emission = handle_unseen_emissions(known_tags[i], words[0])
        transition = transition_prob['q0'][known_tags[i]]
        current_proba = transition + emission
        
        start_state.append((current_proba, None,known_tags[i]))
    
    probability_matrix.append(start_state)
    
    for i in range(1, len(words)):
        state = []
        for (index,prev_tag) in known_tags.items():
            
            max_probability = -99999999999
            bp_max = -999999999999999
            back_pointer = -99999999999
            
            emission = handle_unseen_emissions(prev_tag, words[i])
                      
            for (new_index,next_tag) in known_tags.items():
                    
                transition =   transition_prob[next_tag][prev_tag]
                prob_current = probability_matrix[i-1][new_index][0] + transition + emission
                back_prob =    probability_matrix[i-1][new_index][0] + transition
                
                if back_prob> bp_max:
                    back_pointer = new_index
                    bp_max = back_prob
                
                max_probability=max(max_probability,prob_current)
                    
    
            state.append((max_probability,back_pointer,prev_tag))
        
        probability_matrix.append(state)

    """ -------------- Back-Propogation --------------- """
            
    last_state = probability_matrix[len(probability_matrix)-1]
    
    most_probable_tag,back_pointer =  get_max(last_state)    
    
    final_answer = []
    final_answer.append((words[len(probability_matrix)-1],most_probable_tag))
   
    x = len(probability_matrix)-2
    
    while x>=0:
        final_answer.append((words[x],known_tags[back_pointer]))
        back_pointer = probability_matrix[x][back_pointer][1]
        x -= 1
    
    final_answer.reverse()
    
    return final_answer

if __name__ == '__main__':
    # Define the parameters to test
   
    pool = Pool(os.cpu_count())

    # Parallel map
    
    results = pool.map(viterbi_decoding, test_sentences)
    
    write_list=[]
    for lists in results:
        format_list = [pair[0]+"/"+pair[1] for pair in lists]
        output = " ".join(format_list)
        write_list.append(output)
    

    with codecs.open('hmmoutput_new.txt','w',encoding='utf8') as text_file:
        text_file.write("\n".join(write_list))
    print("--- %s seconds ---" % (time.time() - start_time))

    