'''
Created on 13 May 2015

@author: Russell
'''
import random
import FeatureExtractor
from _collections import defaultdict

debug = True

class GenPercept(object):
    START_PADDING = ["!START1!","!START2!"]
    END_PADDING = ["!END1!","!END2!"]

    def __init__(self):
        self.weights = {}
        self.observed_tags = set()
        
        self._totals=defaultdict(int)
        self._timestamps=defaultdict(int)
        self.i=0
        
        self.N = 0 #N is number of training sentences
        self.P = 0 #P is number of training iterations

        #we actually want to convert ['the/DT first/JJ example/JJ string/NN', 'the/DT second/JJ example/JJ string/NN']
        #to [ (['the','first','example','string'],['DT','JJ','JJ','NN']), (['the','second','example','string'],['DT','JJ','JJ','NN']) ]

    def set_context(self, words):
        self.context = GenPercept.START_PADDING + words + GenPercept.END_PADDING #fill out the space at either end to allow back and fwd looking features
               
    def train(self, n_iter, examples):
        self.N = n_iter
        self.P = len(examples)
        
        for n in range(n_iter):
            random.shuffle(examples)
            for words, tags in self._parallelise(examples):
                self.observed_tags = self.observed_tags.union(tags) # build up a set of seen tags as we go
                self.set_context(words)
                prev, pprev = GenPercept.START_PADDING

                for wi, word in enumerate(words):
                    feats = FeatureExtractor._get_features(wi, word, self.context, prev, pprev) #this returns the set of features that this word has...
                    guess_tag = self.predict(feats)
                    real_tag = tags[wi]
                    if real_tag != guess_tag:
                        self.update(real_tag, guess_tag, feats)
                    pprev = prev
                    prev = guess_tag
                    
                self.i += 1
        self.average_weights()

    def predict_tags(self, sentence):
        words = sentence.split()
        self.set_context(words)
        prev, pprev = GenPercept.START_PADDING
        
        predicted_tags = []
        i=0
        
        for w in words:
            feats = FeatureExtractor._get_features(i, w, self.context, prev, pprev )
            guess_tag = self.predict(feats)
            predicted_tags.append(guess_tag)
            
            pprev = prev
            prev = guess_tag
            i += 1
            
        return predicted_tags

    def predict(self, features):
        '''Dot-product the features and current weights and return the best class.'''
        scores = defaultdict(float) 
        for feat in features:
            if feat not in self.weights:
                continue
            f_weights = self.weights[feat]
            for klass, f_weight in f_weights.items(): #items returns (k,v) tuples!
                scores[klass] += f_weight
        return max(self.observed_tags, key=lambda klass: (scores[klass], klass)) #ok, so this returns the max (class, score) combo

#will need this for a non-greedy implementation
    def get_scores(self, features):
        scores=defaultdict(float)
        for feat in features:
            if feat not in self.weights:
                continue
            weights = self.weights[feat]
            for cls, wgt in weights.items():
                scores[cls] += wgt
        return scores

    def get_score(self, state_item):
        #firstly, our item is in form (score, [postags])
        
        #print "state item:", state_item
        
        score = state_item[0]
        tags_so_far= self.START_PADDING + state_item[1]
        #print 'tags:', tags_so_far
        
        #print "CONTEXT:", self.context
                
        index = len(tags_so_far)-3
        cls = tags_so_far[-1]
        prev = tags_so_far[-2]
        pprev = tags_so_far[-3]
        word = self.context[index]
        print word, "=?", cls, "(given:", prev, pprev, ")"
        
        features = FeatureExtractor._get_features(index, word, self.context, prev, pprev)
        for feat in features:
            if feat not in self.weights:
                continue
            f_weights = self.weights[feat]
            
            if cls not in f_weights:
                continue
            
            score += f_weights[cls]
        return score

    def update(self, truth, guess, features):
        def upd_feat(c, f, delta):            
            if f not in self.weights:
                self.weights[f]={}
            
            if c not in self.weights[f]:
                self.weights[f][c]=0.0
                            
            curr_w = self.weights[f][c]
            key = (f,c) #combine the feature and class into a single key
            
            #print 'UPDATE',key,':', self.i, '-', self._timestamps[key], '=', (self.i - self._timestamps[key])
            self._totals[key] += (self.i - self._timestamps[key]) * curr_w # i.e. the num of iterations at a given weight, times the weight
            self._timestamps[key] = self.i
            self.weights[f][c] = curr_w + delta
            #print 'NEW WEIGHT', f, c, self.weights[f][c]
        
        for f in features:
            upd_feat(truth, f, 1.0)
            upd_feat(guess, f, -1.0)
        

    def average_weights(self):
        '''Average weights from all iterations.'''
        for f, f_wts in self.weights.items():
            new_f_wts = {}
            for c, w in f_wts.items():
                key = (f,c)
                total = self._totals[key]
                total += (self.i - self._timestamps[key]) * w
                averaged = round(total / float(self.i), 3)
                if averaged:
                    new_f_wts[c] = averaged
                    
                print c, '(',f,')' , total, '->' , averaged
                    
            self.weights[f] = new_f_wts
            #print 'set weights', f, 'to be', new_f_wts
        return None
    
    def _parallelise(self, string_arr): #convert a list of tuples [(k0,v0)..(kn,vn)] into tuple of lists ([k0..kn],[v0..vn])
        out_list = []
        for sent in string_arr:
            #print sent
            words = []
            tags = []
            for tok in sent.split():
                #print tok
                w,t = tok.split('/')
                print w,t
                words.append(w)
                tags.append(t)
            out_list.append((words,tags))
        return out_list