import pygame 

import config
import math

from config import (
	BALL_RADIUS,
	BALL_SPEED,
)

import random

class Ball:

	def __init__(self, x, y, radius, color):
		self.xpos = self.original_x = x
		self.ypos = self.original_y = y
		self.radius = radius
		self.x_vel = BALL_SPEED
		self.y_vel = 0
		self.has_bounced_wall = False

	def move(self):
		self.xpos += self.x_vel
		self.ypos += self.y_vel

	def	reset(self):
		if config.NUM_OF_PLAYERS == 2 :
			up_or_side = 1
		else :
			up_or_side = random.choice([0, 1])
		if up_or_side == 0 :
			self.direction_y = random.choice([BALL_SPEED * -1, BALL_SPEED])
			self.direction_x = 0
		elif up_or_side == 1 :
			self.direction_x = random.choice([BALL_SPEED * -1, BALL_SPEED])
			self.direction_y = 0
		self.x_vel = 0
		self.y_vel = 0
		self.xpos = self.original_x
		self.ypos = self.original_y
		await asyncio.sleep(2)
		await self.start_after_reset()

	async def start_after_reset(self):
		self.x_vel = self.direction_x
		self.y_vel = self.direction_y
		self.direction_x = 0
		self.direction_y = 0

	def reverse_effect(self):
		if abs(self.x_vel) < abs(self.y_vel):	
			self.x_vel *= -1
		if abs(self.y_vel) < abs(self.x_vel):	
			self.y_vel *= -1

	def handle_ball_collision(self, players, wall):
		if wall.isActive:
			handle_wall_collision(wall)
		if config.NUM_OF_PLAYERS == 2:
			if self.ypos + self.radius >= config.WIN_HEIGHT and self.y_vel > 0 or self.ypos - self.radius <= 0 and self.y_vel < 0:
				self.y_vel *= -1
		elif config.NUM_OF_PLAYERS == 3:
			if self.ypos - self.radius <= 0:
				self.y_vel *= -1
		for player in players:
			if player.orientation == 'v':
				handle_vertical_collision(player)
			elif player.orientation == 'h':
				handle_horizontal_collision(player)

	def handle_wall_collision(self, wall):
		if self.xpos >= config.WIN_WIDTH // 2 - wall.width // 2 and self.xpos <= config.WIN_WIDTH // 2 + wall.width // 2 :
			if not self.has_bounced_wall :
				self.x_vel *= -1
				self.has_bounced_wall = True

	def handle_vertical_collision(self, player):
		if self.ypos >= player.ypos - player.height // 2 and self.ypos <= player.ypos + player.height // 2:
			if self.xpos + self.radius >= player.xpos - player.width // 2 and self.xpos - self.radius <= player.xpos + player.width // 2:
				if self.xpos > config.WIN_WIDTH // 2 and self.x_vel > 0 or self.xpos < config.WIN_WIDTH // 2 and self.x_vel < 0:
					update_ball_velocity(ball, player, 'v')

	def handle_horizontal_collision(self, player):
		if self.xpos >= player.xpos - player.width // 2 and self.xpos <= player.xpos + player.width // 2:
			if self.ypos + self.radius >= player.ypos - player.height // 2 and self.ypos - self.radius <= player.ypos + player.height // 2:
				if self.ypos > config.WIN_HEIGHT // 2 and self.y_vel > 0 or self.ypos < config.WIN_HEIGHT // 2 and self.y_vel < 0:
					update_ball_velocity(self, player, 'h')

	def update_ball_velocity(self, player, axis):
		self.color = player.color

		if axis == 'h':
			self.y_vel *= -1
			difference_in_x = player.xpos - self.xpos
			reduction_factor = (float(player.width) / 2) / BALL_SPEED
			self.x_vel = -difference_in_x / reduction_factor
		elif axis == 'v':
			self.x_vel *= -1
			difference_in_y = player.ypos - self.ypos
			reduction_factor = (float(player.height) / 2) / BALL_SPEED
			self.y_vel = -difference_in_y / reduction_factor
		#Merci julien pour le tip qui fixe la vitesse
		vel = math.sqrt(self.x_vel*self.x_vel + self.y_vel*self.y_vel);
		self.x_vel *= BALL_SPEED/vel
		self.y_vel *= BALL_SPEED/vel

	def to_dict(self):
		return {
			'xpos': self.xpos,
			'ypos': self.ypos,
			'x_speed': self.x_vel,
			'y_speed': self.y_vel,
			'radius': self.radius,
		}
