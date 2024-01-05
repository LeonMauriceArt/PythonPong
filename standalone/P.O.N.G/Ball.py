import pygame 

import config
import math

from config import (
	BALL_RADIUS,
	BALL_SPEED,
	WHITE
)

import random

class Ball:
	RESET_COOLDOWN = 1500

	def __init__(self, x, y, radius, color):
		self.x = self.original_x = x
		self.y = self.original_y = y
		self.radius = radius
		self.x_vel = BALL_SPEED
		self.y_vel = 0
		self.color = color
		self.has_bounced_wall = False

	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y),self.radius)

	def move(self):
		self.x += self.x_vel
		self.y += self.y_vel

	def	reset(self):
		self.wait_start = pygame.time.get_ticks()
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
		self.color = WHITE
		self.x_vel = 0
		self.y_vel = 0
		self.x = self.original_x
		self.y = self.original_y

	def reverse_effect(self):
		if abs(self.x_vel) < abs(self.y_vel):	
			self.x_vel *= -1
		if abs(self.y_vel) < abs(self.x_vel):	
			self.y_vel *= -1

	def update(self):
		if self.x_vel == 0 and self.y_vel == 0:
			current_time = pygame.time.get_ticks()
			if current_time - self.wait_start >= self.RESET_COOLDOWN:
				self.x_vel = self.direction_x
				self.y_vel = self.direction_y
				self.direction_x = 0
				self.direction_y = 0

def handle_ball_collision(ball, players, wall):
	if wall.isActive:
		handle_wall_collision(ball, wall)
	if config.NUM_OF_PLAYERS == 2:
		if ball.y + ball.radius >= config.WIN_HEIGHT and ball.y_vel > 0 or ball.y - ball.radius <= 0 and ball.y_vel < 0:
			ball.y_vel *= -1
	elif config.NUM_OF_PLAYERS == 3:
		if ball.y - ball.radius <= 0:
			ball.y_vel *= -1
	for player in players:
		if player.orientation == 'v':
			handle_vertical_collision(ball, player)
		elif player.orientation == 'h':
			handle_horizontal_collision(ball, player)

def handle_wall_collision(ball, wall):
	if ball.x >= config.WIN_WIDTH // 2 - wall.width // 2 and ball.x <= config.WIN_WIDTH // 2 + wall.width // 2 :
		if not ball.has_bounced_wall :
			ball.x_vel *= -1
			ball.has_bounced_wall = True
		

def handle_vertical_collision(ball, player):
    if ball.y >= player.y - player.height // 2 and ball.y <= player.y + player.height // 2:
        if ball.x + ball.radius >= player.x - player.width // 2 and ball.x - ball.radius <= player.x + player.width // 2:
            if ball.x > config.WIN_WIDTH // 2 and ball.x_vel > 0 or ball.x < config.WIN_WIDTH // 2 and ball.x_vel < 0:
                update_ball_velocity(ball, player, 'v')


def handle_horizontal_collision(ball, player):
    if ball.x >= player.x - player.width // 2 and ball.x <= player.x + player.width // 2:
        if ball.y + ball.radius >= player.y - player.height // 2 and ball.y - ball.radius <= player.y + player.height // 2:
            if ball.y > config.WIN_HEIGHT // 2 and ball.y_vel > 0 or ball.y < config.WIN_HEIGHT // 2 and ball.y_vel < 0:
                update_ball_velocity(ball, player, 'h')

def update_ball_velocity(ball, player, axis):
	ball.color = player.color

	if axis == 'h':
		ball.y_vel *= -1
		difference_in_x = player.x - ball.x
		reduction_factor = (float(player.width) / 2) / BALL_SPEED
		ball.x_vel = -difference_in_x / reduction_factor
	elif axis == 'v':
		ball.x_vel *= -1
		difference_in_y = player.y - ball.y
		reduction_factor = (float(player.height) / 2) / BALL_SPEED
		ball.y_vel = -difference_in_y / reduction_factor

	#Merci julien pour le tip qui fixe la vitesse
	vel = math.sqrt(ball.x_vel*ball.x_vel + ball.y_vel*ball.y_vel);
	ball.x_vel *= BALL_SPEED/vel
	ball.y_vel *= BALL_SPEED/vel
