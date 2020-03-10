from Snake import Snake
from SerializationUtils import serializeCoordsFromCoordList

class SnakeBoard:
    def __init__(self, data):
        self.width = data['board']['width']
        self.height = data['board']['height']
        self.playerSnake = Snake(data['you'])
        self.enemySnakes = self.getEnemySnakes(data['board']['snakes'])
        self.foodCoords = serializeCoordsFromCoordList(data['board']['food'])

    def getEnemySnakes(self, snakeData):
        enemySnakes = []
        for snake in snakeData:
            if(snake['id'] != self.playerSnake.id):
                enemySnakes += Snake(snake)
        return enemySnakes

    def isNextMoveOutOfBounds(self, nextMoveCoord):
        # Test x cord
        nextHeadPosition = self.getNextHeadPosition(nextMoveCoord)
        if(nextHeadPosition[0] < 0 or nextHeadPosition[0] > self.width):
            return True
        # Test y cord
        if(nextHeadPosition[1] < 0 or nextHeadPosition[1] > self.height):
            return True
        return False
    
    def getNextHeadPosition(self, nextMoveCoord):
        print(self.playerSnake.getHead())
        print(self.playerSnake.coords)
        print(self.enemySnakes.coords)
        print(self.enemySnakes[0])
        print(self.enemySnakes[0].coords)
        return [self.playerSnake.getHead()[0] + nextMoveCoord[0], self.playerSnake.getHead()[1] + nextMoveCoord[1]]

    def isNextMoveInAnySnake(self, nextMoveCoord):
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
