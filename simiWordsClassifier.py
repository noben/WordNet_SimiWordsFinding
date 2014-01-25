#functions for building the dictionary for homophones

#nltk lib, including pronunciation dictionary
import nltk
from nltk.corpus import cmudict
from nltk.corpus import wordnet as wn
import difflib

#-----------------------------------------------------------------------
#read the words from a txt file to a list
def readWords(wordsListNameTXT):

    '''read list named as 'gaokaocihui.txt, converting to a list'''
    
    with open(wordsListNameTXT, 'U') as f:
        wordList = [line.strip() for line in f]
    f.close()
    return wordList
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
#output dictionary to a dic file
def outputDict(dic_name):
    import pickle
    with open('wordDict', 'wb') as f:
        pickle.dump(dic_name, f)

#read dictionary pkl file
def readDict(file_name):
    import pickle
    with open(file_name, 'rb') as f:
        dic = pickle.load(f)
    return dic

#output dictionary to a txt file
def outDicTXT(dic_name, filename_txt):
    import json
    d = dic_name
    json.dump(d, open(filename_txt, 'w'))

def readDictJson(dic_name):
    import json
    dictionary = json.load(open(dic_name))
    return dictionary

def OutputDictLines(dic):
    f = open('GRE_WordsDictLines.txt', 'w')
    for i in dic.keys():
        f.write(repr(i))
        f.write(':  [')
        for n in dic[i]:
            f.write(' %s,'%(repr(n)))
        f.write(']')
        f.write('\n')
    f.close

def OutputDictForExcel(dic):
    f = open('TextForExcel.txt', 'w')
    for i in dic.keys():
        f.write(repr(i))
        f.write('\t')
        for n in dic[i]:
            f.write('%s\t'%(repr(n)))
        f.write('\n')
    f.close
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
#initiate a dictionary here for storing words and related words
wordsDict = nltk.defaultdict(list)

disturbingDict = nltk.defaultdict(list)

