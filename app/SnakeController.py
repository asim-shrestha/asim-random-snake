import random
from SerializationUtils import getDirectionFromTuple, getCoordPerimeterCoords

# Weights for heuristics
SMALLER_HEAD_PERIMETER_WEIGHT = 4
TIE_HEAD_PERIMETER_WEIGHT = 1
BIGGER_HEAD_PERIMETER_WEIGHT = 5
TRAPPED_WEIGHT = 10
BELOW_SNAKE_SIZE_WEIGHT = 5
ABOVE_POTENTIAL_TURN_REQUIREMENTS_WEIGHT = 1
# Size required for the snake to hunt for a tie
SIZE_REQUIRED_FOR_TIE = 5
# To determine if the snake should hunt for food
LENGTH_REQUIRED_TO_STOP_HUNTING_FOOD = 8
NUM_OF_MOVES_REQUIRED_TO_HUNT_NEAREST_FOOD = 3
STARVING_HEALTH = 45
STARVATION_LENGTH = 5
# For BFS
POTENTIAL_TURN_REQUIREMENTS = 15

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
		weightList[i] = getNextMoveCoordWeight(nextMoveCoord, snakeBoard)
	print('Available Directions:    ', [getDirectionFromTuple(x) for x in availableDirectionTuples])
	print('Weights:                 ', weightList)
	return getHighestWeightedMoveCoord(availableDirectionTuples, weightList)

def getNextMoveCoordWeight(nextMoveCoord, snakeBoard):
	weight = 0
	weight += getSmallerHeadPerimeterWeight(nextMoveCoord, snakeBoard)
	weight += getEqualHeadPermiterWeight(nextMoveCoord, snakeBoard)
	weight += getBiggerHeadPerimeterWeight(nextMoveCoord, snakeBoard)
	weight += getStarvationWeight(nextMoveCoord, snakeBoard)
	weight += getNearbyFoodWeight(nextMoveCoord, snakeBoard)
	weight += getBFSWeight(nextMoveCoord, snakeBoard)
	# TODO weight for 1 space trapping or free areas
	# TODO weight for closer to food if health is low
	return weight

def getSmallerHeadPerimeterWeight(nextMoveCoord, snakeBoard):
	return snakeBoard.smallerHeadPerimeterCoords.count(nextMoveCoord) * SMALLER_HEAD_PERIMETER_WEIGHT

# Check if the coordinant is in the head perimeter of a snake of equal size
# We want to avoid ties, DUBS ONLY
# Do not try to get a tie when you 
def getEqualHeadPermiterWeight(nextMoveCoord, snakeBoard):
	if (snakeBoard.equalHeadPerimeterCoords.count(nextMoveCoord) > 0):
		if len(snakeBoard.enemySnakes) == 1:
			return SIZE_REQUIRED_FOR_TIE * -1
		else:
			return SMALLER_HEAD_PERIMETER_WEIGHT * -1
	else:
		return 0

def getBiggerHeadPerimeterWeight(nextMoveCoord, snakeBoard):
	return snakeBoard.biggerHeadPerimeterCoords.count(nextMoveCoord) * BIGGER_HEAD_PERIMETER_WEIGHT * -1

def getStarvationWeight(nextMoveCoord, snakeBoard):
	# Player isn't starving, no need to prioritize food
	if snakeBoard.playerSnake.health > STARVING_HEALTH:
		return 0
	else:
		starvationWeight = STARVATION_LENGTH - snakeBoard.getNumMovesToNearestFood(nextMoveCoord)
		if starvationWeight < 0:
			starvationWeight = 0
		return starvationWeight

def getNearbyFoodWeight(nextMoveCoord, snakeBoard):
	# Check if the snake is already big enough
	if snakeBoard.playerSnake.length > LENGTH_REQUIRED_TO_STOP_HUNTING_FOOD:
		return 0
	
	numMovesToNearestFood = snakeBoard.getNumMovesToNearestFood(nextMoveCoord)
	print('num moves to nearest food', numMovesToNearestFood)
	if numMovesToNearestFood <= NUM_OF_MOVES_REQUIRED_TO_HUNT_NEAREST_FOOD:
		return NUM_OF_MOVES_REQUIRED_TO_HUNT_NEAREST_FOOD - numMovesToNearestFood
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

def getBFSWeight(coord, snakeBoard):
	cordsToCheckPerimeters = []
	checkedCoords = []
	availableCoords = []
	cordsToCheckPerimeters.append(coord)
	checkedCoords.append(coord)
	availableCoords.append(coord)
	potentialTurns = len(BFS(cordsToCheckPerimeters, checkedCoords, availableCoords, snakeBoard))
	print('Potential turns:', potentialTurns)
	if(potentialTurns >= POTENTIAL_TURN_REQUIREMENTS):
		return ABOVE_POTENTIAL_TURN_REQUIREMENTS_WEIGHT
	if(potentialTurns <= 1):
		return TRAPPED_WEIGHT * -1
	if(potentialTurns < snakeBoard.playerSnake.length):
		return BELOW_SNAKE_SIZE_WEIGHT * -1
	else:
		return 0

def BFS(cordsToCheckPerimeters, checkedCoords, availableCoords, snakeBoard):
	# No possible moves left
	if len(cordsToCheckPerimeters) == 0:
		return availableCoords
	
	# Check if we've already found a lot of potential turns
	if len(availableCoords) >= POTENTIAL_TURN_REQUIREMENTS:
		return availableCoords

	# Get coords we haven't tested yet
	cordPerimeters = getCoordPerimeterCoords(cordsToCheckPerimeters.pop(0))
	unCheckedCoords = []
	unCheckedCoords[:] = [coord for coord in cordPerimeters if coord not in checkedCoords]

	for coord in unCheckedCoords:
		checkedCoords.append(coord)
		if isNextMoveCoordACollision(coord, snakeBoard) == False:
			cordsToCheckPerimeters.append(coord)
			availableCoords.append(coord)
	# Test if we've checked already
	# Add to available 
	return BFS(cordsToCheckPerimeters, checkedCoords, availableCoords, snakeBoard)
	
		 
def isDirectionTupleACollision(directionTuple, snakeBoard):
	nextMoveCoord = snakeBoard.playerSnake.getNextPosition(directionTuple)
	return isNextMoveCoordACollision(nextMoveCoord, snakeBoard)
	
def isNextMoveCoordACollision(nextMoveCoord, snakeBoard):
	if(snakeBoard.isNextMoveInAnySnake(nextMoveCoord)):
		return True
	if(snakeBoard.isNextMoveOutOfBounds(nextMoveCoord)):
		return True
	return False