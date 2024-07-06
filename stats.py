import pygame.font

class Stats():
	def __init__(self, settings, screen):
		self.fps_flag = 0
		self.time = 0
		self.moves = 0
		self.level = 1
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.settings = settings
		self.game_win = False
		self.paused = False
		self.auto = False
		self.new_game = False
		self.recursion = False
		self.recursion_flag = True
		self.recursion_path = []
	
		
		
		self.text_color = (0, 0, 0)
		self.text_color1 = (255, 0, 0)
		self.font = pygame.font.SysFont(None, 50)
		self.win_font = pygame.font.SysFont(None, 19)
		self.auto_font = pygame.font.SysFont(None, 20)
		self.error_font = pygame.font.SysFont(None, 27)
		self.dir_font = pygame.font.SysFont(None, 30)
		
		
		self.prep_score()
		self.prep_move()
		self.prep_level()
		
	
		
	def prep_score(self):
		self.score_string = "Time: " + "" + str(self.time)
		self.score_image = self.font.render(self.score_string, True, self.text_color, self.settings.screen_bg)
	
	
		self.score_rect = self.score_image.get_rect()
		self.score_rect.left = self.screen_rect.left + 20
		
	def prep_move(self):
		self.move_string = "Move: " + "" + str(self.moves) 
		self.move_image = self.font.render(self.move_string, True, self.text_color, self.settings.screen_bg)
		self.move_rect = self.move_image.get_rect()
		self.move_rect.left = self.score_rect.right + 50
		
	def prep_win(self):
		self.win_string = "01011001 01101111 01110101 - 01010111 01001001 01001110 00100001"
		self.win_string2 = "01010000 01110010 01100101 01110011 01110011 - 01001110 01100101 01110111 - 01000111 01100001 01101101 01100101 00100001"
		self.win_image = self.win_font.render(self.win_string, True, self.text_color, self.settings.screen_bg)
		self.win_image2 = self.win_font.render(self.win_string2, True, self.text_color, self.settings.screen_bg)
		self.win_rect = self.win_image.get_rect()
		self.win_rect2 = self.win_image2.get_rect()
		self.win_rect.top = 600
		self.win_rect2.top = 625
	
	def show_score(self):
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.move_image, self.move_rect)
		
	def show_win(self):
		self.screen.blit(self.win_image, self.win_rect)
		self.screen.blit(self.win_image2, self.win_rect2)
		
	def prep_paused(self):
		self.paused_string = "Game is Paused!"
		self.paused_image = self.font.render(self.paused_string, True, self.text_color, self.settings.screen_bg)
		self.paused_rect = self.paused_image.get_rect()
		self.paused_rect.top = 200
		self.paused_rect.left = 200
	
	def show_paused(self):
		self.screen.blit(self.paused_image, self.paused_rect)
		
	def prep_auto(self):
		self.auto_string = "Backtracking..."
		self.auto_image = self.auto_font.render(self.auto_string, True, self.text_color1, self.settings.screen_bg)
		self.auto_rect = self.auto_image.get_rect()
		self.auto_rect.top = 150
		self.auto_rect.right = self.screen_rect.right - 20
	def show_auto(self):
		self.screen.blit(self.auto_image, self.auto_rect)
		
	def prep_recursion(self):
		self.recursion_string = "Recursioning..."
		self.recursion_image = self.auto_font.render(self.recursion_string, True, self.text_color1 , self.settings.screen_bg)
		self.recursion_rect = self.recursion_image.get_rect()
		self.recursion_rect.top = 200
		self.recursion_rect.right = self.screen_rect.right-20
	def show_recursion(self):
		self.screen.blit(self.recursion_image, self.recursion_rect)

	def prep_level(self):
		self.level_string = "Level: " + "" + str(self.level)
		self.level_image = self.font.render(self.level_string, True, self.text_color, self.settings.screen_bg)
		self.level_rect = self.level_image.get_rect()
		self.level_rect.left = self.move_rect.right + 50
	
		
	def show_level(self):
		self.screen.blit(self.level_image, self.level_rect)

	def prep_error(self):
		self.error_string = "ERROR WITH RECURSION..TRY AGAIN...TOO LAZY TO FIND OUT WHATS WRONG"
		self.error_image = self.error_font.render(self.error_string, True, self.text_color, self.settings.screen_bg)
		self.error_rect = self.error_image.get_rect()
		self.error_rect.top = 200
		self.error_rect.left = 25
	
	def show_error(self):
		self.screen.blit(self.error_image, self.error_rect)
	
	def prep_dir(self):
		self.dir_string = "USE ARROW KEYS TO MOVE"
		self.dir_image = self.dir_font.render(self.dir_string, True, self.text_color, self.settings.screen_bg)
		self.dir_rect = self.dir_image.get_rect()
		self.dir_rect.left = 400
	
	def show_dir(self):
		self.screen.blit(self.dir_image, self.dir_rect)
	
