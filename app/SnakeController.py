import random
from SerializationUtils import getDirectionFromTuple

def getDirectionTuples():
	# Up. down, left, right
	return [[0,-1],[0,1],[-1,0],[1,0]]
	
def getNextMove(snakeBoard):
	allDirectionTuples = getDirectionTuples()
	availableDirectionTuples = getAvailableDirectionTuples(snakeBoard)
	if(len(availableDirectionTuples) > 0):
		directionTuple = getBestDirectionTuple(availableDirectionTuples, snakeBoard)
	else:
		getRandomListValue(allDirectionTuples)
	print('Next move:', getDirectionFromTuple(directionTuple))
	return getDirectionFromTuple(directionTuple)

def getAvailableDirectionTuples(snakeBoard):
	allDirectionTuples = getDirectionTuples()
	availableDirectionTuples = []
	for directionTuple in allDirectionTuples:
		if isDirectionTupleACollision(directionTuple, snakeBoard) == False:
			availableDirectionTuples.append(directionTuple)
	return availableDirectionTuples

def getBestDirectionTuple(availableDirectionTuples, snakeBoard):
	weightList = [0] * len(availableDirectionTuples)
	for i in range(len(availableDirectionTuples)):
		nextMoveCoord = snakeBoard.playerSnake.getNextPosition(availableDirectionTuples[i])
		weightList[i] += getBiggerHeadPerimeterWeight(nextMoveCoord, snakeBoard.biggerHeadPerimeterCoords)

	print('Available Directions:    ', [getDirectionFromTuple(x) for x in availableDirectionTuples])
	print('Weights:                 ', weightList)
	return getHighestWeightedMoveCoord(availableDirectionTuples, weightList)

def getBiggerHeadPerimeterWeight(nextMoveCoord, biggerHeadPerimeterCoords):
	print('COUNT of coords', biggerHeadPerimeterCoords.count(nextMoveCoord))
	return biggerHeadPerimeterCoords.count(nextMoveCoord) * -1

def getHighestWeightedMoveCoord(availableMoveCoords, weightList):
	# Get the index with the highest weight
	# If there are multiple, one of the options is randomly selected
	highestWeight = max(weightList)
	while True:
		randomIndex = random.randint(0, len(weightList) - 1)
		if weightList[randomIndex] == highestWeight:
			indexOfHighestWeight = randomIndex
			break
	
	return availableMoveCoords[indexOfHighestWeight]

def getRandomListValue(choicesList):
	return random.choice(choicesList)

def isDirectionTupleACollision(directionTuple, snakeBoard):
	nextMoveCoord = snakeBoard.playerSnake.getNextPosition(directionTuple)
	print('Next move coord for direction:', getDirectionFromTuple(directionTuple), ' : ', nextMoveCoord)
	if(snakeBoard.isNextMoveInAnySnake(nextMoveCoord)):
		print(getDirectionFromTuple(directionTuple), 'collides with a snake!')#
		return True
	if(snakeBoard.isNextMoveOutOfBounds(nextMoveCoord)):
		print(getDirectionFromTuple(directionTuple), 'collides with a wall!')#
		return True
	print(getDirectionFromTuple(directionTuple), 'is ok!')#
	return False