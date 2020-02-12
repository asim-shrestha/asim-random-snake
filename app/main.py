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
    print(json.dumps(data, indent=2))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = json.load(bottle.request.body)
    print('DEBUG DUMP', data)
    print('DEBUG GAME', data['game'])

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)

    return move_response(direction)

def getBodyCoordsFromData(data):
    body = data['you']['body']
    coordsList = []
    for coord in body:
        coordsList.append([coord['x'], coord['y']])
    print('DEBUG BODY:', body)
    print('DEBUG COORDS LIST:', coordsList)
    return coordsList

@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

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
