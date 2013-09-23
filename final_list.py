#Filename: final_list.py
#get the list of words in approperiate odder

import wordNet
import copy
from __builtin__ import any as b_any

def get_final_list(wordsList):

    '''functions for get the sematically linked words list
      traverse and check every word then '''
    
    words1 = wordsList
    words2 = copy.copy(wordsList)
    final_list = []
    for w in  words1:
            synlst = wordNet.getsynList(w)
            hyplst = wordNet.gethypSet(w)
            hyperlst = wordNet.gethyperSet(w)
            for w2 in words2:
                    if (w2 in synlst
                        or w2 in hyplst
                        or w2 in hyperlst
                        or b_any(w2 in x for x in synlst)
                        or b_any(w2 in x for x in hyplst)
                        or b_any(w2 in x for x in hyperlst)):
                            final_list.append(w2)
                            words2.remove(w2)
    return final_list
