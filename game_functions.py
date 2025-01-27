
import sys
import pygame
from player import Player
from settings import Settings
import random


def move_the_player(settings, recursion_path, player, stats, dummy_array, current, previous):
	if current - previous == 1:
		player.right = True
	elif current - previous == -1:
		player.left = True
	elif current - previous == settings.maze_row:
		player.down = True
	elif current - previous == -settings.maze_row:
		player.up = True
	move_player(settings, player, dummy_array, stats)
	if current - previous == 1:
		player.right = False
	elif current - previous == -1:
		player.left = False
	elif current - previous == settings.maze_row:
		player.down = False
	elif current - previous == -settings.maze_row:
		player.up = False
	
def do_recursion(settings, stats, dummy_array, recursion_path, position, visited_path):
	if position not in visited_path:	
		visited_path.append(position)
	if position not in recursion_path:
		recursion_path.append(position)
	
	possible_path = backtrack_path(settings, dummy_array, position, visited_path)

	if len(possible_path) != 0 and position != settings.last_position:
		the_walk = get_random_walk(possible_path)

		if the_walk == 0:
			position = position - 1
		elif the_walk == 1:
			position = position - settings.maze_row
		elif the_walk == 2:
			position = position + 1
		elif the_walk == 3:
			position = position + settings.maze_row

		recursion_path = do_recursion(settings, stats, dummy_array, recursion_path, position, visited_path)

		return recursion_path
	

	if position == settings.last_position:
		return recursion_path	
	elif len(possible_path) == 0 and position != settings.last_position:
		#print("IM IN HERE")
		if position != 0:	
			recursion_path.pop()
		position = recursion_path[-1]
		recursion_path = do_recursion(settings, stats, dummy_array, recursion_path, position, visited_path)
		return recursion_path

	return recursion_path

def do_backtrack(settings, stats, dummy_array, player, solution_path, visited_path):
		
	
	solution_path.append(player.current_position)
	visited_path.append(player.current_position)
	solution_len = len(solution_path) -1

	path = backtrack_path(settings, dummy_array, player.current_position, visited_path)

	if len(path) != 0:
		the_walk = get_random_walk(path)

		if the_walk == 0:
			player.left = True	
		elif the_walk == 1:
			player.up = True
		elif the_walk == 2:
			player.right = True
		elif the_walk == 3:
			player.down = True

		move_player(settings, player, dummy_array, stats)

		if the_walk == 0:
			player.left = False	
		elif the_walk == 1:
			player.up = False
		elif the_walk == 2:
			player.right = False
		elif the_walk == 3:
			player.down = False
	
	
	if len(path) == 0:

		for i in range(solution_len):
			pop_pop = solution_path.pop()


			if (solution_path[-1] - pop_pop) == settings.maze_row:
				player.down = True
			elif (solution_path[-1] - pop_pop) == -settings.maze_row :	
				player.up = True
			elif (solution_path[-1] - pop_pop) == -1:
				player.left = True
			elif (solution_path[-1] - pop_pop) == 1:		
				player.right = True
		
			move_player(settings, player, dummy_array, stats)
	
			if (solution_path[-1] - pop_pop) == settings.maze_row:
				player.down = False
			elif (solution_path[-1] - pop_pop) == -settings.maze_row :	
				player.up = False
			elif (solution_path[-1] - pop_pop) == -1:
				player.left = False
			elif (solution_path[-1] - pop_pop) == 1:		
				player.right = False
		
			#prevents from getting stuck
			if (solution_path[-1] - pop_pop) != 0:
				break
			

	
	
def backtrack_path(settings, dummy_array, current_position, visited_path):
	
	possible_path = [0,1,2,3]
	if 0 in dummy_array[current_position]:
		possible_path.remove(0)
	if 1 in dummy_array[current_position]:
		possible_path.remove(1)
	if 2 in dummy_array[current_position]:
		possible_path.remove(2)
	if 3 in dummy_array[current_position]:
		possible_path.remove(3)
	
	if (current_position + 1) in visited_path:
		if 2 in possible_path:
			possible_path.remove(2)
	if (current_position - 1) in visited_path:
		if 0 in possible_path:
			possible_path.remove(0)
	if (current_position - settings.maze_row) in visited_path:
		if 1 in possible_path:
			possible_path.remove(1)
	if (current_position + settings.maze_row) in visited_path:
		if 3 in possible_path:
			possible_path.remove(3)


	return possible_path

