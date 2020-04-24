import random
from SerializationUtils import getTupleFromDirection

def getAllDirections():
    return ['up', 'down', 'left', 'right']
    
def getNextMove(snakeBoard):
    allDirections = getAllDirections()
    availableDirections = getAvailableDirections(snakeBoard)
    if(len(availableDirections) > 0):
        direction = getBestDirection(availableDirections, snakeBoard)
    else:
        getRandomDirection(allDirections)
    print('Next move:', direction)
    return direction

def getAvailableDirections(snakeBoard):
    allDirections = getAllDirections()
    availableDirections = []
    for direction in allDirections:
        if isNextDirectionACollision(direction, snakeBoard) == False:
            availableDirections.append(direction)
    return availableDirections

def getBestDirection(availableDirections, snakeBoard):
    weightList = [0] * len(availableDirections)
    print('Available Directions:    ', availableDirections)
    print('Weights:                 ', weightList)
    return getHighestWeightedDirection(availableDirections, weightList)

def getHighestWeightedDirection(availableDirections, weightList):
    indexOfHighestWeight = weightList.index(max(weightList))
    return availableDirections[indexOfHighestWeight]

def getRandomDirection(availableDirections):
    nextDirection = random.choice(availableDirections)
    availableDirections.remove(nextDirection)
    return nextDirection

def isNextDirectionACollision(direction, snakeBoard):
    nextDirectionCoord = getTupleFromDirection(direction)
    nextMoveCoord = snakeBoard.playerSnake.getNextPosition(nextDirectionCoord)
    print('DEBUG NEXT MOVE COORD FOR DIRECTION:', direction, ' : ', nextMoveCoord)
    if(snakeBoard.isNextMoveInAnySnake(nextMoveCoord)):
        print('DIRECTION COLLIDES WITH A SNAKE')#
        return True
    if(snakeBoard.isNextMoveOutOfBounds(nextMoveCoord)):
        print('DIRECTION OUT OF BOUNDS')
        return True
    print('DIRECTION IS OKAY')
    return False