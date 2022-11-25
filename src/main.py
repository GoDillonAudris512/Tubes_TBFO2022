# File      : main.py
# Berisi source code program utama untuk menjalankan JavaScript syntax checker
from os.path import isfile 
import argparse

from dfa import *
from cyk import *
from tes import *
#from cfg_to_cnf import *
from terminalConverter import *

# KAMUS 
isAccepted = True
isComment = False
isVarNameValid = True
errorFlag = 0
conditionalLevel = []
waitingIF = False
ableToElse = False
loopLevel = []
waitingLOOP = False
ableToBreak = False
waitingFUNC = False
switchLevel = []
waitingSWITCH = False
ableToDefault = False
stackOfCurlyBrackets = []
string = ""
table = [[]]
stackOfString =[]
valid = True

# PROGRAM UTAMA
argument = argparse.ArgumentParser() 
argument.add_argument('fileName', action='store')
args = argument.parse_args()

fileName = str(args.fileName)

if (not isfile(f'test/{fileName}')):
    print('Error: Cannot open the file specified in argument')
else:
    convert_grammar(read_grammar(r"cfg2.txt"))
    with open(f'test/{fileName}', 'r') as inputFile:
        lines = inputFile.readlines()
    
    # Menghapus karakter newline, semicolon, indentasi, dan line kosong
    for i, line in enumerate(lines):
        if (line.endswith('\n')):
            lines[i] = line[:len(line)-1]
    
    for i, line in enumerate(lines):
        if (line.endswith(';')):
            lines[i] = line[:len(line)-1]
        
    for i, line in enumerate(lines):
        if (line.startswith(" ")):
            temp = line
            while (temp.startswith(" ")):
                lines[i] = lines[i][1:]
                temp = temp[1:]

    i = 0
    pointerToState = 0
    while(isAccepted and errorFlag == 0 and i < len(lines)):
        if(lines[i] != ""):
            terminalsOfCode, varNameToCheck = convertToTerminal(lines[i])

            if ("'DOUBLE_SLASH'" in terminalsOfCode):
                terminalsOfCode = terminalsOfCode[:terminalsOfCode.index("'DOUBLE_SLASH'")]
            
            if ("'OPEN_SLASH'" in terminalsOfCode):
                isComment = True
            
            if ("'CLOSE_SLASH'" in terminalsOfCode):
                if (isComment):
                    terminalsOfCode = terminalsOfCode[terminalsOfCode.index("'CLOSE_SLASH'")+1:]
                    isComment = False
                else:
                    isAccepted = False
                    errorFlag = 10
                    break
            
            if (isComment):
                terminalsOfCode = []

            if (terminalsOfCode != []):
                height = len(terminalsOfCode) - 1
                table = initArray(terminalsOfCode)
                table = parseFirst(terminalsOfCode, table)
                for j in range(1, height+1):
                    table = parse(terminalsOfCode, table, j)
                print(table)
                if (table[height][0] == 0):
                    isAccepted = False
                    errorFlag = 7
                else:
                    for production in table[height][0]:
                        if (production == 'S'):
                            isAccepted = True
                            break
                        else:
                            isAccepted = False
                            errorFlag = 7
                            break

            if (isAccepted):
                if ("'CURFEW_CLOSE'" in terminalsOfCode and "'CURFEW_CLOSE'" == terminalsOfCode[0]):
                    if (len(stackOfCurlyBrackets) == 0):
                        isAccepted = False
                        errorFlag = 1
                        break
                    else:
                        if (len(stackOfCurlyBrackets) in conditionalLevel):
                            conditionalLevel.remove(len(stackOfCurlyBrackets))
                            ableToElse = True
                        elif (ableToElse):
                            ableToElse = False
                        
                        if (len(stackOfCurlyBrackets) in loopLevel):
                            loopLevel.remove(len(stackOfCurlyBrackets))
                            ableToBreak = loopLevel != [] 
                        
                        if (len(stackOfCurlyBrackets) in switchLevel):
                            switchLevel.remove(len(stackOfCurlyBrackets))
                            ableToDefault = switchLevel != [] 
                            ableToBreak = loopLevel != []

                        stackOfCurlyBrackets.pop()

                if ("'IF'" in terminalsOfCode and "'ELSE'" not in terminalsOfCode):
                    if (not waitingIF):
                        waitingIF = True
                    else:
                        isAccepted = False
                        errorFlag = 4
                        break
                
                if ("'ELSE'" in terminalsOfCode and "'IF'" in terminalsOfCode):
                    if (not ableToElse):
                        isAccepted = False
                        errorFlag = 2
                        break

                if ("'ELSE'" in terminalsOfCode and "'IF'" not in terminalsOfCode):
                    if (not ableToElse):
                        isAccepted = False
                        errorFlag = 2
                        break
                    else:
                        ableToElse = False
                
                if ("'SWITCH'" in terminalsOfCode):
                    if (not waitingSWITCH and len(switchLevel) < 1):
                        waitingSWITCH = True
                        ableToDefault = True
                    else:
                        isAccepted = False
                        errorFlag = 4
                        break
                
                if ("'CASE'" in terminalsOfCode):
                    if (switchLevel == []):
                        isAccepted = False
                        errorFlag = 6
                        break
                    else:
                        ableToBreak = True

                if ("'DEFAULT'" in terminalsOfCode):
                    if (switchLevel != [] and ableToDefault):
                        ableToDefault = False
                    else:
                        isAccepted = False
                        errorFlag = 6
                        break

                if ("'WHILE'" in terminalsOfCode or "'FOR'" in terminalsOfCode):
                    if (not waitingLOOP):
                        waitingLOOP = True
                    else:
                        isAccepted = False
                        errorFlag = 4
                        break

                if ("'FUNCTION'" in terminalsOfCode):
                    if (not waitingFUNC):
                        waitingFUNC = True
                    else:
                        isAccepted = False
                        errorFlag = 4
                        break

                if ("'CURFEW_OPEN'" in terminalsOfCode):
                    stackOfCurlyBrackets.append("{")
                    if ([waitingIF, waitingSWITCH, waitingFUNC, waitingLOOP].count(True) > 1):
                        isAccepted = False
                        errorFlag = 4
                        break
                    elif (waitingIF):
                        conditionalLevel.append(len(stackOfCurlyBrackets))
                        waitingIF = False
                    elif (waitingLOOP):
                        loopLevel.append(len(stackOfCurlyBrackets))
                        waitingLOOP = False
                        ableToBreak = True
                    elif (waitingFUNC):
                        waitingFUNC = False
                    elif (waitingSWITCH):
                        switchLevel.append(len(stackOfCurlyBrackets))
                        waitingSWITCH = False

                if ("'BREAK'" in terminalsOfCode):
                    if (ableToBreak):
                        ableToBreak = False
                    else:
                        isAccepted = False
                        errorFlag = 3     
                        break 

                if ("'CONTINUE'" in terminalsOfCode):
                    if (loopLevel == []):
                        isAccepted = False
                        errorFlag = 3
                        break  

                for var in varNameToCheck:
                    valid, stackOfString = checkWithDFA(var, stackOfString)
                    if (not valid):
                        isAccepted = False
                        errorFlag = 5
                        break
                
                if (stackOfString != []):
                    isAccepted = False
                    errorFlag = 5
                    break
                
                if ("'CURFEW_CLOSE'" in terminalsOfCode and "'CURFEW_CLOSE'" != terminalsOfCode[0]):
                    if (len(stackOfCurlyBrackets) == 0):
                        isAccepted = False
                        errorFlag = 1
                        break
                    else:
                        if (len(stackOfCurlyBrackets) in conditionalLevel):
                            conditionalLevel.remove(len(stackOfCurlyBrackets))
                            ableToElse = True
                        elif (ableToElse):
                            ableToElse = False
                        
                        if (len(stackOfCurlyBrackets) in loopLevel):
                            loopLevel.remove(len(stackOfCurlyBrackets))
                            ableToBreak = loopLevel != [] 
                        
                        if (len(stackOfCurlyBrackets) in switchLevel):
                            switchLevel.remove(len(stackOfCurlyBrackets))
                            ableToDefault = switchLevel != [] 
                            ableToBreak = loopLevel != []

                        stackOfCurlyBrackets.pop()
        i += 1

    if (errorFlag != 0 and errorFlag != 7):
        i += 1

    if (isAccepted):
        isAccepted = (stackOfCurlyBrackets == []) and (conditionalLevel == [])
        if (not isAccepted):
            errorFlag = 1

    if (isAccepted and errorFlag == 0):
        print("\033[93m{}\033[00m".format("Syntax accepted"))
    else:
        print("\033[93m{}\033[00m".format(f"Syntax error at line {i}"))
        print("\033[93m{}\033[00m".format("READED: "), end='')
        for terminal in terminalsOfCode:
            string = string + terminal.replace("'", "") + " "
        print("\033[93m{}\033[00m".format(string), end='')
        print("\n", end='')
        if (errorFlag == 1):
            print("\033[93m{}\033[00m".format("Error : Curly bracket not closed"))
        elif (errorFlag == 2):
            print("\033[93m{}\033[00m".format("Error : Else or else-if statement is not started by any if statements"))
        elif (errorFlag == 3):
            print("\033[93m{}\033[00m".format("Error : Break or continue statement not started by any while or loop or case statements"))
        elif (errorFlag == 4):
            print("\033[93m{}\033[00m".format("Error : If or switch or while or for or function statement is not separated by any curly brackets"))
        elif (errorFlag == 5):
            print("\033[93m{}\033[00m".format("Error : Variable name not permitted"))
        elif (errorFlag == 6):
            print("\033[93m{}\033[00m".format("Error : Case or default statements is not started by any switch statements"))
        elif (errorFlag == 7):
            print("\033[93m{}\033[00m".format("Error : Unknown symbol detected when parsing"))
        elif (errorFlag == 10):
            print("\033[93m{}\033[00m".format("Error : Unknown symbol detected. Possibly because comment formatting"))