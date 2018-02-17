import bottle
import os
import random


# Testing to see if server is running

#@bottle.route('/')
#def static():
#   return "the server is running"
#

def distance(start, object):
	# number of moves away from an object
	
	distance_x = abs(int(start[0]) - int(object[0]));
	distance_y = abs(int(start[1]) - int(object[1]));
	
	return distance_x + distance_y;
	
def direction(fromdir, todir):
	# returns the direction up/down and left/right
	
	distance_x = int(fromdir[0]) - int(todir[0]);
	distance_y = int(fromdir[1]) - int(todir[1]);
	
	if (distance_x == 1):
		return 'right'
	
	elif (distance_x == -1):
		return 'left'
		
	elif (distance_y == 1):
		return 'up'
		
	elif (distance_y == -1):
		return 'down'
	
def closest_food(snake_head, finish):
	# Gives the coordinates of the closest food to the head of the snake
	return 0
	
def walls():
	# Returns the dimensions of the grid
	return 0
	
def closest_snake_head():
	# Returns the closest positions to a snake head
	return 0
	
def closest_snake():
	# Returns the closest position of snake head/body/tail
	return 0
	
def path_to_food():
	# Return the desired path to food
	# When small we want the quickest and least dangerous path to the food
	# When large we want to make the path hug our tail / essentially set up traps before going to next food
	return 0
	
def initialize_grid(data):
	# Return Grid
	# Link our snake + put snakes on the grid
	# Set up boundaries (walls)
	# Put food on the grid
	
	gameboard = [[0 for column in xrange(data['height'])for row in xrange(data['width'])]]
	
	for w in data['width']:
		for h in data['height']:
			
			gameboard[wall[0]][wall[h]] = 1 # 1 = wall
			gameboard[wall[len(data['width'])]-1][wall[h]] = 1
			gameboard[wall[w]][wall[0]] = 1
			gameboard[wall[w]][wall[len(data['height'])-1]] = 1
		
	for f in data['food']:
		gameboard[f[0]][f[1]] = 2 # 2 = food
	
	for s in data['snakes']:
		if s['id'] == our_snake_id:
			our_snake = s
	
		for c in s['coords']:
			gameboard[c[0]][c[1]] = 3 # 3 = snake
	
	return gameboard, our_snake;


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

	# Link picture to represent our snake
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#007F00', 
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'Zaddy',
		'head_type': 'smile',
		'tail_type': 'fat-rattle',
		'secondary_color': '#4B0082'
		
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data
	# Priorities: 
	# 1. Avoid walls
	# 2. Eat food / Don't starve
	# 3. Avoid turning too close to other snakes and ourselves (if distance to other snake body/head = 2, go in opposite direction)
	# 4. Avoid head on collisions unless big
	# 4. Locate and acquire nearest food

    gameboard, zad_snake = initialize_grid(data)
    r = random.randint()
	
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
    
    directions = ['up', 'down', 'left', 'right']
    #direction = random.choice(directions)
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