def move_player(settings, player, dummy_array, stats):
	
	check_wall(settings, player, dummy_array)			
	player.update_player()
	#print("Players current position: " + str(player.current_position))
	if player.collide_test():
		stats.game_win = True
		stats.auto = False
		

def check_wall(settings, player, dummy_array):

	if 0 in dummy_array[player.wall_flag]:
		player.wall_left = False
	if 1 in dummy_array[player.wall_flag]:
		player.wall_up = False
	if 2 in dummy_array[player.wall_flag]:
		player.wall_right = False
	if 3 in dummy_array[player.wall_flag]:
		player.wall_down = False

def button_clicked(settings, screen, player, dummy_array, new_game_button, mouse_x, mouse_y, stats, maze_tracker):
	if new_game_button.rect.collidepoint(mouse_x, mouse_y):
		dummy_array, maze_tracker = reset_game(settings, screen, player, dummy_array, stats, maze_tracker)
	return dummy_array, maze_tracker
		
def reset_game(settings, screen, player, dummy_array, stats, maze_tracker):
	
	del dummy_array[:]
	del player.player_trail[:]
	
	
	if settings.easy == True:
		settings.maze_row = 30
		settings.maze_col = 30
		settings.player_size = 14
		

	elif settings.medium == True:
		settings.maze_row = 34
		settings.maze_col = 34
		settings.player_size = 12

	elif settings.hard == True:
		settings.maze_row = 52
		settings.maze_col = 52
		settings.player_size = 8
		
	elif settings.extreme == True:
		settings.maze_row = 70
		settings.maze_col = 70
		settings.player_size = 6
	
	settings.maze_tracker = [0] * (settings.maze_col * settings.maze_row)
	settings.last_position = settings.maze_row * settings.maze_col -1
	player.rect = pygame.Rect(settings.player_start, settings.player_start, settings.player_size, settings.player_size)
	player.move = settings.player_size + (settings.player_size/2)
	player.end_block = pygame.Rect(player.move * (settings.maze_col-1) + settings.player_start, 
									player.move * (settings.maze_row-1) +  settings.player_start,
									settings.player_size, settings.player_size)
	
	player.wall_flag = 0
	dummy_array = generate_corners(settings, dummy_array, settings.maze_tracker)
	
	

	stats.time = 0
	stats.fps_flag = 0
	stats.moves = 0
	stats.game_win = False
	stats.paused = False
	stats.auto = False
	stats.recursion = False
	stats.recursion_path = []
	stats.recursion_flag = True
	stats.new_game = True
	
	return dummy_array, settings.maze_tracker
	

def paused_clicked(paused_game_button, mouse_x, mouse_y, stats):
	if paused_game_button.rect.collidepoint(mouse_x, mouse_y):
		if stats.paused == True:
			stats.paused = False
		elif stats.paused == False:
			stats.paused = True
			
def auto_clicked(auto_game_button, mouse_x, mouse_y, stats):
	if auto_game_button.rect.collidepoint(mouse_x, mouse_y):
		if stats.paused != True:
			if stats.auto == True:
				stats.auto = False
			elif stats.auto == False:
				stats.auto = True
			if stats.recursion == True:
				stats.recursion = False
		
				
				
def recursion_clicked(recursion_button, mouse_x, mouse_y, stats):
	if recursion_button.rect.collidepoint(mouse_x, mouse_y):
		if stats.paused != True:
			if stats.recursion == False:
				stats.recursion = True
			elif stats.recursion == True:
				stats.recursion = False
				
			if stats.auto == True:
				stats.auto = False

