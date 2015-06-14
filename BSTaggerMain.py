'''
Created on 15 May 2015

@author: Russell Moore
'''
from GenPercept import GenPercept
import conll_utils
import heapq

n_iter=20
max_sentences = 5000 # just train on 5000 sentences to start
training_file = 'C:\\Users\\Russell\\Dropbox\\nlp_alta\\tacl14_swbd_deps\\train.conll'
beam_w = 10

def beam_search(sentence, beam_width=5):
        #words = sentence.split()
        candidates = [(0.0,[])]
        scored_cands = []
        agenda = []
        #for i in range(iterations):
        j=0
        while True:
            for c in candidates:
                agenda += expand(c)

            scored_cands = []      
            for item in agenda: 
                heapq.heappush(scored_cands, score(item))
            
            candidates = heapq.nlargest(beam_width, scored_cands) #get the beam_width top scored candidates
            print 'iter',j,'top',beam_width,':',candidates 
            
            best = candidates[0]
            if goal_test(best):
                print "GOAL MET"
                return best
            agenda = []
            j+=1
    

def goal_test(cand):
    return len(cand[1]) == len(perc.context)-4 #i.e. is the list of tags the same length as the sentence (with 4 pieces of padding removed)

def score(item):
    #print 'unscored item=', item
    #how do we generally "score" our items?? we surely have to do an incremental weight comparison??
    score = perc.get_score(item)
    scored_item = (score, item[1])
    #print 'returning scored item=', scored_item
    return scored_item

def expand(cand):
    #cand is a tuple of form (score, [postags])
    possible_next_tags = perc.observed_tags
    #print "poss next tags", possible_next_tags
    #print "cand", cand
    newcs=[]
    for pnt in possible_next_tags:
        #score pnt in context
        newc=(cand[0], cand[1]+[pnt])
        #compute overall score
        newcs.append(newc)
    #print "new candidates:", newcs
    return newcs
    
if __name__ == '__main__':
 
    training_sentences = conll_utils.load_sentences(training_file, True, max_sentences)

    #create components
    perc = GenPercept()
    print "TRAINING"
    perc.train(n_iter, training_sentences)
    print "TOTAL ITERATIONS", perc.i
    print perc.N, perc.P, perc.i
    print perc.i == perc.N * perc.P
        
    #initialise the test data
    sentence = 'he lives in a pineapple under the sea'
    
    print "SETTING CONTEXT"
    perc.set_context(sentence.split())
    
    print "STARTING BEAM SEARCH"
    best = beam_search(sentence, beam_w)
    print "ENDED BEAM SEARCH"
    print sentence, best
    