import random
from SerializationUtils import getDirectionFromTuple

HEAD_PERIMETER_WEIGHT = 3
FOOD_WEIGHT = 2

TRAPPED_WEIGHT = 10

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
	print('Next move:', getDirectionFromTuple(directionTuple), ',coord:', snakeBoard.playerSnake.getNextPosition(directionTuple))
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
		weightList[i] += getSmallTrapAvoidanceWeight(nextMoveCoord, snakeBoard)
		# TODO weight for 1 space trapping or free areas
		# TODO weight for closer to food if health is low

	print('Available Directions:    ', [getDirectionFromTuple(x) for x in availableDirectionTuples])
	print('Weights:                 ', weightList)
	return getHighestWeightedMoveCoord(availableDirectionTuples, weightList)

def getSmallerHeadPerimeterWeight(nextMoveCoord, snakeBoard):
	return snakeBoard.smallerHeadPerimeterCoords.count(nextMoveCoord) * HEAD_PERIMETER_WEIGHT

# Check if the coordinant is in the head perimeter of a snake of equal size
# We want to step in these spots if we are the only 2 snakes left, otherwise avoid it
def getEqualHeadPermiterWeight(nextMoveCoord, snakeBoard):
	if (snakeBoard.equalHeadPerimeterCoords.count(nextMoveCoord) > 0):
		if len(snakeBoard.enemySnakes) == 1:
			return HEAD_PERIMETER_WEIGHT
		else:
			return HEAD_PERIMETER_WEIGHT * -1
	else:
		return 0

def getBiggerHeadPerimeterWeight(nextMoveCoord, snakeBoard):
	return snakeBoard.biggerHeadPerimeterCoords.count(nextMoveCoord) * HEAD_PERIMETER_WEIGHT * -1

def getSmallTrapAvoidanceWeight(nextMoveCoord, snakeBoard):
	nextMovePerimeterCoords = snakeBoard.getCoordPerimeterCoords(nextMoveCoord)
	availableFutureMoves = []
	for move in nextMovePerimeterCoords:
		if isNextMoveCoordACollision(move, snakeBoard) == False:
			availableFutureMoves.append(move)
	if len(availableFutureMoves) == 0:
		print(nextMoveCoord, 'WILL BE A TRAP!!!!')
		return TRAPPED_WEIGHT * -1
	else:
		return 0

def getCollisionNeighboursInBoundary(nextMoveCoord, boundary, snakeBoard):
	collisionNeighbourCoords = []
	for i in range(boundary * -1, boundary + 1):
		for j in range(boundary * -1, boundary + 1):
			neighbourCoord = [nextMoveCoord[0] + i, nextMoveCoord[1] + j]
			if isNextMoveCoordACollision(neighbourCoord, snakeBoard):
				collisionNeighbourCoords.append(neighbourCoord)
	print('Debug colliding neighbours:', collisionNeighbourCoords)
	return collisionNeighbourCoords

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
	return isNextMoveCoordACollision(nextMoveCoord, snakeBoard)
	
def isNextMoveCoordACollision(nextMoveCoord, snakeBoard):
	if(snakeBoard.isNextMoveInAnySnake(nextMoveCoord)):
		print(nextMoveCoord, 'collides with a snake!')#
		return True
	if(snakeBoard.isNextMoveOutOfBounds(nextMoveCoord)):
		print(nextMoveCoord, 'collides with a wall!')#
		return True
	print(nextMoveCoord, 'is ok!')#
	return False