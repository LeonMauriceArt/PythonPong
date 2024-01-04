import pygame

import config

class Wall:
	def __init__(self):
		self.width = config.POWERUP_WALL_WIDTH 
		self.color = config.WHITE
		self.isActive = False
		self.time_since_active = 0

	#paddle draw function
	def draw(self, win):
		if self.isActive:
			pygame.draw.rect(win, self.color, (config.WIN_WIDTH//2 - config.POWERUP_WALL_WIDTH//2, 0, self.width, config.WIN_HEIGHT))

	def activate(self, color):
		self.time_since_active = pygame.time.get_ticks()
		self.color = color
		self.isActive = True

	def update(self, ball):
		current_time = pygame.time.get_ticks()
		if self.isActive:
			if current_time - self.time_since_active >= config.POWERUP_WALL_DURATION * 1000:
				self.isActive = False
				ball.has_bounced_wall = False