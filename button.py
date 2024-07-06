import pygame.font

class Button():
	def __init__(self, settings, screen, msg): 
		self.screen = screen
		
		self.screen_rect = screen.get_rect()
		
		self.width, self.height = 100, 30
		self.button_color = (0, 0, 0)
		self.text_color = (255,255,255)
		self.font = pygame.font.SysFont(None, 25)
		
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.right = self.screen_rect.right - 15
		self.rect.centery = self.screen_rect.top + 25
		
		self.prep_msg(msg)
		
	def prep_msg(self, msg):
		self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
