import pygame

from config import (
	POWERUP_WALL_WIDTH,
	POWERUP_WALL_DURATION,
	WHITE
)

class Wall:
	def __init__(self):
		self.width = POWERUP_WALL_WIDTH 
		self.color = WHITE
		self.isActive = False
		self.time_since_active = 0

	#paddle draw function
	def draw(self, win):
		if self.isActive:
			pygame.draw.rect(win, self.color, (WIN_WIDTH//2 - WALL_WIDTH//2, 0, self.width, WIN_HEIGHT))

	def activate(self, color):
		self.time_since_active = pygame.time.get_ticks()
		self.color = color
		self.isActive = True

	def update(self):
		current_time = pygame.time.get_ticks()
		if self.isActive:
			if current_time - self.time_since_active >= POWERUP_WALL_DURATION * 1000:
				self.isActive = False