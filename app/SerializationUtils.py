def serializeCoordsFromCoordList(coordsList):
        coords = []
        for coord in coordsList:
            coords.append([coord['x'], coord['y']])
        return coords

def getDirectionFromTuple(tuple):
    if tuple[0] == 0 and tuple[1] == -1:
        return 'up'
    if tuple[0] == 0 and tuple[1] == 1:
        return 'down'
    if tuple[0] == -1 and tuple[1] == 0:
        return 'left'
    if tuple[0] == 1 and tuple[1] == 0:
        return 'right'

def getTupleFromDirection(direction):
    if( direction == 'up'):
        return [0,-1]
    elif( direction == 'down'):
        return [0,1]
    elif( direction == 'left'):
        return [-1,0]
    else:
        return [1,0]