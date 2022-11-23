# FILE  : dfa.py
# Berisi source code program untuk mengecek apakah suatu nama variabel dapat dikenali dalam JavaScript

delta = [['start', 'else', 'dead'],
         ['start', 'number', 'dead'],
         ['start', 'lowerCase', 'final'],
         ['start', 'upperCase', 'final'],
         ['start', 'specialSign', 'final'],
         ['final', 'else', 'dead'],
         ['final', 'number', 'final'],
         ['final', 'lowerCase', 'final'],
         ['final', 'upperCase', 'final'],
         ['final', 'specialSign', 'final'],
         ['dead', 'else', 'dead'],
         ['dead', 'number', 'dead'],
         ['dead', 'lowerCase', 'dead'],
         ['dead', 'upperCase', 'dead'],
         ['dead', 'specialSign', 'dead']]

def convertInputSymbol(char):
    if (char in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']):
        return 'upperCase'
    elif (char in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']):
        return 'lowerCase'
    elif (char in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']):
        return 'number'
    elif (char in ['$', '_']):
        return 'specialSign'
    else:
        return 'else'

def transitions(currentState, inputSymbol):
    global delta

    for trans in delta:
        if (trans[0] == currentState and trans[1] == inputSymbol):
            return trans[2]

def checkWithDFA(varName):
    i = 0
    currentState = 'start'

    while (i < len(varName)):
        inputSymbol = convertInputSymbol(varName[i])
        currentState = transitions(currentState, inputSymbol)
        i += 1
    
    return currentState == 'final'