#initiate a pronunciation dictionary
prondict = cmudict.dict()
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
def GetHomoPhoneDict(wordList):

    '''Funtions with a list of words as input and a HomePhone words dictionary as out put'''
    
    for word1 in wordList:
        #three conditions for  judging if two words are similar#
        word1_len = len(word1)
        #1st condition: word length <= 4#
        if (word1_len <= 4):
            wordsDict[word1] = []
            if word1 in prondict:
                for word2 in wordList:
                    word2_len = len(word2)
                    abs_len = abs(word1_len - word2_len)
                    if word2 in prondict:
                        if (abs_len == 0):   #this argument needed to be considered/modified
                            exitFlag = False
                            sm_word = difflib.SequenceMatcher(None, word1, word2)
                            sm_word_rate = sm_word.ratio()
                            for s1 in prondict[word1]:
                                for s2 in prondict[word2]:
                                    sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                    sm_pron_rate = sm_pron.ratio()
                                    if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.65 or word1 != word2 and sm_word_rate >= 0.7):
                                        #push word2 into the dict with key word1
                                        wordsDict[word1].append(word2)
                                        exitFlag = True
                                        break
                                if exitFlag:
                                    break
                        elif (abs_len <=2):
                            #add if statement for judging if word1 in word2 OR word2 in word1 string
                            s1 = prondict[word1][0]
                            s2 = prondict[word2][0]
                            sm_pron = difflib.SequenceMatcher(None, s1, s2)
                            sm_pron_rate = sm_pron.ratio()
                            if ((word1 in word2 or word2 in word1) and sm_pron_rate > 0.45):
                                wordsDict[word1].append(word2)
                            else:
                                exitFlag = False
                                sm_word = difflib.SequenceMatcher(None, word1, word2)
                                sm_word_rate = sm_word.ratio()
                                for s1 in prondict[word1]:
                                    for s2 in prondict[word2]:
                                        sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                        sm_pron_rate = sm_pron.ratio()
                                        #a relatively big absolute length value requires more restricting arguments below
                                        if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.67 or word1 != word2 and sm_word_rate >= 0.75):
                                            #push word2 into the dict with key word1
                                            wordsDict[word1].append(word2)
                                            exitFlag = True
                                            break
                                    if exitFlag:
                                        break
                        else:
                            #add if statement for judging if word1 in word2 OR word2 in word1 string
                            s1 = prondict[word1][0]
                            s2 = prondict[word2][0]
                            sm_pron = difflib.SequenceMatcher(None, s1, s2)
                            sm_pron_rate = sm_pron.ratio()
                            if ((word1 in word2 or word2 in word1) and sm_pron_rate > 0.45):
                                wordsDict[word1].append(word2)
                            else:
                                exitFlag = False
                                sm_word = difflib.SequenceMatcher(None, word1, word2)
                                sm_word_rate = sm_word.ratio()
                                for s1 in prondict[word1]:
                                    for s2 in prondict[word2]:
                                        sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                        sm_pron_rate = sm_pron.ratio()
                                        #a relatively big absolute length value requires more restricting arguments below
                                        if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.7 or word1 != word2 and sm_word_rate >= 0.72):
                                            #push word2 into the dict with key word1
                                            wordsDict[word1].append(word2)
                                            exitFlag = True
                                            break
                                    if exitFlag:
                                        break
                    else:
                        if (abs_len == 0):
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.7):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
                        elif (abs_len > 0 and abs_len <= 2):
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.75):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
                        else:
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.72):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
            else:
                for word2 in wordList:
                    word2_len = len(word2)
                    abs_len = abs(word1_len - word2_len)
                    if (abs_len == 0):
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.7):
                            #push word2 in the dict with key word1
                            wordsDict[word1].append(word2)
                    elif (abs_len > 0 and abs_len <= 2):
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.75):
                            #push word2 into the dict with key word1
                            wordsDict[word1].append(word2)
                    else:
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.72):
                            #push word2 into the dict with key word1
                            wordsDict[word1].append(word2)
                        
        #2nd condition word length >4 and < 7#
        elif (word1_len > 4 and word1_len < 7):
            wordsDict[word1] = []
            if word1 in prondict:
                for word2 in wordList:
                    word2_len = len(word2)
                    abs_len = abs(word1_len - word2_len)
                    if word2 in prondict:
                        if (abs_len == 0):   #this argument needed to be considered/modified
                            exitFlag = False
                            sm_word = difflib.SequenceMatcher(None, word1, word2)
                            sm_word_rate = sm_word.ratio()
                            for s1 in prondict[word1]:
                                for s2 in prondict[word2]:
                                    sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                    sm_pron_rate = sm_pron.ratio()
                                    if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.65 or word1 != word2 and sm_word_rate >= 0.67):
                                        #push word2 into the dict with key word1
                                        wordsDict[word1].append(word2)
                                        exitFlag = True
                                        break
                                if exitFlag:
                                    break
                        elif (abs_len > 0 and abs_len <=2):
                            #add if statement for judging if word1 in word2 OR word2 in word1 string
                            s1 = prondict[word1][0]
                            s2 = prondict[word2][0]
                            sm_pron = difflib.SequenceMatcher(None, s1, s2)
                            sm_pron_rate = sm_pron.ratio()
                            if ((word1 in word2 or word2 in word1) and sm_pron_rate > 0.45):
                                wordsDict[word1].append(word2)
                            else:
                                exitFlag = False
                                sm_word = difflib.SequenceMatcher(None, word1, word2)
                                sm_word_rate = sm_word.ratio()
                                for s1 in prondict[word1]:
                                    for s2 in prondict[word2]:
                                        sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                        sm_pron_rate = sm_pron.ratio()
                                        #a relatively big absolute length value requires more restricting arguments below
                                        if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.67 or word1 != word2 and sm_word_rate >= 0.72):
                                            #push word2 into the dict with key word1
                                            wordsDict[word1].append(word2)
                                            exitFlag = True
                                            break
                                    if exitFlag:
                                        break
                        else:
                            #add if statement for judging if word1 in word2 OR word2 in word1 string
                            s1 = prondict[word1][0]
                            s2 = prondict[word2][0]
                            sm_pron = difflib.SequenceMatcher(None, s1, s2)
                            sm_pron_rate = sm_pron.ratio()
                            if ((word1 in word2 or word2 in word1) and sm_pron_rate > 0.45):
                                wordsDict[word1].append(word2)
                            else:
                                exitFlag = False
                                sm_word = difflib.SequenceMatcher(None, word1, word2)
                                sm_word_rate = sm_word.ratio()
                                for s1 in prondict[word1]:
                                    for s2 in prondict[word2]:
                                        sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                        sm_pron_rate = sm_pron.ratio()
                                        #a relatively big absolute length value requires more restricting arguments below
                                        if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.76 or word1 != word2 and sm_word_rate >= 0.75):
                                            #push word2 into the dict with key word1
                                            wordsDict[word1].append(word2)
                                            exitFlag = True
                                            break
                                    if exitFlag:
                                        break
                    else:
                        if (abs_len == 0):
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.67):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
                        elif (abs_len > 0 and abs_len <= 2):
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.72):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
                        else:
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.75):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
            else:
                for word2 in wordList:
                    word2_len = len(word2)
                    abs_len = abs(word1_len - word2_len)
                    if (abs_len == 0):
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.67):
                            #push word2 in the dict with key word1
                            wordsDict[word1].append(word2)
                    elif (abs_len > 0 and abs_len <= 2):
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.72):
                            #push word2 into the dict with key word1
                            wordsDict[word1].append(word2)
                    else:
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.75):
                            #push word2 into the dict with key word1
                            wordsDict[word1].append(word2)
        
        #3rd for words >= 7 and <= 9#
        elif (word1_len >= 7 and word1_len <= 9):
            wordsDict[word1] = []
            if word1 in prondict:
                for word2 in wordList:
                    word2_len = len(word2)
                    abs_len = abs(word1_len - word2_len)
                    if word2 in prondict:
                        if (abs_len == 0):   #this argument needed to be considered/modified
                            exitFlag = False
                            sm_word = difflib.SequenceMatcher(None, word1, word2)
                            sm_word_rate = sm_word.ratio()
                            for s1 in prondict[word1]:
                                for s2 in prondict[word2]:
                                    sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                    sm_pron_rate = sm_pron.ratio()
                                    if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.67 or word1 != word2 and sm_word_rate >= 0.71):
                                        #push word2 into the dict with key word1
                                        wordsDict[word1].append(word2)
                                        exitFlag = True
                                        break
                                if exitFlag:
                                    break
                        elif (abs_len > 0 and abs_len <=2):
                            #add if statement for judging if word1 in word2 OR word2 in word1 string
                            s1 = prondict[word1][0]
                            s2 = prondict[word2][0]
                            sm_pron = difflib.SequenceMatcher(None, s1, s2)
                            sm_pron_rate = sm_pron.ratio()
                            if ((word1 in word2 or word2 in word1) and sm_pron_rate > 0.45):
                                wordsDict[word1].append(word2)
                            else:
                                exitFlag = False
                                sm_word = difflib.SequenceMatcher(None, word1, word2)
                                sm_word_rate = sm_word.ratio()
                                for s1 in prondict[word1]:
                                    for s2 in prondict[word2]:
                                        sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                        sm_pron_rate = sm_pron.ratio()
                                        #a relatively big absolute length value requires more restricting arguments below
                                        if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.73 or word1 != word2 and sm_word_rate >= 0.75):
                                            #push word2 into the dict with key word1
                                            wordsDict[word1].append(word2)
                                            exitFlag = True
                                            break
                                    if exitFlag:
                                        break
                        else:
                            #add if statement for judging if word1 in word2 OR word2 in word1 string
                            s1 = prondict[word1][0]
                            s2 = prondict[word2][0]
                            sm_pron = difflib.SequenceMatcher(None, s1, s2)
                            sm_pron_rate = sm_pron.ratio()
                            if ((word1 in word2 or word2 in word1) and sm_pron_rate > 0.45):
                                wordsDict[word1].append(word2)
                            else:
                                exitFlag = False
                                sm_word = difflib.SequenceMatcher(None, word1, word2)
                                sm_word_rate = sm_word.ratio()
                                for s1 in prondict[word1]:
                                    for s2 in prondict[word2]:
                                        sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                        sm_pron_rate = sm_pron.ratio()
                                        #a relatively big absolute length value requires more restricting arguments below
                                        if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.75 or word1 != word2 and sm_word_rate >= 0.77):
                                            #push word2 into the dict with key word1
                                            wordsDict[word1].append(word2)
                                            exitFlag = True
                                            break
                                    if exitFlag:
                                        break
                    else:
                        if (abs_len == 0):
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.71):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
                        elif (abs_len > 0 and abs_len <= 2):
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.75):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
                        else:
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.77):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
            else:
                for word2 in wordList:
                    word2_len = len(word2)
                    abs_len = abs(word1_len - word2_len)
                    if (abs_len == 0):
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.71):
                            #push word2 in the dict with key word1
                            wordsDict[word1].append(word2)
                    elif (abs_len > 0 and abs_len <= 2):
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.75):
                            #push word2 into the dict with key word1
                            wordsDict[word1].append(word2)
                    else:
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.77):
                            #push word2 into the dict with key word1
                            wordsDict[word1].append(word2)

        #4th words length >9 and <= 12#
        elif (word1_len > 9 and word1_len <= 12):
            wordsDict[word1] = []
            if word1 in prondict:
                for word2 in wordList:
                    word2_len = len(word2)
                    abs_len = abs(word1_len - word2_len)
                    if word2 in prondict:
                        if (abs_len == 0):   #this argument needed to be considered/modified
                            exitFlag = False
                            sm_word = difflib.SequenceMatcher(None, word1, word2)
                            sm_word_rate = sm_word.ratio()
                            for s1 in prondict[word1]:
                                for s2 in prondict[word2]:
                                    sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                    sm_pron_rate = sm_pron.ratio()
                                    if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.67 or word1 != word2 and sm_word_rate >= 0.71):
                                        #push word2 into the dict with key word1
                                        wordsDict[word1].append(word2)
                                        exitFlag = True
                                        break
                                if exitFlag:
                                    break
                        elif (abs_len > 0 and abs_len <=2):
                            #add if statement for judging if word1 in word2 OR word2 in word1 string
                            s1 = prondict[word1][0]
                            s2 = prondict[word2][0]
                            sm_pron = difflib.SequenceMatcher(None, s1, s2)
                            sm_pron_rate = sm_pron.ratio()
                            if ((word1 in word2 or word2 in word1) and sm_pron_rate > 0.45):
                                wordsDict[word1].append(word2)
                            else:
                                exitFlag = False
                                sm_word = difflib.SequenceMatcher(None, word1, word2)
                                sm_word_rate = sm_word.ratio()
                                for s1 in prondict[word1]:
                                    for s2 in prondict[word2]:
                                        sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                        sm_pron_rate = sm_pron.ratio()
                                        #a relatively big absolute length value requires more restricting arguments below
                                        if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.73 or word1 != word2 and sm_word_rate >= 0.75):
                                            #push word2 into the dict with key word1
                                            wordsDict[word1].append(word2)
                                            exitFlag = True
                                            break
                                    if exitFlag:
                                        break
                        else:
                            #add if statement for judging if word1 in word2 OR word2 in word1 string
                            s1 = prondict[word1][0]
                            s2 = prondict[word2][0]
                            sm_pron = difflib.SequenceMatcher(None, s1, s2)
                            sm_pron_rate = sm_pron.ratio()
                            if ((word1 in word2 or word2 in word1) and sm_pron_rate > 0.45):
                                wordsDict[word1].append(word2)
                            else:
                                exitFlag = False
                                sm_word = difflib.SequenceMatcher(None, word1, word2)
                                sm_word_rate = sm_word.ratio()
                                for s1 in prondict[word1]:
                                    for s2 in prondict[word2]:
                                        sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                        sm_pron_rate = sm_pron.ratio()
                                        #a relatively big absolute length value requires more restricting arguments below
                                        if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.75 or word1 != word2 and sm_word_rate >= 0.78):
                                            #push word2 into the dict with key word1
                                            wordsDict[word1].append(word2)
                                            exitFlag = True
                                            break
                                    if exitFlag:
                                        break
                    else:
                        if (abs_len == 0):
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.71):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
                        elif (abs_len > 0 and abs_len <= 2):
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.75):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
                        else:
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.78):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
            else:
                for word2 in wordList:
                    word2_len = len(word2)
                    abs_len = abs(word1_len - word2_len)
                    if (abs_len == 0):
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.71):
                            #push word2 in the dict with key word1
                            wordsDict[word1].append(word2)
                    elif (abs_len > 0 and abs_len <= 2):
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.75):
                            #push word2 into the dict with key word1
                            wordsDict[word1].append(word2)
                    else:
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.78):
                            #push word2 into the dict with key word1
                            wordsDict[word1].append(word2)

        #5th words length > 12#
        else:
            wordsDict[word1] = []
            if word1 in prondict:
                for word2 in wordList:
                    word2_len = len(word2)
                    abs_len = abs(word1_len - word2_len)
                    if word2 in prondict:
                        if (abs_len == 0):   #this argument needed to be considered/modified
                            exitFlag = False
                            sm_word = difflib.SequenceMatcher(None, word1, word2)
                            sm_word_rate = sm_word.ratio()
                            for s1 in prondict[word1]:
                                for s2 in prondict[word2]:
                                    sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                    sm_pron_rate = sm_pron.ratio()
                                    if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.67 or word1 != word2 and sm_word_rate >= 0.72):
                                        #push word2 into the dict with key word1
                                        wordsDict[word1].append(word2)
                                        exitFlag = True
                                        break
                                if exitFlag:
                                    break
                        elif (abs_len > 0 and abs_len <=2):
                            #add if statement for judging if word1 in word2 OR word2 in word1 string
                            s1 = prondict[word1][0]
                            s2 = prondict[word2][0]
                            sm_pron = difflib.SequenceMatcher(None, s1, s2)
                            sm_pron_rate = sm_pron.ratio()
                            if ((word1 in word2 or word2 in word1) and sm_pron_rate > 0.45):
                                wordsDict[word1].append(word2)
                            else:
                                exitFlag = False
                                sm_word = difflib.SequenceMatcher(None, word1, word2)
                                sm_word_rate = sm_word.ratio()
                                for s1 in prondict[word1]:
                                    for s2 in prondict[word2]:
                                        sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                        sm_pron_rate = sm_pron.ratio()
                                        #a relatively big absolute length value requires more restricting arguments below
                                        if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.73 or word1 != word2 and sm_word_rate >= 0.76):
                                            #push word2 into the dict with key word1
                                            wordsDict[word1].append(word2)
                                            exitFlag = True
                                            break
                                    if exitFlag:
                                        break
                        else:
                            #add if statement for judging if word1 in word2 OR word2 in word1 string
                            s1 = prondict[word1][0]
                            s2 = prondict[word2][0]
                            sm_pron = difflib.SequenceMatcher(None, s1, s2)
                            sm_pron_rate = sm_pron.ratio()
                            if ((word1 in word2 or word2 in word1) and sm_pron_rate > 0.45):
                                wordsDict[word1].append(word2)
                            else:
                                exitFlag = False
                                sm_word = difflib.SequenceMatcher(None, word1, word2)
                                sm_word_rate = sm_word.ratio()
                                for s1 in prondict[word1]:
                                    for s2 in prondict[word2]:
                                        sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                        sm_pron_rate = sm_pron.ratio()
                                        #a relatively big absolute length value requires more restricting arguments below
                                        if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.75 or word1 != word2 and sm_word_rate >= 0.78):
                                            #push word2 into the dict with key word1
                                            wordsDict[word1].append(word2)
                                            exitFlag = True
                                            break
                                    if exitFlag:
                                        break
                    else:
                        if (abs_len == 0):
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.72):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
                        elif (abs_len > 0 and abs_len <= 2):
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.76):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
                        else:
                            sm=difflib.SequenceMatcher(None, word1, word2)
                            simiRate = sm.ratio()
                            if (word1 != word2 and simiRate != 1 and simiRate >= 0.78):
                                #push word2 into the dict with key word1
                                wordsDict[word1].append(word2)
            else:
                for word2 in wordList:
                    word2_len = len(word2)
                    abs_len = abs(word1_len - word2_len)
                    if (abs_len == 0):
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.72):
                            #push word2 in the dict with key word1
                            wordsDict[word1].append(word2)
                    elif (abs_len > 0 and abs_len <= 2):
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.76):
                            #push word2 into the dict with key word1
                            wordsDict[word1].append(word2)
                    else:
                        sm=difflib.SequenceMatcher(None, word1, word2)
                        simiRate = sm.ratio()
                        if (word1 != word2 and simiRate != 1 and simiRate >= 0.78):
                            #push word2 into the dict with key word1
                            wordsDict[word1].append(word2)
    outDicTXT(wordsDict, 'all_words_Dict.txt')
    OutputDictForExcel(wordsDict)
    return wordsDict
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
def GetHomoPhoneDictOfWord(word1, wordList):

    '''Funtions with a list of words as input and a HomePhone words dictionary as out put'''

    wordsDict2 = nltk.defaultdict(list)
    wordsDict2[word1] = []
    word1_len = len(word1)
    if word1 in prondict:
        for word2 in wordList:
            word2_len = len(word2)
            if word2 in prondict:
                if (abs(word1_len - word2_len) <= 3):   #this argument needed to be considered/modified
                    exitFlag = False
                    sm_word = difflib.SequenceMatcher(None, word1, word2)
                    sm_word_rate = sm_word.ratio()
                    for s1 in prondict[word1]:
                        for s2 in prondict[word2]:
                            sm_pron = difflib.SequenceMatcher(None, s1, s2)
                            sm_pron_rate = sm_pron.ratio()
                            #try to modify here in the methods of change "or" to "and" for below:
                            if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.65 or word1 != word2 and sm_word_rate >= 0.8):
                                #push word2 into the dict with key word1
                                wordsDict2[word1].append(word2)
                                exitFlag = True
                                break
                        if exitFlag:
                            break
                else:
                    #add if statement for judging if word1 in word2 OR word2 in word1 string
                    if (word1 in word2 or word2 in word1):
                        wordsDict2[word1].append(word2)
                    else:
                        exitFlag = False
                        sm_word = difflib.SequenceMatcher(None, word1, word2)
                        sm_word_rate = sm_word.ratio()
                        for s1 in prondict[word1]:
                            for s2 in prondict[word2]:
                                sm_pron = difflib.SequenceMatcher(None, s1, s2)
                                sm_pron_rate = sm_pron.ratio()
                                #a relatively big absolute length value requires more restricting arguments below
                                if (word1 != word2 and sm_pron_rate != 1 and sm_pron_rate >= 0.66 or word1 != word2 and sm_word_rate >= 0.85):
                                    #push word2 into the dict with key word1
                                    wordsDict2[word1].append(word2)
                                    exitFlag = True
                                    break
                            if exitFlag:
                                break
            else:
                sm=difflib.SequenceMatcher(None, word1, word2)
                simiRate = sm.ratio()
                if (word1 != word2 and simiRate != 1 and simiRate >= 0.8):
                    #push word2 into the dict with key word1
                    wordsDict2[word1].append(word2)
    else:
        for word2 in wordList:
            sm=difflib.SequenceMatcher(None, word1, word2)
            simiRate = sm.ratio()
            if (word1 != word2 and simiRate != 1 and simiRate >= 0.8):
                #push word2 in the dict with key word1
                wordsDict2[word1].append(word2)
    return wordsDict2
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
#Get the derivationally related words list of a word
#This function is used for words list which may contain derivations (derivation elemination)
def FindDerivation(word):
    DerivationLst = []
    for i in wn.synsets(word):
        for j in i.lemmas:
            for k in j.derivationally_related_forms():
                DerivationLst.append(k.name)
    DeriveList = list(set(DerivationLst))
    return DeriveList
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
#Four functions for getting antonyms, synonyms, hypernym and hyponyms
def getsynList(word):  #get the synset list of a word
        syns = wn.synsets(word)
        lemmas = [s.lemma_names for s in syns]
        synlist = list(set([item for sublist in lemmas for item in sublist]))
        return synlist

