
import bottle
import os
import random



@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with datasssss

    return {
        'color': '#00F700',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python',
		'head_type': 'smile',
		'tail_type': 'fat-rattle',
		'secondary_color': '#4B0082'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data
    
    directions = ['up', 'down', 'left', 'right']
	
    for w in data['width']:
        for h in data['height']:
            if zad_snake['coords'][0] == [0,h]:
		 	# Change so it wont run into itself
                if zad_snake['coords'][1] == [1,h]:	
                    if (r % 2) == 0:
                        direction = 'up'
                    else:
                        direction = 'down'
			
            if (zad_snake['coords'][0] == [len(zad_snake['width'])-1, h]):
                if (zad_snake['coords'][1] == [len(zad_snake['width'])-2, h]):
                    if (r % 2) == 0:
                        direction = 'up'
                    else:
                        direction = 'down'
					
            if zad_snake['coords'][0] == [w, len(zad_snake[height])-1]:
                if zad_snake['coords'][1] == [w, len(zad_snake[height])-2]:
                    if (r % 2) == 0:
                        direction = 'right'
                    else:
                        direction = 'left'
					
            if zad_snake['coords'][0] == [w, 0]:
                if zad_snake['coords'][1] == [w, 1]:
                    if (r % 2) == 0:
                        direction = 'right'
                    else:
                        direction = 'left'
	
    print direction
    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)