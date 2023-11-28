import pygame

import config
import Powerup
import Wall
import Ball

from Wall import Wall
from Ball import *
from Powerup import *
from config import *

#Player class
class Player:
	#Movement speed of the paddle
	VEL = 5

	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.powerups = []
		self.curse_time_start = 0

	#paddle draw function
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

	#Move function
	def move(self, up=True):
		if up:
			self.y -= self.VEL
		else:
			self.y += self.VEL

	def curse_opponent(self, opponent):
		if opponent.height != POWERUP_CURSE_SIZE:
			# Calculate the amount by which the rectangle should expand
			expansion_amount = POWERUP_CURSE_SIZE - opponent.height

			# Expand the rectangle both upwards and downwards
			opponent.y -= expansion_amount // 2
			opponent.height += expansion_amount

			# Ensure the rectangle doesn't go above the top
			if opponent.y < 0:
				opponent.y = 0

			# Ensure the rectangle doesn't go below the bottom
			if opponent.y + opponent.height > HEIGHT:
				opponent.y = HEIGHT - opponent.height

	def reset(self):
		self.y = HEIGHT//2 - PADDLE_HEIGHT//2

	def add_powerup(self, powerup):
		if not self.powerups:
			print("Player as acquired the", powerup.type, "power !")
			self.powerups.append(powerup)
	
	def use_powerup(self, player, wall, ball, opponent):
		if self.powerups:
			if (self.powerups[0].type == POWERUP_WALL and not wall.isActive):
				self.powerups[0].printuse(player)
				wall.activate(self.color)
				self.powerups.pop(0)
			elif self.powerups[0].type == POWERUP_REVERSE:
				self.powerups[0].printuse(player)
				ball.reverse_effect()
				self.powerups.pop(0)
			elif self.powerups[0].type == POWERUP_CURSE:
				self.powerups[0].printuse(player)
				opponent.curse_time_start = pygame.time.get_ticks()
				self.curse_opponent(opponent)
				self.powerups.pop(0)

	def update(self):
		current_time = pygame.time.get_ticks()
		if self.height == POWERUP_CURSE_SIZE:
			if current_time - self.curse_time_start >= POWERUP_CURSE_DURATION * 1000:
				retract_amount = POWERUP_CURSE_SIZE - PADDLE_HEIGHT
				self.y += retract_amount // 2
				self.height -= retract_amount
				self.CURSE_time_start = 0


#Handling key pressing for paddle movement
def handle_inputs(keys, left_player, right_player, ball, wall):
	#Left paddle input
	if keys[pygame.K_w] and left_player.y - left_player.VEL >= 0:
		left_player.move(up=True)
	if keys[pygame.K_s] and left_player.y + left_player.VEL + left_player.height <= HEIGHT:
		left_player.move(up=False)
	if keys[pygame.K_d]:
		left_player.use_powerup("Left Player", wall, ball, right_player)
	#Right paddle input
	if keys[pygame.K_UP] and right_player.y - right_player.VEL >= 0:
		right_player.move(up=True)
	if keys[pygame.K_DOWN] and right_player.y + right_player.VEL + right_player.height <= HEIGHT:
		right_player.move(up=False)
	if keys[pygame.K_LEFT]:
		right_player.use_powerup("Right Player", wall, ball, left_player)

