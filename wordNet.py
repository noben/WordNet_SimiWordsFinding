#Filename: wordNet.py
#iteratively get synset of the input list of words and the hyponyms of words

from nltk.corpus import wordnet as wn

def getsynList(word):  #find the synset list of a word
        syns = wn.synsets(word)
        lemmas = [s.lemma_names for s in syns]
        synlist = list(set([item for sublist in lemmas for item in sublist]))
        return synlist

def gethypSet(word):  #find the hyponyms set of a word
        lst = [synset.hyponyms() for synset in wn.synsets(word)]
        hyplist = [item for sublist in lst for item in sublist]
        hypfinallist = [w.lemma_names for w in hyplist]
        hypFianlList = [item for sublist in hypfinallist for item in sublist]
        return hypFianlList

def gethyperSet(word):
        lst = [synset.hypernyms() for synset in wn.synsets(word)]
        hyperlist = [item for sublist in lst for item in sublist]
        hyperfinallist = [w.lemma_names for w in hyperlist]
        hyperFianlList = [item for sublist in hyperfinallist for item in sublist]
        return hyperFianlList
