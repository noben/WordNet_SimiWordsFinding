#Filename: words_list.py
#input the txt file of vocabularys, generate the list of words

def words_in():

    '''read list named as 'gaokaocihui.txt'''
    
    with open('gaokaocihui.txt', 'U') as f:
        wordList = [line.strip() for line in f]
    f.close()
    return wordList

def output_ordered_list(final_list):

    '''output the result words list to txt file, named as OrderedWordsList'''
    
    finalList = ' -> '.join(final_list)
    open('test1.txt','w').write(finalList)

def save_words_list(lst):

    '''input the list to a txt file'''
    
    from cPickle import dump
    output = open('cihuiList.txt', 'wb')
    dump(lst, output, -1)
    output.close()

def get_words_list():

    '''get the saved list'''
    
    from cPickle import load
    infile = open('cihuiList.txt', 'rb')
    List = load(infile)
    infile.close()
    return List
