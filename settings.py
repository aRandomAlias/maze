class Settings():
		
	def __init__(self):
		
		self.screen_width = 800
		self.screen_height = 700
		self.maze_row = 30
		self.maze_col = 30
		self.screen_bg = (200,200,200)
		self.wall_color = (0,0,0)
		# make sure its a even number or it get fucked up
		self.player_size = 14
		self.player_start = 50
		self.FPS = 10
		self.maze_tracker = [0] * (self.maze_col * self.maze_row)
		self.last_position = self.maze_row * self.maze_col -1
		
		self.easy = False
		self.medium = False
		self.hard = False
		self.extreme = False
