'''
Created on 11 May 2015

@author: Russell Moore MA Cantab FRSA - russellmoo.re
'''
from _pytest.main import Item
from __builtin__ import True

import heapq

class BeamSearcher(object):
    '''
    classdocs
    '''
    
    def __init__(self, params):
        '''
        Constructor
        '''
        self.agenda = []
        self.candidates = []
        self.beam_width = 5
    
    #Here we implement the generic beam search algo    
    def beam_search(self, iterations):
        candidates = self.start_item(problem)
        agenda = []
        for i in (range(iterations)):
            for c in self.candidates:
                agenda.append( expand(c,problem) )
            best = self.top(agenda)
            if self.goal_test(problem, best):
                return best
            self.candidates = self.get_top_n(agenda, self.beam_width)
            agenda = []


    def start_item(self, problem):
        #in the segn task, the start state item is a pair, of an empty segmented sentence, and the complete seq of words waiting to be segmented
        
        return [([],"this is the sentence we want to segment this is not this is also not although we will here is another".split())]
    
    
    def expand(self, cand, prob):
        
        
    
    def top(self, agenda):
        maxscore = 0
        for item in agenda:
            if score(item) > maxscore:
                max_item = item 
        return maxscore
    
    def goal_test(self, problem, cand):
        if(len(cand[1])==0):
            return True
        return False

    def get_top_n(self, agenda, beam_width):
        scores = []
        for item in agenda:
            scored_tuple = (score(item),item)
            heapq.heappush(scores, scored_tuple)
        return [scored_tuple[1] for scored_tuple in heapq.nlargest(beam_width, scores)]
    
    #expand takes the partially segmented sentence in a state item, and extends it in all possible ways
    
    