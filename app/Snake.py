from SerializationUtils import serializeCoordsFromCoordList

class Snake:
    def __init__(self, snake):
        self.id = snake['id']
        self.health = snake['health']
        self.coords = serializeCoordsFromCoordList(snake['body'])
        self.length = len(self.coords)
    
    def getHead(self):
        return self.coords[0]

    def getNextPosition(self, nextMoveCoord):
        return [self.getHead()[0] + nextMoveCoord[0], self.getHead()[1] + nextMoveCoord[1]]