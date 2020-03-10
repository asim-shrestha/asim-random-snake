import json
import os
import random
import bottle

from Snake import Snake
from SnakeBoard import SnakeBoard
from SerializationUtils import getTupleFromDirection
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
    snakeColour = getRandomColour
    
    return start_response(snakeColour)

def getRandomColour():
    return ("%06x" % random.randint(0, 0xFFFFFF))

@bottle.post('/move')
def move():
    # Retrieve data
    data = json.load(bottle.request.body)
    # print('DEBUG DUMP', data)

    snakeBoard = SnakeBoard(data)
    direction = getNextMove(snakeBoard)
    return move_response(direction)

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

def getDirections():
    return ['up', 'down', 'left', 'right']

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
