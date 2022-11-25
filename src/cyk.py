import numpy as np
from tes import CFG

def findRules(charItem):
	rulesFound = []
	with open("cnf.txt", "r") as cfg:
		rules = cfg.readlines()
	
	for i, rule in enumerate(rules):
		rule = rule.replace("->", "").split()
		if len(rule) == 3:
			if (rule[1] + " " + rule[2] == charItem):
				rulesFound.append(rule[0])
		else:
			if (rule[1] == charItem):
				rulesFound.append(rule[0])

	return rulesFound

def initArray(tWORD):
	length = len(tWORD)
	height = length
	tArray = np.zeros([height, length], list)
	return tArray

def parseFirst(tWORD, array):
	length = len(tWORD)
	height = length

	for i in range(length):
		findC = tWORD[i]
		foundC = findRules(findC)
		array[0][i] = foundC

	return array

def getDiag(array, possibleProductions, currentLength, currentHeight, length, i, diagList):

	indexDiagLenght = currentHeight + currentLength
	indexDiagHeight = 0
	for diagLoopIndex in range(currentHeight):
		tempDiag = array[indexDiagHeight][indexDiagLenght]
		if(tempDiag == 0):
			tempDiag = ['EMPTY']
			diagList.append(tempDiag)
		else:
			diagList.append(tempDiag)
		#MOVE DIAG LEFT UP
		indexDiagLenght = indexDiagLenght - 1
		indexDiagHeight = indexDiagHeight + 1
	return diagList



def getDown(array, possibleProductions, currentHeight, currentLength):
	for indexHeight in range(currentHeight):
		tempSignal = array[indexHeight][currentLength]
		if(tempSignal == 0):
			possibleProductions.append(['EMPTY'])
		else:
			possibleProductions.append(tempSignal)
	possibleProductions.reverse()
	return possibleProductions


def checkCombinations(array, possibleProductions, diagList, currentLength, currentHeight):
	rulesFound = []
	for i in range(len(possibleProductions)):
		for u in range(len(possibleProductions[i])):
			tempPos = possibleProductions[i][u]
			for h in range(len(diagList[i])):
				tempDiag = diagList[i][h]
				if(tempPos == 'EMPTY'):
					dummy = 9
				elif(tempDiag == 'EMPTY'):
					dummy = 9
				else:
					searchC = ''.join(item for item in tempPos + " " +  tempDiag)
					with open("cnf.txt", "r") as cfg:
						rules = cfg.readlines()
					for temp, rule in enumerate(rules):
						rule = rule.replace("->", "").split()
						if len(rule) == 3:
							if (rule[1] + " " + rule[2] == searchC):
								rulesFound.append(rule[0])
					
	if(len(rulesFound) == 0):
		return array
	else:
		array[currentHeight][currentLength] = rulesFound
		return array


def parse(tWORD, array, i):
	length = len(tWORD)
	currentHeight = i
	widthLength = length - i
	for currentLength in range(widthLength):
		possibleProductions = []
		diagList = []
		possibleProductions = getDown(array, possibleProductions, currentHeight, currentLength)
		diagList = getDiag(array, possibleProductions, currentLength, currentHeight, length, i, diagList)
		array = checkCombinations(array, possibleProductions, diagList, currentLength, i)

	return array