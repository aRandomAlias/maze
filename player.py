from settings import Settings
import pygame

class Player():
	
	def __init__(self, settings, screen, stats):
		
		# row location
	
		self.settings = settings
		self.stats = stats
		self.right = False
		self.left = False
		self.up = False
		self.down = False
		self.rect = pygame.Rect(self.settings.player_start, self.settings.player_start, self.settings.player_size, self.settings.player_size)
		self.screen = screen
		self.move = self.settings.player_size + (self.settings.player_size/2)
		self.wall_right = True
		self.wall_left = True
		self.wall_up = True
		self.wall_down = True
		#Use to navigate dummy_array
		self.wall_flag = 0
		self.current_position = 0
		
		self.end_block = pygame.Rect(self.move * (self.settings.maze_col-1) + self.settings.player_start, 
									self.move * (self.settings.maze_row-1) +  self.settings.player_start,
									self.settings.player_size, self.settings.player_size) 
		
		
		self.player_trail = []
		
	def update_player(self):

		
		if self.up and self.wall_up:
			
			self.rect.top -= self.move
			self.wall_flag = self.wall_flag - self.settings.maze_col
			self.stats.moves += 1
			self.current_position -= self.settings.maze_row
			#print("Players current position: " + str(self.current_position))
		
		elif self.down and self.wall_down:
		
			self.rect.bottom += self.move
			self.wall_flag = self.wall_flag + self.settings.maze_col
			self.stats.moves += 1
			self.current_position += self.settings.maze_row
			#print("Players current position: " + str(self.current_position))

		elif self.left and self.wall_left:
			
			self.rect.left -= self.move
			self.wall_flag = self.wall_flag - 1
			self.stats.moves += 1
			self.current_position -= 1
			#print("Players current position: " + str(self.current_position))

		elif self.right and self.wall_right:
			
			self.rect.right += self.move
			self.wall_flag = self.wall_flag + 1
			self.stats.moves += 1
			self.current_position += 1
			#print("Players current position: " + str(self.current_position))
		
		
		self.wall_right = True
		self.wall_left = True
		self.wall_up = True
		self.wall_down = True
		self.player_trail.append([self.rect.centerx, self.rect.centery])
		
		
	def draw_player(self):
		pygame.draw.rect(self.screen, (255,0,0) ,self.rect)
		pygame.draw.rect(self.screen, (252, 123, 34), self.end_block)
		
	def collide_test(self):
		collide = pygame.Rect.colliderect(self.rect, self.end_block)
		return collide
