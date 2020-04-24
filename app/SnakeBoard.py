from Snake import Snake
from SerializationUtils import serializeCoordsFromCoordList

class SnakeBoard:
    def __init__(self, data):
        self.width = data['board']['width']
        self.height = data['board']['height']
        self.playerSnake = Snake(data['you'])
        self.enemySnakes = self.getEnemySnakes(data['board']['snakes'])
        self.biggerHeadPerimeterCoords = self.getBiggerHeadPerimeterCoords()
        self.foodCoords = serializeCoordsFromCoordList(data['board']['food'])
        print('Player coords', self.playerSnake.coords)
        print('Bigger head perimiters', self.biggerHeadPerimeterCoords)

    def getEnemySnakes(self, snakeData):
        enemySnakes = []
        for snake in snakeData:
            if(snake['id'] != self.playerSnake.id):
                enemySnakes.append(Snake(snake))
        return enemySnakes
    
    def getBiggerHeadPerimeterCoords(self):
        biggerHeadPerimetersCoords = []
        for snake in self.enemySnakes:
            if(snake.length >= self.playerSnake.length):
                biggerHeadPerimetersCoords.extend(self.getHeadPerimetersCoordsFromSnake(snake))
        return biggerHeadPerimetersCoords

    def getSmallerHeadPerimeterCoords(self):
        smallerHeadPerimeterCoords = []
        for snake in self.enemySnakes:
            if(snake.length < self.playerSnake.length):
                smallerHeadPerimeterCoords.extend(self.getHeadPerimetersCoordsFromSnake(snake))
        return smallerHeadPerimeterCoords

    def getHeadPerimetersCoordsFromSnake(self, snake):
        headPerimeterCoords = []
        snakeHeadCoord = snake.coords[0]
        headPerimeterCoords.append([snakeHeadCoord[0], snakeHeadCoord[1] - 1]) # Block above the head
        headPerimeterCoords.append([snakeHeadCoord[0], snakeHeadCoord[1] + 1]) # Block below the head
        headPerimeterCoords.append([snakeHeadCoord[0] - 1, snakeHeadCoord[1]]) # Block to the left of head
        headPerimeterCoords.append([snakeHeadCoord[0] + 1, snakeHeadCoord[1]]) # Block to the right of head
        return headPerimeterCoords

    def isNextMoveOutOfBounds(self, nextMoveCoord):
        # Test x cord
        if(nextMoveCoord[0] < 0 or nextMoveCoord[0] >= self.width):
            return True
        # Test y cord
        if(nextMoveCoord[1] < 0 or nextMoveCoord[1] >= self.height):
            return True
        return False

    def isNextMoveInAnySnake(self, nextMoveCoord):
        if(self.isNextMoveInSnake(nextMoveCoord, self.playerSnake)):
            print("COLLIDED WITH SELF")
            return True

        for snake in self.enemySnakes:
            if(self.isNextMoveInSnake(nextMoveCoord, snake)):
                print("COLLIDED WITH ENEMY SNAKE")
                return True
        return False
        
    def isNextMoveInSnake(self, nextMoveCoord, snake):
        # Skip last coordinant since it will dissapear next turn
        for snakeCoord in snake.coords[:-1]:
            if(nextMoveCoord[0] == snakeCoord[0] and nextMoveCoord[1] == snakeCoord[1]):
                return True
        return False