def	difficulty_clicked(easy_button, medium_button, hard_button, extreme_button, mouse_x, mouse_y, stats, settings, screen, player, dummy_array, maze_tracker):
	if easy_button.rect.collidepoint(mouse_x, mouse_y):
		settings.easy = True
		settings.medium = False
		settings.hard = False
		settings.extreme = False
		reset_game(settings, screen, player, dummy_array, stats, maze_tracker)
	elif hard_button.rect.collidepoint(mouse_x, mouse_y):
		settings.easy = False
		settings.medium = False
		settings.hard = True
		settings.extreme = False
		reset_game(settings, screen, player, dummy_array, stats, maze_tracker)
	elif medium_button.rect.collidepoint(mouse_x, mouse_y):
		settings.easy = False
		settings.medium = True
		settings.hard = False
		settings.extreme = False
		reset_game(settings, screen, player, dummy_array, stats, maze_tracker)
	elif extreme_button.rect.collidepoint(mouse_x, mouse_y):
		settings.easy = False
		settings.medium = False
		settings.hard = False
		settings.extreme = True
		reset_game(settings, screen, player, dummy_array, stats, maze_tracker)
		
	

def event_check(settings, screen, player, dummy_array, new_game_button, stats, maze_tracker, 
				paused_game_button, auto_game_button, recursion_button,
				easy_button, medium_button, hard_button, extreme_button):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			dummy_array, maze_tracker = button_clicked(settings, screen, player, dummy_array, new_game_button, mouse_x, mouse_y, stats, maze_tracker)
			paused_clicked(paused_game_button, mouse_x, mouse_y, stats)
			auto_clicked(auto_game_button, mouse_x, mouse_y, stats)
			recursion_clicked(recursion_button, mouse_x, mouse_y, stats)
			difficulty_clicked(easy_button, medium_button, hard_button, extreme_button, mouse_x, mouse_y, stats, settings, screen, player, dummy_array, maze_tracker)

	
			
		elif event.type == pygame.KEYDOWN and stats.auto == False and stats.recursion == False:
			if event.key == pygame.K_RIGHT:	
				player.right = True
							
				
			elif event.key == pygame.K_DOWN:	
				player.down = True
				
			elif event.key == pygame.K_LEFT:	
				player.left = True

			elif event.key == pygame.K_UP:	
				player.up = True			

			
			
		elif event.type == pygame.KEYUP and stats.auto == False and stats.recursion == False:
			if event.key == pygame.K_RIGHT:
				player.right = False
			elif event.key == pygame.K_DOWN:
				player.down = False
			elif event.key == pygame.K_LEFT:
				player.left = False
			elif event.key == pygame.K_UP:
				player.up = False
		
	return dummy_array, maze_tracker
	
def draw_walls(settings, screen, dummy_array):
	space = (settings.player_size + (settings.player_size/2))
	start_row = settings.player_start - (settings.player_size/4)
	start_col = settings.player_start - (settings.player_size/4)
	row_flag = 0
	col_flag = 0
	 
	for lsls in dummy_array:
		for ls in lsls:
			if ls == 0:
				pygame.draw.line(screen, settings.wall_color, (start_col, start_row), (start_col, start_row + space))
			elif ls == 1:
				pygame.draw.line(screen, settings.wall_color, (start_col, start_row), (start_col + space, start_row))
			elif ls == 2:
				pygame.draw.line(screen, settings.wall_color, (start_col + space, start_row), (start_col+space, start_row + space))
			elif ls == 3:
				pygame.draw.line(screen, settings.wall_color, (start_col, start_row+space), (start_col + space, start_row + space))
		
			
		start_col += space
		col_flag += 1
		if col_flag == settings.maze_col:
			row_flag += 1
			start_row += space
			col_flag = 0
			start_col = (settings.player_start - (settings.player_size/4))
			
def draw_player_trail(player, screen):

	for i in player.player_trail:
		pygame.draw.circle(screen, 'red', (i[0], i[1]), 3)


