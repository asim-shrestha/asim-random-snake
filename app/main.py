import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    # print(json.dumps(data, indent=2))
    print('STARTING GAME')

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    # Retrieve data
    data = json.load(bottle.request.body)
    # print('DEBUG DUMP', data)

    # Find walls
    walls = getBodyCoordsFromData(data)

    # Get random direction
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    directions.remove(direction)
    # Ensure it isn't in a wall
    while(isNextMoveInWall(direction, walls)):
        if(len(directions) == 0):
            print('CHECKED ALL DIRECTIONS')
            break
        print('GETTING ANOTHER DIRECTION')
        direction = random.choice(directions)
        directions.remove(direction)

    return move_response(direction)

def getBodyCoordsFromData(data):
    body = data['you']['body']
    coordsList = []
    for coord in body:
        coordsList.append([coord['x'], coord['y']])
    print('DEBUG BODY:', body)
    print('DEBUG COORDS LIST:', coordsList)
    return coordsList

def isNextMoveInWall(direction, walls):
    currentPos = walls[0]
    nextMoveCoord = getCoordFromDirection(direction, currentPos)
    print('DEBUG NEXT MOVE COORD FOR DIRECTION:', direction, ' : ', nextMoveCoord)
    for wall in walls:
        if(wall[0] == nextMoveCoord[0] and  wall[1] == nextMoveCoord[1]):
            print('DIRECTION IN PLAYER WALL')
            return True
    if(isNextMoveOutOfBounds(nextMoveCoord)):
        print('DIRECTION OUT OF BOUNDS')
        return True
    print('DIRECTION IS GUCCI')
    return False

def getCoordFromDirection(direction, currentPos):
    # Add direction positions to current position
    moveTuple = getTupleFromDirection(direction)
    return[ currentPos[0] + moveTuple[0], currentPos[1] + moveTuple[1] ]

def getTupleFromDirection(direction):
    if( direction == 'up'):
        return [0,-1]
    elif( direction == 'down'):
        return [0,1]
    elif( direction == 'left'):
        return [-1,0]
    else:
        return [1,0]

def isNextMoveOutOfBounds(nextMoveCoord):
    if(nextMoveCoord['x'] < 0 or nextMoveCoord['x'] > 10):
        return True
    if(nextMoveCoord['y'] < 0 or nextMoveCoord['y'] > 10):
        return True
    return False

@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    # print(json.dumps(data))
    print('GAME OVER')

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '5000'),
        debug=os.getenv('DEBUG', True)
    )
