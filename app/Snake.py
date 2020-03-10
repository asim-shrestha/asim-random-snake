from SerializationUtils import serializeCoordsFromCoordList

class Snake:
    def __init__(self, snake):
        self.id = snake['id']
        self.health = snake['health']
        self.coords = serializeCoordsFromCoordList(snake['body'])
        self.head = self.coords[0]
        self.length = len(self.coords)
    
    def getHead(self):
        return self.coords[0]