def getantList(word):  #get the antonym list of a word
        antlist = []
        syns = wn.synsets(word)
        for synset in syns:
            synset_lemmas = synset.lemmas
            for lemma in synset_lemmas:
                for l in lemma.antonyms():
                    w = l.name
                    antlist.append(w)
                    antlist = list(set(antlist))
        return antlist
        
def gethypSet(word):  #get the hyponyms set of a word
        lst = [synset.hyponyms() for synset in wn.synsets(word)]
        hyplist = [item for sublist in lst for item in sublist]
        hypfinallist = [w.lemma_names for w in hyplist]
        hypFianlList = [item for sublist in hypfinallist for item in sublist]
        return hypFianlList

def gethyperSet(word): #get the hypernyms set of a word
        lst = [synset.hypernyms() for synset in wn.synsets(word)]
        hyperlist = [item for sublist in lst for item in sublist]
        hyperfinallist = [w.lemma_names for w in hyperlist]
        hyperFianlList = [item for sublist in hyperfinallist for item in sublist]
        return hyperFianlList
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
def DisturbingDict(wordList):
    for word1 in wordList:
        disturbingDict[word1] = []
        synlst = getsynList(word1)
        antlst = getantList(word1)
        hyplst = gethypSet(word1)
        hyperlst = gethyperSet(word1)
        
        for word2 in wordList:
            if (word1 != word2):
                if (word2 in synlst
                    or word2 in antlst
                    or word2 in hyplst
                    or word2 in hyperlst
                    or b_any(word2 in x for x in synlst)
                    or b_any(word2 in x for x in antlst)
                    or b_any(word2 in x for x in hyplst)
                    or b_any(word2 in x for x in hyperlst)):
                        disturbingDict[word].append(word2)
                        
    return final_list
#-----------------------------------------------------------------------      