def generate_corners(settings, dummy_array, maze_tracker):
	wall_tracker = []
	for row in range(settings.maze_row):
		for col in range(settings.maze_col):
			#TOP LEFT CORNER
			if row == 0 and col == 0:
				# set initial corner(top left)
				dummy_array.append([0,1])
				wall_tracker.append(1)
			#TOP WALL
			elif row == 0 and col != settings.maze_col-1:
				# set initial wall
				dummy_array.append([1])
				wall_tracker.append(5)								
			#TOP RIGHT CORNER
			elif row == 0 and col == settings.maze_col-1:
				dummy_array.append([1,2])
				wall_tracker.append(2)
			#LEFT WALL
			elif col == 0 and row !=0 and row != settings.maze_row-1:
				dummy_array.append([0])
				wall_tracker.append(6)
			#RIGHT WALL
			elif col == settings.maze_col-1 and row != 0 and row != settings.maze_row-1:
				dummy_array.append([2])
				wall_tracker.append(7)
			#BOTTOM LEFT CORNER
			elif row == settings.maze_row-1 and col == 0:
				dummy_array.append([0,3])
				wall_tracker.append(3)
			#BOTTOM WALL
			elif row == settings.maze_row-1 and col != settings.maze_col-1:
				dummy_array.append([3])
				wall_tracker.append(8)
			#BOTTOM RIGHT CORNER
			elif row == settings.maze_row-1 and col == settings.maze_col-1:
				dummy_array.append([2,3])	
				wall_tracker.append(4)
			# MIDDLE
			else:
				# number 5 is a placeholder
				dummy_array.append([])
				wall_tracker.append(0)
	
	dummy_array = generate_maze(settings, dummy_array, wall_tracker, maze_tracker)
	
	#print(dummy_array)					
	return dummy_array

def generate_maze(settings, dummy_array, wall_tracker, maze_tracker):

	c_pos = 0
	
	no_solution = True
	maze_size = settings.maze_row * settings.maze_col - 1
	prev_path = -1
	choosen_path = -1
	connect_it = -1
	connect_Flag = False

	while no_solution:
		"""
		print()
		print("Back at TOP: ")
		print("current pos: " + str(c_pos))
		"""
		maze_tracker[c_pos] = 1
		# look for possible paths in current position, returns an array of possible paths.
		possible_path = possible_paths(settings, c_pos, dummy_array, wall_tracker, maze_tracker)
		if len(possible_path) == 0 or c_pos == maze_size:
			#print("IN IF")
			connect_Flag = False
			
			choosen_path = -1

			dummy_array[c_pos] = create_walls(settings, choosen_path, prev_path, connect_it, connect_Flag)
			
			prev_path = -1
			# we have reached a dead end now we must find a c_pos that hasn't been visited
			c_pos = new_cpos(maze_tracker, settings)
			maze_tracker[c_pos] = 1
			if c_pos == maze_size:
				break
			#print("New c_pos: " + str(c_pos))
			# open wall so that it connects the paths
			dummy_array, connect_it = connect_path(settings, dummy_array, c_pos, maze_tracker, wall_tracker)
			connect_Flag = True

			continue
		# choose the random path
		choosen_path = get_random_walk(possible_path)

		connect_it == -1
		# create walls for c_pos and leave choosen_path open
		dummy_array[c_pos] = create_walls(settings, choosen_path, prev_path, connect_it, connect_Flag)
		connect_Flag = False
		
		
		prev_path = choosen_path
		
		# update c_pos based on the random path and update maze_tracker to let us know c_pos has been visited
		
		c_pos = update_cpos(settings, c_pos, choosen_path)
		
		
		
		
		
		if c_pos == maze_size:
			maze_tracker[c_pos] = 1
			# check if there are any remaining unvisited position
			remains = check_remaining(maze_tracker)
			if remains: 				
				continue
			
			no_solution = False
		
	
	
	# remaining boxed out sqaures

	dummy_array = remaining_blocked_in(settings, dummy_array, c_pos, maze_tracker, wall_tracker)
	
	# for last square boxed in 	
	if 2 in dummy_array[maze_size-1] and 3 in dummy_array[maze_size-settings.maze_row]:
		remove_it = get_random_walk([2,3])
		if remove_it == 2:
			dummy_array[maze_size-1].remove(2)
		else:
			dummy_array[maze_size-settings.maze_row].remove(3)
	return dummy_array
	
