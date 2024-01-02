import random
import math
import pygame
import config
import random

class Powerup:
	def __init__(self, x, y, radius, type):
		self.x = x
		self.y = y
		self.radius = radius
		self.type = type
		self.color = self.getColorType()

	def getColorType(self):
		if self.type == config.POWERUP_REVERSE:
			return (0, 255, 0)
		elif self.type == config.POWERUP_WALL:
			return (255, 0, 255)
		elif self.type == config.POWERUP_CURSE:
			return (0, 255, 255)

	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y),self.radius)

def spawn_power():
	types = [config.POWERUP_REVERSE, config.POWERUP_CURSE, config.POWERUP_WALL]
	newpower_type =  random.randint(0, 2)
	newpower_x_pos = random.randint(config.SPAWN_MIN_X, config.SPAWN_MAX_X)
	newpower_y_pos = random.randint(config.SPAWN_MIN_Y, config.SPAWN_MAX_Y)
	newpower = Powerup(newpower_x_pos, newpower_y_pos, config.POWERUP_RADIUS, types[newpower_type])
	return newpower


def handle_power_collision(ball, powerup, players):
	distance = math.sqrt((ball.x - powerup.x)**2 + (ball.y - powerup.y)**2)
	if distance <= (ball.radius + powerup.radius):
		for player in players :
			if ball.color == player.color and not player.powerups:
				player.add_powerup(powerup)
				return True
	return False

def power_can_spawn(powerups, last_empty_time):
	current_time = pygame.time.get_ticks()
	if not powerups and (current_time - last_empty_time) > config.POWERUP_SPAWN_INTERVAL * 1000:
		return True
	return False