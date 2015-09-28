'''
Created on 15 May 2015

@author: Russell
'''
import GenPercept

def _get_features(i, word, context, prev, prev2):
    '''Map tokens-in-contexts into a feature representation, implemented as a
    set. If the features change, a new model must be trained.'''
    def add(name, *args):
        features.add('+'.join((name,) + tuple(args)))
 
    i += len(GenPercept.GenPercept.START_PADDING)

    features = set()
    add('bias') # This acts sort of like a prior
    add('i suffix', word[-3:])
    add('i pref1', word[0])
    add('i-1 tag', prev)
    add('i-2 tag', prev2)
    add('i tag+i-2 tag', prev, prev2)
    add('i word', context[i])
    add('i-1 tag+i word', prev, context[i])
    add('i-1 word', context[i-1])
    add('i-1 suffix', context[i-1][-3:])
    add('i-2 word', context[i-2])
    add('i+1 word', context[i+1])
    add('i+1 suffix', context[i+1][-3:])
    add('i+2 word', context[i+2])
    return features