def remaining_blocked_in(settings, dummy_array, c_pos, maze_tracker, wall_tracker):
	
	maze_len = len(maze_tracker) - 1
	for i in range(maze_len):
		
		if len(dummy_array[i]) == 4:
			#print("IM IN REMAINING BLOCK: " + str(i))
			if wall_tracker[i] == 2:
				if 2 not in dummy_array[i-1]:
					dummy_array[i].remove(0)
				elif 1 not in dummy_array[i+settings.maze_row]:
					dummy_array[i].remove(3)
			elif wall_tracker[i] == 3:
				if 3 not in dummy_array[i-settings.maze_row]:
					dummy_array[i].remove(1)
				elif 0 not in dummy_array[i+1]:
					dummy_array[i].remove(2)
			elif wall_tracker[i] == 4:
				if 3 not in dummy_array[i-settings.maze_row]:
					dummy_array[i].remove(1)
				elif 2 not in dummy_array[i-1]:
					dummy_array[i].remove(0)
			elif wall_tracker[i] == 5:
				if 2 not in dummy_array[i-1]:
					dummy_array[i].remove(0)
				elif 0 not in dummy_array[i+1]:
					dummy_array[i].remove(2)
				elif 1 not in dummy_array[i+settings.maze_row]:
					dummy_array[i].remove(3)
			elif wall_tracker[i] == 6:
				if 3 not in dummy_array[i-settings.maze_row]:
					dummy_array[i].remove(1)
				elif 0 not in dummy_array[i+1]:
					dummy_array[i].remove(2)
				elif 1 not in dummy_array[i+settings.maze_row]:
					dummy_array[i].remove(3)
			elif wall_tracker[i] == 7:
				if 3 not in dummy_array[i-settings.maze_row]:
					dummy_array[i].remove(1)
				elif 2 not in dummy_array[i-1]:
					dummy_array[i].remove(0)
				elif 1 not in dummy_array[i+settings.maze_row]:
					dummy_array[i].remove(3)
			elif wall_tracker[i] == 8:
				if i != maze_len -1:
					if 2 not in dummy_array[i-1]:
						dummy_array[i].remove(0)
					elif 3 not in dummy_array[i-settings.maze_row]:
						dummy_array[i].remove(1)
					elif 0 not in dummy_array[i+1]:
						dummy_array[i].remove(2)
				else:
					if 2 in dummy_array[i-1]:
						dummy_array[i].remove(0)
						dummy_array[i-1].remove(2)
					elif 3 in dummy_array[i-settings.maze_row]:
						dummy_array[i].remove(1)
						dummy_array[i-settings.maze_row].remove(3)
					elif 0 in dummy_array[i+1]:
						dummy_array[i].remove(2)
						dummy_array[i+1].remove(0)
			else:
				#print("IM IN ELSE:" + str(i))
				if 2 not in dummy_array[i-1]:
					dummy_array[i].remove(0)
				elif 3 not in dummy_array[i-settings.maze_row]:
					dummy_array[i].remove(1)
				elif 1 not in dummy_array[i+settings.maze_row]:
					dummy_array[i].remove(3)
				elif 0 not in dummy_array[i+1]:
					dummy_array[i].remove(2)


	return dummy_array
	
def check_remaining(maze_tracker):
	maze_len = len(maze_tracker) -1

	for i in range(maze_len):
		if maze_tracker[i] == 0:
			return True
			
	
	return False
	
