import bottle
import os
import random

global directions

global up
global down
global left
global right

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
        'color': '#23C1EB',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'Zad Acad Grad',
		'head_type': 'shades',
		'tail_type': 'curled',
		'secondary_color': '#DDA0DD'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data
	# Calculate the average position of enemy snakes and move away if smaller
	# Distance X*2 + distance y*2 from food 
	# Snakehead position within 2 spots, that takes priority
    
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
    
    food_timer = int(data['you']['health'])
	
	# Locate closest food
	# Loop that finds all the food available
	# locate and label closest food x, y
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
        
    for item2 in data['snakes']['data']:
		# Could include length
	for item3 in item2['body']['data'][: - 1]:
		xcoor = item3['x']
		ycoor = item3['y']
		list.append([int(xcoor), int(ycoor)])
        
    # List needs to contain the previous 10 conditions, no more
    # Checks to see if direction to the up, down, left, right is in the list
    for c1 in list:
	    if [snakehead_x, snakehead_y - 1] in list:
		    list2.append(['down'])
		    priority.append(['u', 10000])
		    break
			
    for c2 in list:
	    if [snakehead_x - 1, snakehead_y] in list:
		    list2.append(['right'])
		    priority.append(['l', 10000])
		    break

    for c3 in list:
	    if [snakehead_x + 1, snakehead_y] in list:
		    list2.append(['left'])
		    priority.append(['r', 10000])
		    break
			
    for c4 in list:
	    if [snakehead_x, snakehead_y + 1] in list:
		    list2.append(['up'])
		    priority.append(['d', 10000])
		    break
		
   
    width = data.get('width')
    height = data.get('height')

    # This will be the final check, we need to set priorities to 0 at the last step
    for j in range(0, width):
		if [j, 0] in list:
		    #Direction is not down
		    priority.append(['u', 900]) 
		    #priority.append(['l', 9000])
		    #priority.append(['r', 9000])
		    #break
		    #if [j, height - 2] in list:
		        #priority.append(['d', 400])
		    if snakehead_x == width - 1:
		    	    priority.append(['d', 500000])
				
		elif [j, height - 1] in list:
		    # Direction is not up
		    priority.append(['d', 900])
		    #priority.append(['l', 9000])
		    #priority.append(['r', 9000])
		    #if [j, 1] in list:
		        #priority.append(['u', 400])
		    if snakehead_x == width - 1:
		    	    priority.append(['u', 500000])
				
    for k in range(0, height):
		if [0, k] in list:
		    priority.append(['l', 900])
		    if snakehead_x == 0:
		    	    priority.append(['r', 500000])
		    	    
		    #priority.append(['d', 9000])
		    #priority.append(['u', 9000])
		    # Direction is not left
		    #if [j, 1] in list:
		        #priority.append(['d', 400])
				
		elif [width - 1, k] in list:
		    priority.append(['r', 900])
		    #priority.append(['u', 9000])
		    #priority.append(['d', 9000])
		    # Direction is not right
		    #if [j, 1] in list:
		        #priority.append(['u', 400])
		    if snakehead_x == width - 1:
		    	    priority.append(['l', 500000])
	
    if food_timer <= 40:
    	    if food_x + 1 == snakehead_x and food_y == snakehead_y:
		    priority.append(['r', 500])
		    priority.append(['d', 500])
		    priority.append(['u', 500])
			
	    elif food_x - 1 == snakehead_x and food_y == snakehead_y:
		    priority.append(['l', 500])
		    priority.append(['d', 500])
		    priority.append(['u', 500])
			
	    elif food_y + 1 == snakehead_y and food_x == snakehead_x:
		    priority.append(['r', 500])
		    priority.append(['l', 500])
		    priority.append(['d', 500])
			
	    elif food_y - 1 == snakehead_y and food_x == snakehead_x:
		    priority.append(['r', 500])
		    priority.append(['l', 500])
		    priority.append(['u', 500])
		
	    else:
		    priority.append(['r', 7])
		    priority.append(['l', 7])
		    priority.append(['u', 7])
		    priority.append(['d', 7])
        
			
    if (snakehead_x >= food_x and snakehead_y >= food_y):
        # direction = 'left';
	#priority.append(['u', 30])
	#priority.append(['d', 30])
	priority.append(['d', 350])
        priority.append(['u', 350])
        priority.append(['r', 350])
        
    elif (snakehead_x <= food_x and snakehead_y >= food_y):
        # direction = 'right'
        #priority.append(['u', 30])
        #priority.append(['d', 30])
        priority.append(['d', 350])
        priority.append(['l', 350])
        priority.append(['u', 350])
		
    elif (snakehead_x >= food_x and snakehead_y <= food_y):
        # direction = 'up'
        #priority.append(['l', 30])
        priority.append(['r', 350])
	priority.append(['l', 350])
	priority.append(['u', 350])
		
    else:
        # direction = 'down'
        priority.append(['l', 350])
        priority.append(['r', 350])
        priority.append(['d', 350])
		#priority.append(['l', 30])
		#priority.append(['r', 30])
	

 
    if food_x + 1 == snakehead_x and food_y == snakehead_y:
    	    priority.append(['r', 200])
	    priority.append(['d', 200])
	    priority.append(['u', 200])
		
    elif food_x - 1 == snakehead_x and food_y == snakehead_y:
	    priority.append(['l', 200])
	    priority.append(['d', 200])
	    priority.append(['u', 200])
		
    elif food_y + 1 == snakehead_y and food_x == snakehead_x:
	    priority.append(['r', 200])
	    priority.append(['l', 200])
	    priority.append(['d', 200])
		
    elif food_y - 1 == snakehead_y and food_x == snakehead_x:
	    priority.append(['r', 200])
	    priority.append(['l', 200])
	    priority.append(['u', 200])
        
    else:
	    priority.append(['r', 7])
	    priority.append(['l', 7])
	    priority.append(['u', 7])
	    priority.append(['d', 7])
	
	# If snake head touching bottom and tail is touching the top
	# direction = left or right
	
	# If snake head touching top and tail is touching the bottom
	# direction = left or right
	
	# If snake head touching left and tail touching right
	# direction = up or down
	
	# If snake head touching rigth and tail touching left
	# direction = up or down
	
	# If tail is touching wall and head touching other wall, direction is not out
	
	# Check to see if any snakehead_x coordinates in list, go opposite direction of x if just one x value in there
        # Dont turn right if head x + 1, y + 1 and x, y + 1 in list
	
	# If food timer < 30, food priority = high
	
	# If direction is going to run ya into a wall
	
    if snakehead_x == 0 and snakehead_y == 0 and [1, 0] in list:
	    priority.append(['r', 290000])
	    priority.append(['l', 290000])
	    priority.append(['u', 290000])
	    # Last one is debatable

    if snakehead_x == 0 and snakehead_y == 0 and [0, 1] in list:
	    priority.append(['u', 260000])
	    priority.append(['l', 260000])
	    priority.append(['d', 260000])
	    # Last one is debatable
	   
    if snakehead_x == width - 1 and snakehead_y == 0 and [width - 2, 0] in list:
	    priority.append(['r', 270000])
	    priority.append(['l', 270000])
	    priority.append(['u', 270000])
	    # Last one is debatable
	 
    if snakehead_x == width - 1 and snakehead_y == 0 and [width - 1, 1] in list:
	    priority.append(['r', 300000])
	    priority.append(['l', 300000])
	    priority.append(['d', 300000])
	    # Last one is debatable
	    
    if snakehead_x == width - 1 and snakehead_y == height - 1 and [width - 1, height - 2] in list:
	    priority.append(['r', 210000])
	    priority.append(['l', 210000])
	    priority.append(['d', 210000])
	    # Last one is debatable
	
    '''
    if snakehead_x == width - 1 and snakehead_y == height - 2 and [width - 2, height - 2] in list:
	    priority.append(['r', 130000])
	    priority.append(['l', 130000])
	    priority.append(['d', 130000])
	    # Last one is debatable '''
    
    ''' 
    if snakehead_x == width - 1 and snakehead_y == height - 1 and [width - 2, height - 1] in list:
	    priority.append(['r', 130000])
	    priority.append(['l', 130000])
	    priority.append(['d', 130000])
	    # Last one is debatable '''
  
    
    if snakehead_x == width - 1 and snakehead_y == height - 1 and [width - 2, height - 1] in list:
	    priority.append(['r', 130000])
	    priority.append(['l', 130000])
	    priority.append(['d', 130000])
	    # Last one is debatable '''
	 
    if snakehead_x == 0 and snakehead_y == height - 1 and [0, height - 2] in list:
	    priority.append(['d', 120000])
	    priority.append(['l', 120000])
	    priority.append(['u', 120000])
	    # Last one is debatable
	    
    if snakehead_x == 0 and snakehead_y == height - 1 and [1, height - 1] in list:
	    priority.append(['r', 150000])
	    priority.append(['l', 150000])
	    priority.append(['d', 150000])
	    # Last one is debatable

    if snakehead_x == 0 and snakehead_y == height - 1 and [1, height - 1] in list:
	    priority.append(['r', 150000])
	    priority.append(['l', 150000])
	    priority.append(['u', 150000])
	    # Last one is debatable
    
    u = 1
    d = 2
    l = 3
    r = 4
    final_choice = []
    mini = 1000000
    dir = []
	
    for i in range(0, int(len(priority))):
	    if priority[i][0] == 'u':
		    u += int(priority[i][1])
		
	    elif priority[i][0] == 'd':
		    d += int(priority[i][1])
			
	    elif priority[i][0] == 'r':
		    r += int(priority[i][1])
			
	    else:
		    l += int(priority[i][1])
			
    final_choice.append(['u', u])
    final_choice.append(['d', d])
    final_choice.append(['r', r])
    final_choice.append(['l', l])
	
    for fc in range(0, len(final_choice)):
	    if final_choice[fc][1] <= mini:
		    mini = int(final_choice[fc][1])
		    dir = final_choice[fc][0]
			
    if dir == 'u':
	    direction = directions[0]
    elif dir == 'd':
	    direction = directions[1]
    elif dir == 'l':
	    direction = directions[2]
    elif dir == 'r':
	    direction = directions[3]
    else:
	    direction = random.choice(directions)
    
	# 
	# Check for lowest value in list, improve
    
    print list2
    print "u:", u
    print "d:", d
    print "l:", l
    print "r:", r
    print priority
    print direction
    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }
	
def direction_choice(priority):
    up = 1
    down = 1
    left = 1
    right = 1
	
    for i in range(0, int(len(priority)) - 1):
	    if priority[i][0] == 'u':
		    up += int(priority[i][1])
		
	    elif priority[i][0] == 'd':
		    down += int(priority[i][1])
			
	    elif priority[i][0] == 'right':
		    right += int(priority[i][1])
			
	    else:
		    left += int(priority[i][1])
	
    

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)