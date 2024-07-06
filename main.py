
import sys
import pygame
from player import Player
from settings import Settings
import game_functions as gf
from button import Button
from stats import Stats
import asyncio
import time


async def main():
	def start_game():
		
		sys.setrecursionlimit(10**6)
 

		settings = Settings()
		game_active = True
		
		dummy_array = []
		wall_tracker = []
		#m, n = settings.maze_col, settings.maze_row
		#maze_tracker = [[0] * n for i in range(m)]
		settings.maze_tracker = [0] * (settings.maze_col * settings.maze_row)

		dummy_array= gf.generate_corners(settings, dummy_array, settings.maze_tracker)
		pygame.init()
		
		screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
		stats = Stats(settings, screen)
		
		player = Player(settings, screen, stats)
		pygame.display.set_caption("Maze")
		new_game_button = Button(settings, screen, "New Game")
		paused_game_button = Button(settings, screen, "Pause")
		paused_game_button.rect.centery = paused_game_button.screen_rect.top + 75
		paused_game_button.prep_msg("Pause")
		
		auto_game_button = Button(settings, screen, "Backtrack")
		auto_game_button.rect.top = paused_game_button.rect.bottom + 25
		auto_game_button.prep_msg("Backtrack")
		
		recursion_button = Button(settings, screen, "Recursion")
		recursion_button.rect.top = auto_game_button.rect.bottom + 25
		recursion_button.prep_msg("Recursion")
		
		extreme_button = Button(settings, screen, "????????")
		extreme_button.rect.bottom = stats.screen_rect.bottom - 25
		extreme_button.prep_msg("????????")
		
		hard_button = Button(settings, screen, "HARD")
		hard_button.rect.bottom = extreme_button.rect.top - 25
		hard_button.prep_msg("HARD")
		
		medium_button = Button(settings, screen, "MEDIUM")
		medium_button.rect.bottom = hard_button.rect.top -25
		medium_button.prep_msg("MEDIUM")
		
		easy_button = Button(settings, screen, "EASY")
		easy_button.rect.bottom = medium_button.rect.top - 25
		easy_button.prep_msg("EASY")
		
		clock = pygame.time.Clock()
		
		solution_path = []
		visited_path = []
	
		recursion_visited = []
		
		#print(maze_tracker)
		#print(wall_tracker)
	

		while game_active:
			
			dummy_array, settings.maze_tracker = gf.event_check(settings, screen, player, dummy_array, new_game_button, stats, 
													   settings.maze_tracker, paused_game_button, auto_game_button, recursion_button,
														easy_button, medium_button, hard_button, extreme_button)
			
			screen.fill(settings.screen_bg)
			if stats.new_game == True:
				solution_path = []
				visited_path = []
				stats.new_game = False
				player.current_position = 0
			if stats.auto == False:
				solution_path = []
				visited_path = []
				
			if stats.recursion == False:
				recursion_path = []
				recursion_visited = []
				
			
			gf.draw_walls(settings, screen, dummy_array)
			player.draw_player()	
			if not stats.game_win and not stats.paused and not stats.auto and not stats.recursion:	
				gf.move_player(settings, player, dummy_array, stats)	
				
			# backtracking(not recursion)
			if stats.auto and not stats.game_win and not stats.paused and not stats.recursion:
				# we need dummy_array, player.current_position
			
				gf.do_backtrack(settings, stats, dummy_array, player, solution_path, visited_path)
				
			# recursion and backtracking
			if stats.recursion and not stats.game_win and not stats.paused and not stats.game_win:
				# because of recursion limit
				# or use import sys ... sys.setrecursionlimit()

				if stats.recursion_flag:
					# SOMETIMES IT RETURNS 0 as the last element of the array and fucks everything up. i think passing the 0 has something to do with it.
					stats.recursion_path = []
					recursion_visited = []
					
					try:
						if stats.recursion and not stats.game_win and not stats.paused and not stats.auto:
							stats.prep_recursion()
							stats.show_recursion()
							pygame.display.flip()
							
						stats.recursion_path = gf.do_recursion(settings, stats, dummy_array, stats.recursion_path, player.current_position, recursion_visited)
						stats.recursion_flag = False
						"""
						print()

						print()
						print()
						print("I GOT HERE")
						
						print("THE SOULTION: " + str(stats.recursion_path))
						"""
						
					except:
						stats.recursion = False
						stats.prep_error()
						stats.show_error()
						pygame.display.flip()
						time.sleep(2)	
				
				
				#print(stats.recursion_path)
				
				try:
					previous = stats.recursion_path.pop(0)	
					current = stats.recursion_path[0]
					gf.move_the_player(settings, recursion_path, player, stats, dummy_array, current, previous)
				except:
					stats.recursion = False
					stats.prep_error()
					stats.show_error()
					pygame.display.flip()
					time.sleep(2)			
				
				
				#print("PREVIOUS: " + str(previous))
				#print("CURRENT: " + str(current))
				
				
				
			stats.prep_dir()
			stats.show_dir()
			stats.show_score()
			stats.prep_score()	
			stats.prep_move()

			
			new_game_button.draw_button()
			paused_game_button.draw_button()
			auto_game_button.draw_button()
			recursion_button.draw_button()
			extreme_button.draw_button()
			hard_button.draw_button()
			medium_button.draw_button()
			easy_button.draw_button()
		
			
			
			if stats.paused == True and not stats.game_win:
				stats.prep_paused()
				stats.show_paused()
				
			if stats.auto == True and stats.paused != True and not stats.game_win:
				stats.prep_auto()
				stats.show_auto()
				
			if stats.recursion and not stats.game_win and not stats.paused and not stats.auto:
				stats.prep_recursion()
				stats.show_recursion()
			
			if stats.game_win:
				stats.prep_win()
				stats.show_win()
			
			#pygame.display.update can update the whole screen as well if there are no paraments
			#allows to update a portion of the screen, instead of the entire area of the screen
			pygame.display.flip()
			

			#if stats.paused == False:
			clock.tick(settings.FPS)
		
			if not stats.game_win and not stats.paused:
				stats.fps_flag += 1
				if stats.fps_flag == settings.FPS:
					stats.time += 1
					stats.prep_score()
					stats.fps_flag = 0
							

	start_game()
	await asyncio.sleep(0)

asyncio.run(main())
	
