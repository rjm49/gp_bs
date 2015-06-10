'''
Created on 15 May 2015

@author: Russell Moore
'''
from GenPercept import GenPercept
import os

if __name__ == '__main__':
    n_iter=20
    max_sentences = 5000 # just train on 5000 sentences to start
    
    training_file = 'C:\\Users\\Russell\\Dropbox\\nlp_alta\\tacl14_swbd_deps\\train.conll'
    file_list=[]
    keep_tags=True
    
    training_sentences = []
    
    if os.path.isfile(training_file):
        print "is file"
        file_list=[training_file]
    else:
        print "not a valid file"
        exit()
        
    for fname in file_list:
        raw_file = open(fname, 'r')
        conll_str = raw_file.read().strip()
        segs = conll_str.split('\n\n')
        i=0
        
        for seg in segs:
            #print '****************************'
            oseg = ''
            for line in seg.split('\n'):
                #print '<',line,'>'
                fields = line.split()
                #print fields
                
                if not len(fields):
                    continue
                
                word = fields[1]
                pos = fields[4]
#                 word = fields[1].split('_')[0]
#                 pos = fields[1].split('_')[1]
                
                if word == 'i':
                    word = 'I'
                
                if word in ['uh','mm','er','um']:
                    print 'skipped ', word
                    continue
                
                if keep_tags:
                    oseg= oseg + ' ' + word+'/'+pos
                else:
                    oseg= oseg + ' ' + word
                
            #print oseg
            training_sentences.append(oseg)
            if (i<(max_sentences-1)):
                i+=1
            else:
                break
            
        raw_file.close()
        print 'finished: ', raw_file
        
    
    #example_strings = ['the/DT first/JJ example/NN string/NN', 'the/DT second/JJ example/NN string/NN', 'the/DT second/JJ string/NN', 'the/DT example/NN'] # use a list of tagged strings

    
    #Initialise the examples data
    
    #create components
    perc = GenPercept()
    perc.train(n_iter, training_sentences)
    print "TOTAL ITERATIONS", perc.i
    print perc.N, perc.P, perc.i
    print perc.i == perc.N * perc.P
    
    
    #initialise the test data
    sentence = 'I do n\'t know he looks like a giant chicken who lives in the sea'
    
    print sentence, perc.predict_tags(sentence)