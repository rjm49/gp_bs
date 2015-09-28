'''
Created on 15 May 2015

@author: Russell Moore
'''
from GenPercept import GenPercept
import conll_utils

n_iter=20
max_sentences = 5000 # just train on 5000 sentences to start
training_file = 'C:\\Users\\Russell\\Dropbox\\nlp_alta\\tacl14_swbd_deps\\train.conll'

if __name__ == '__main__':
 
    training_sentences = conll_utils.load_sentences(training_file, True, max_sentences)
    #create components
    perc = GenPercept()
    perc.train(n_iter, training_sentences)
    print "TOTAL ITERATIONS", perc.i
    print perc.N, perc.P, perc.i
    print perc.i == perc.N * perc.P
        
    #initialise the test data
    sentence = 'he lives in a pineapple under the sea'
    print sentence, perc.predict_tags(sentence)