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
		directionTuple = getRandomListValue(allDirectionTuples)
	print('Next move:', getDirectionFromTuple(directionTuple), 'coord:' snakeBoard.playerSnake.getNextPosition(directionTuple))
	getLocalNeighbourhood(snakeBoard.playerSnake.getNextPosition(directionTuple))
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
		weightList[i] += getSmallerHeadPerimeterWeight(nextMoveCoord, snakeBoard)
		weightList[i] += getEqualHeadPermiterWeight(nextMoveCoord, snakeBoard)
		weightList[i] += getBiggerHeadPerimeterWeight(nextMoveCoord, snakeBoard)
		# TODO avoid head to head if tie more than 2 snakes in game
		# TODO weight for 1 space trapping or free areas
		# TODO weight for closer to food if health is low

	print('Available Directions:    ', [getDirectionFromTuple(x) for x in availableDirectionTuples])
	print('Weights:                 ', weightList)
	return getHighestWeightedMoveCoord(availableDirectionTuples, weightList)

def getSmallerHeadPerimeterWeight(nextMoveCoord, snakeBoard):
	return snakeBoard.smallerHeadPerimeterCoords.count(nextMoveCoord) * 1

# Check if the coordinant is in the head perimeter of a snake of equal size
# We want to step in these spots if we are the only 2 snakes left, otherwise avoid it
def getEqualHeadPermiterWeight(nextMoveCoord, snakeBoard):
	if (snakeBoard.equalHeadPerimeterCoords.count(nextMoveCoord) > 0):
		if len(snakeBoard.enemySnakes) == 1:
			return 1
		else:
			return -1
	else:
		return 0

def getBiggerHeadPerimeterWeight(nextMoveCoord, snakeBoard):
	return snakeBoard.biggerHeadPerimeterCoords.count(nextMoveCoord) * -1


def getLocalNeighbourhood(coord):
	NEIGHBOURHOOD_SIZE = 5
	BOUNDARY = int(NEIGHBOURHOOD_SIZE / 2)  # Gives us the floor
	localNeighbourhoodCoords = []
	for i in range(BOUNDARY * -1, BOUNDARY + 1):
		for j in range(BOUNDARY * -1, BOUNDARY + 1):
			localNeighbourhoodCoords.append([coord[0] + i, coord[1] + j])
	print('Debug local neighbourhood:', localNeighbourhoodCoords)
	return localNeighbourhoodCoords

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
	if(snakeBoard.isNextMoveInAnySnake(nextMoveCoord)):
		print(getDirectionFromTuple(directionTuple), 'collides with a snake!')#
		return True
	if(snakeBoard.isNextMoveOutOfBounds(nextMoveCoord)):
		print(getDirectionFromTuple(directionTuple), 'collides with a wall!')#
		return True
	print(getDirectionFromTuple(directionTuple), 'is ok!')#
	return False