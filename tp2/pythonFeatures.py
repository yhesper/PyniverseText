#editorFeatures
#######1. identify python keyword
#https://docs.python.org/3/library/keyword.html#keyword.kwlist
import keyword
#print(keyword.kwlist)
import string


def formedBySpace(s):
    for c in s:
        if c not in string.whitespace:
            return False
    return True
    
#seperate words by spaces. but if # occur, the rest of string is considered as one word.
def seperateWords(s):
    if s=='':
        return ['']
    wordList=[]
    currWord=s[0]
    if '#' not in s:
        for i in range(1,len(s)):
            nextChar=s[i]
            if not formedBySpace(currWord):
                if nextChar not in string.whitespace:
                    currWord=currWord+nextChar
                else:
                    wordList.append(currWord)
                    currWord=nextChar
            else:#currWord is white space
            
                if nextChar in string.whitespace:
                    currWord = currWord +nextChar
                else:
                    wordList.append(currWord)
                    currWord=nextChar
        wordList.append(currWord)
    else:
        i=s.find('#')
        for i in range (1,i):
            nextChar=s[i]
            if currWord not in string.whitespace:
                if nextChar not in string.whitespace:
                    currWord=currWord+nextChar
                else:
                    wordList.append(currWord)
                    currWord=nextChar
            else:#currWord is white space
                if nextChar in string.whitespace:
                    currWord = currWord +nextChar
                else:
                    wordList.append(currWord)
                    currWord=nextChar
        wordList.append(currWord)
        wordList.append(s[i+1:])
    return wordList


def isPythonKeyword(word):
    a=''
    for c in word:
        if c.isalnum():
            a=a+c
    return a in keyword.kwlist
    
#in draw function if is key word, change font
#isFunctionName
#isComment



def checkStyle(str):
    pass
    







