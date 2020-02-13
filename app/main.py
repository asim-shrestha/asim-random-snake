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
    print('DEBUG DUMP', data)

    # Find snakeCoords
    snakeCoords = getsnakeCoordsFromData(data)

    # Get random direction
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    directions.remove(direction)
    # Ensure it isn't in an obstacle
    while(isNextMoveACollision(direction, snakeCoords)):
        if(len(directions) == 0):
            print('CHECKED ALL DIRECTIONS')
            break
        print('GETTING ANOTHER DIRECTION')
        direction = random.choice(directions)
        directions.remove(direction)

    return move_response(direction)

def getsnakeCoordsFromData(data):
    playerId = data['you']['id']
    snakeCoords = []
    snakeCoords += getPlayerLocationsFromData(data)
    print('DEBUG PLAYER SNAKE LIST:', snakeCoords)
    snakeCoords += getOpponentsnakeCoordsFromData(data, playerId)
    print('ALL SNAKE LIST:', snakeCoords)
    return snakeCoords

def getPlayerLocationsFromData(data):
    playerSnake = data['you']['body']
    playerCoordsList = getCoordsFromSnakeBody(playerSnake)
    return playerCoordsList

def getOpponentsnakeCoordsFromData(data, playerId):
    allSnakeData = data['board']['snakes']
    opponentCoordsList = []
    for snake in allSnakeData:
        if(snake['id'] != playerId):
            snakeBody = snake['body']
            opponentCoordsList += getCoordsFromSnakeBody(snakeBody)
    return opponentCoordsList

def getCoordsFromSnakeBody(snake):
    coordsList = []
    for coord in snake:
        coordsList.append([coord['x'], coord['y']])
    return coordsList

def isNextMoveACollision(direction, snakeCoords):
    headCoord = snakeCoords[0]
    nextMoveCoord = getCoordFromDirection(direction, headCoord)
    print('DEBUG NEXT MOVE COORD FOR DIRECTION:', direction, ' : ', nextMoveCoord)
    for coord in snakeCoords:
        if(coord[0] == nextMoveCoord[0] and coord[1] == nextMoveCoord[1]):
            print('DIRECTION IN SNAKE')
            return True
    if(isNextMoveOutOfBounds(nextMoveCoord)):
        print('DIRECTION OUT OF BOUNDS')
        return True
    print('DIRECTION IS OKAY')
    return False

def getCoordFromDirection(direction, headCoord):
    # Add direction positions to current position
    nextMoveTuple = getTupleFromDirection(direction)
    return[ headCoord[0] + nextMoveTuple[0], headCoord[1] + nextMoveTuple[1] ]

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
    # Test x cord
    if(nextMoveCoord[0] < 0 or nextMoveCoord[0] > 10):
        return True
    # Test y cord
    if(nextMoveCoord[1] < 0 or nextMoveCoord[1] > 10):
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
