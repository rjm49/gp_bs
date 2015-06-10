'''
Created on 10 Jun 2015

@author: Russell Moore
'''
import os

def load_sentences(training_file, keep_tags=True, max_sentences=1000):
    training_sentences = []
    file_list = []

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
    return training_sentences