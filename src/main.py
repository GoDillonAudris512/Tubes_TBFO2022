# File      : main.py
# Berisi source code program utama untuk menjalankan JavaScript syntax checker

from os.path import isfile 
# KAMUS
isAccepted = False
listOfLine = []

# PROGRAM UTAMA
print("==============================")
print("Welcome to Syntax Checker ehe")
print("==============================\n")
print("Please input your JavaScript file and CFG file")
inputFileName = input("Insert JavaScript file name to be checked:  ")
rulesFilename = input("Insert CFG file name: ")

if (isfile(f'test/{inputFileName}')) :
    with open(f'test/{inputFileName}', 'r') as jsFile :
        listOfLine = jsFile.readlines() 

print("\n==============================")
print(listOfLine)
print("==============================\n")

print("Result: ", end = '')
if(isAccepted):
    print("Code accepted.")
else:
    print("Code error")
    print("    >>> At: ", end = '')