def connect_path(settings, dummy_array, c_pos, maze_tracker, wall_tracker):
	removal_path = []
	if wall_tracker[c_pos] != 0:
		if wall_tracker[c_pos] == 2:
			if maze_tracker[c_pos-1] == 1:
				removal_path.append(0)
			elif maze_tracker[c_pos+settings.maze_row] == 1:
				removal_path.append(3)
		elif wall_tracker[c_pos] == 3:
			if maze_tracker[c_pos-settings.maze_row] == 1:
				removal_path.append(1)
			elif maze_tracker[c_pos+1] == 1:
				removal_path.append(2)
		elif wall_tracker[c_pos] == 5:
			if maze_tracker[c_pos-1] == 1:
				removal_path.append(0)
			elif maze_tracker[c_pos+sttings.maze_row] == 1:
				removal_path.append(3)
			elif maze_tracker[c_pos+1] == 1:
				removal_path.append(2)
		elif wall_tracker[c_pos] == 6:
			if maze_tracker[c_pos-settings.maze_row] == 1:
				removal_path.append(1)
			elif maze_tracker[c_pos+sttings.maze_row] == 1:
				removal_path.append(3)
			elif maze_tracker[c_pos+1] == 1:
				removal_path.append(2)
		elif wall_tracker[c_pos] == 7:
			if maze_tracker[c_pos-settings.maze_row] == 1:
				removal_path.append(1)
			elif maze_tracker[c_pos+settings.maze_row] == 1:
				removal_path.append(3)
			elif maze_tracker[c_pos-1] == 1:
				removal_path.append(0)
		elif wall_tracker[c_pos] == 8:
			if maze_tracker[c_pos+1] == 1:
				removal_path.append(2)
			elif maze_tracker[c_pos-1] == 1:
				removal_path.append(0)
			elif maze_tracker[c_pos - settings.maze_row] == 1:
				removal_path.append(1)


	else:
		if maze_tracker[c_pos+1] == 1:
			removal_path.append(2)
		elif maze_tracker[c_pos-1] == 1:
			removal_path.append(0)
		elif maze_tracker[c_pos+settings.maze_row] == 1:
			removal_path.append(3)
		elif maze_tracker[c_pos-settings.maze_row] == 1:
			removal_path.append(1)
			
	

	remove_path = get_random_walk(removal_path)

	if remove_path == 0:
		dummy_array[c_pos-1].remove(2)
	elif remove_path == 1:
		dummy_array[c_pos-settings.maze_row].remove(3)
	elif remove_path == 2:
		dummy_array[c_pos+1].remove(0)
	elif remove_path == 3:
		dummy_array[c_pos+settings.maze_row].remove(1)
		
	dummy_array[c_pos] = [0,1,2,3]
	dummy_array[c_pos].remove(remove_path)
	
	possible_path = possible_paths(settings, c_pos, dummy_array, wall_tracker, maze_tracker)
	if len(possible_path) != 0:
		if 0 in possible_path:
			dummy_array[c_pos].remove(0)
		if 1 in possible_path:
			dummy_array[c_pos].remove(1)
		if 2 in possible_path:
			dummy_array[c_pos].remove(2)
		if 3 in possible_path:
			dummy_array[c_pos].remove(3)
	
	

	return dummy_array, remove_path
		

def new_cpos(maze_tracker, settings):
	maze_len = len(maze_tracker) -1
	
	#possible_paths
	# new c_pos horizontal or vertical
	vert_hort = get_random_walk([0,1])
	# if 0 horizontal if 1 vertical
	if vert_hort == 0:
		for i in range(maze_len):
			if maze_tracker[i] == 0:
				return i
					#print("new_cpos: " + str(i))
	elif vert_hort == 1:
		for i in range(settings.maze_row):
			for j in range(settings.maze_row):
				if maze_tracker[(i)+(j*settings.maze_row)] == 0:
					return (i+(j*settings.maze_row)) 

			
	
	return maze_len
	
#create walls for dead in 
def create_walls(settings, choosen_path, prev_path, connect_it, connect_Flag):
	walls = [0,1,2,3]
	
	if choosen_path != -1:
		walls.remove(choosen_path)
	
	if prev_path != -1:
		#print("REMOVING PREV: " + str(prev_path))
		if prev_path == 0:
			walls.remove(2)
		if prev_path == 1:
			walls.remove(3)
		if prev_path == 2:
			walls.remove(0)
		if prev_path == 3:
			walls.remove(1)
    # maz tracker
	if connect_it != choosen_path and connect_Flag:
		#print("REMOVING CONNECT: " + str(connect_it))
		if connect_it == 0 and 0 in walls:
			walls.remove(0)
		elif connect_it == 1 and 1 in walls:
			walls.remove(1)
		elif connect_it == 2 and 2 in walls:
			walls.remove(2)
		elif connect_it == 3 and 3 in walls:
			walls.remove(3)

	return walls
	
