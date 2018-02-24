
import bottle
import os
import random

global directions

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
        'color': '#800080',
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
	# Calculate the average position of enemy snakes and move away if smaller
    
    directions = ['up', 'down', 'left', 'right']
	
	# Snake head position
    snakehead_x = int(data['you']['body']['data'][0]['x'])
    snakehead_y = int(data['you']['body']['data'][0]['y'])
    
	# Most recent food position 
    food_x = int(data['food']['data'][0]['x'])
    food_y = int(data['food']['data'][0]['y'])
	
    # Probably don't need list2
    snake_food = []
    list = []
    list2 = []
    priority = []
	
	# Loop that finds all the food available
    for f in data['food']['data']:
	    f_x = f['x']
	    f_y = f['y']
	    snake_food.append([f_x, f_y])
	
	
	# List that finds all of your coordinates as the snake
    for item in data['you']['body']['data']:
		# Could include length
        xcoor = item['x']
        ycoor = item['y']
        list.append([xcoor, ycoor])
	
    # Checks to see if direction to the up, down, left, right is in the list
    for c1 in list:
	    if [snakehead_x, snakehead_y - 1] in list:
		    list2.append([snakehead_x, snakehead_y - 1])
		    priority.append(['d', 100])
		    break
			
    for c2 in list:
	    if [snakehead_x - 1, snakehead_y] in list:
		    list2.append([snakehead_x - 1, snakehead_y])
		    priority.append(['l', 100])
		    break

    for c3 in list:
	    if [snakehead_x + 1, snakehead_y] in list:
		    list2.append([snakehead_x + 1, snakehead_y])
		    priority.append(['r', 100])
		    break
			
    for c4 in list:
	    if [snakehead_x, snakehead_y + 1] in list:
		    list2.append([snakehead_x, snakehead_y + 1])
		    priority.append(['u', 100])
		    break
			
   
    width = data.get('width')
    height = data.get('height')
	
	# This will be the final check, we need to set priorities to 0 at the last step
    for j in range(0, width-1):
	    if [j, 0] in list:
		    # Direction is not down
		    priority.append(['d', 100])
	    elif [j, height - 1] in list:
			# Direction is not up
		    priority.append(['u', 100])
			
    for k in range(0, height-1):
	    if [0, k] in list:
		    # Direction is not left
		    priority.append(['l', 100])
	    elif [width - 1, k] in list:
			# Direction is not right
	        priority.append(['r', 100])
			
    if (snakehead_x > food_x):
        # direction = 'left';
		#priority.append(['u', 30])
		#priority.append(['d', 30])
		priority.append(['u', 30])
		
    elif (snakehead_x < food_x):
        # direction = 'right'
		#priority.append(['u', 30])
		#priority.append(['d', 30])
		priority.append(['d', 30])
		
    elif (snakehead_y > food_y):
        # direction = 'up'
		#priority.append(['l', 30])
		priority.append(['r', 30])
		#priority.append(['r', 30])
		
    elif (snakehead_y < food_y):
        # direction = 'down'
		priority.append(['l', 30])
		#priority.append(['l', 30])
		#priority.append(['r', 30])
    
    direction = direction_choice(priority)
    print list2
    print direction
    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }
	
def direction_choice(priority):
    up = 1
    down = 2
    right = 3
    left = 4
	
    for i in range(0, int(len(priority)) - 1):
	    if priority[i][0] == 'u':
		    up += int(priority[i][1])
		
	    elif priority[i][0] == 'd':
		    down += int(priority[i][1])
			
	    elif priority[i][0] == 'right':
		    right += int(priority[i][1])
			
	    else:
		    left += int(priority[i][1])
			
    print up
    print down
    print right
    print left
	
    if (up < left and up < right and up < down):
	    return 'up'
	
    elif (down < left and down < right and down < up):
	    return 'down'
		
    elif (left < down and left < right and left < up):
	    return 'left'
		
    else:
	    return 'right'
		
    

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)