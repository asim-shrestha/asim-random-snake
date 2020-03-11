import random
from SerializationUtils import getTupleFromDirection

def getDirections():
    return ['up', 'down', 'left', 'right']
    
def getNextMove(snakeBoard):
    availableDirections = getDirections()
    direction = getRandomAvailableDirection(availableDirections)
    while(isNextDirectionACollision(direction, snakeBoard)):
        if(len(availableDirections) == 0):
            print('CHECKED ALL DIRECTIONS')
            break
        print('GETTING ANOTHER DIRECTION')
        direction = getRandomAvailableDirection(availableDirections)
    return direction

def getRandomAvailableDirection(availableDirections):
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