def possible_paths(settings, c_pos, dummy_array, wall_tracker, maze_tracker):
	# 0 - left, 1 - up, 2 - right, 3 - down
	paths = [0,1,2,3]
	# check to see if you are in corner with wall_tracker
	# using maze_tracker to check if its already been visited and take out of possible paths list
	# walltracker != 0 is to ceck if we are in a corner
	if wall_tracker[c_pos] != 0:
		if wall_tracker[c_pos] == 1:
			paths.remove(0)
			paths.remove(1)
			if maze_tracker[c_pos+1] == 1:
				paths.remove(2)
			if maze_tracker[c_pos+settings.maze_row] == 1:
				paths.remove(3)
		elif wall_tracker[c_pos] == 2:
			paths.remove(1)
			paths.remove(2)
			if maze_tracker[c_pos-1] == 1:
				paths.remove(0)
			if maze_tracker[c_pos+settings.maze_row] ==1:
				paths.remove(3)
		elif wall_tracker[c_pos] == 3:
			paths.remove(0)
			paths.remove(3)
			if maze_tracker[c_pos-settings.maze_row] == 1:
				paths.remove(1)
			if maze_tracker[c_pos+1] == 1:
				paths.remove(2)
		elif wall_tracker[c_pos] == 4:
			paths.remove(2)
			paths.remove(3)
			if maze_tracker[c_pos-settings.maze_row] == 1:
				paths.remove(1)
			if maze_tracker[c_pos-1] == 1:
				paths.remove(0)
		elif wall_tracker[c_pos] == 5:
			paths.remove(1)
			if maze_tracker[c_pos-1] == 1:
				paths.remove(0)
			if maze_tracker[c_pos+1] == 1:
				paths.remove(2)
			if maze_tracker[c_pos+settings.maze_row] == 1:
				paths.remove(3)
		elif wall_tracker[c_pos] == 6:
			paths.remove(0)
			if maze_tracker[c_pos-settings.maze_row] == 1:
				paths.remove(1)
			if maze_tracker[c_pos+1] == 1:
				paths.remove(2)
			if maze_tracker[c_pos+settings.maze_row] == 1:
				paths.remove(3)
		elif wall_tracker[c_pos] == 7:
			paths.remove(2)
			if maze_tracker[c_pos-settings.maze_row] == 1:
				paths.remove(1)
			if maze_tracker[c_pos-1] == 1:
				paths.remove(0)
			if maze_tracker[c_pos+settings.maze_row] ==1:
				paths.remove(3)
		elif wall_tracker[c_pos] == 8:
			paths.remove(3)
			if maze_tracker[c_pos-1] == 1:
				paths.remove(0)
			if maze_tracker[c_pos-settings.maze_row] == 1:
				paths.remove(1)
			if maze_tracker[c_pos+1] == 1:
				paths.remove(2)
	else:
		if maze_tracker[c_pos+1] == 1:
			paths.remove(2)
		if maze_tracker[c_pos-1] == 1:
			paths.remove(0)
		if maze_tracker[c_pos+settings.maze_row] == 1:
			paths.remove(3)
		if maze_tracker[c_pos-settings.maze_row] == 1:
			paths.remove(1)

	return paths
	

def get_random_walk(path_list):
	the_walk = random.choice(path_list)
	return the_walk


def update_cpos(settings, c_pos, random_walk):
	if random_walk == 0:
		c_pos -= 1
	elif random_walk == 1:
		c_pos -= settings.maze_col
	elif random_walk == 2:
		c_pos += 1
	elif random_walk == 3:
		c_pos += settings.maze_col
	
	return c_pos

