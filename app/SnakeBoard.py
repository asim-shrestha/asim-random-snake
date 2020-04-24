from Snake import Snake
from SerializationUtils import serializeCoordsFromCoordList, getCoordPerimeterCoords

class SnakeBoard:
	def __init__(self, data):
		# Data from request
		self.width = data['board']['width']
		self.height = data['board']['height']
		self.playerSnake = Snake(data['you'])
		self.enemySnakes = self.getEnemySnakes(data['board']['snakes'])
		self.foodCoords = serializeCoordsFromCoordList(data['board']['food'])
		# Head perimeters
		self.smallerHeadPerimeterCoords = self.getSmallerHeadPerimeterCoords()
		self.equalHeadPerimeterCoords = self.getEqualHeadPerimeterCoords()
		self.biggerHeadPerimeterCoords = self.getBiggerHeadPerimeterCoords()
		print('Player coords', self.playerSnake.coords)
		print('smaller head perimiters', self.smallerHeadPerimeterCoords)

	def getEnemySnakes(self, snakeData):
		enemySnakes = []
		for snake in snakeData:
			if(snake['id'] != self.playerSnake.id):
				enemySnakes.append(Snake(snake))
		return enemySnakes
	
	def getSmallerHeadPerimeterCoords(self):
		smallerHeadPerimeterCoords = []
		for snake in self.enemySnakes:
			if(snake.length < self.playerSnake.length):
				smallerHeadPerimeterCoords.extend(getCoordPerimeterCoords(snake.coords[0]))
		return smallerHeadPerimeterCoords

	def getEqualHeadPerimeterCoords(self):
		equalHeadPerimeterCoords = []
		for snake in self.enemySnakes:
			if snake.length == self.playerSnake.length:
				equalHeadPerimeterCoords.extend(getCoordPerimeterCoords(snake.coords[0]))
		return equalHeadPerimeterCoords

	def getBiggerHeadPerimeterCoords(self):
		biggerHeadPerimetersCoords = []
		for snake in self.enemySnakes:
			if(snake.length > self.playerSnake.length):
				biggerHeadPerimetersCoords.extend(getCoordPerimeterCoords(snake.coords[0]))
		return biggerHeadPerimetersCoords



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
			return True

		for snake in self.enemySnakes:
			if(self.isNextMoveInSnake(nextMoveCoord, snake)):
				return True
		return False
		
	def isNextMoveInSnake(self, nextMoveCoord, snake):
		# Skip last coordinant since it will dissapear next turn
		for snakeCoord in snake.coords[:-1]:
			if(nextMoveCoord[0] == snakeCoord[0] and nextMoveCoord[1] == snakeCoord[1]):
				return True
		return False

	def getNumMovesToNearestFood(self, moveCoord):
		if len(self.foodCoords) == 0:
			return 0
		
		# Loop through each food coord and find the minimum moves to food
		numMovesToNearestFood = self.getNumMovesToFoodCoord(moveCoord, self.foodCoords[0])
		for foodCoord in self.foodCoords:
			numMovesToNearestFood = min(numMovesToNearestFood, self.getNumMovesToFoodCoord(moveCoord, foodCoord))
		return numMovesToNearestFood
	
	def getNumMovesToFoodCoord(self, moveCoord, foodCoord):
		horizontalMoves = abs(moveCoord[0] - foodCoord[0])
		verticalMoves = abs(moveCoord[1] - foodCoord[1])
		return horizontalMoves + verticalMoves
