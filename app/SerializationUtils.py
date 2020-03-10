def serializeCoordsFromCoordList(coordsList):
        coords = []
        for coord in coordsList:
            coords += [coord['x'], coord['y']]
        return coords

def getTupleFromDirection(direction):
    if( direction == 'up'):
        return [0,-1]
    elif( direction == 'down'):
        return [0,1]
    elif( direction == 'left'):
        return [-1,0]
    else:
        return [1,0]