import pygame
import config
from config import (
	PLAYER_WIDTH,
	PLAYER_HEIGHT,
	PLAYER_1_COLOR,
	PLAYER_2_COLOR,
	PLAYER_3_COLOR,
	PLAYER_4_COLOR,
	POWERUP_CURSE_SIZE,
	POWERUP_CURSE_DURATION,
	WINNING_SCORE
)

#Player class
class Player:
	#Movement speed of the paddle
	VEL = 5
	orientation = None	#h for horizontal, v for vertical
	x = None
	y = None
	width = None
	height = None
	color = None

	def __init__(self, position):
		self.position = position
		self.powerups = []
		self.score = 0 #personnal score of the player
		self.curse_time_start = 0

	def init_from_pos(self, position):
		if position == "Player 0": #left player
			self.orientation = 'v'
			self.xpos = config.WIN_WIDTH // 50
			self.ypos = config.WIN_HEIGHT // 2
			self.width = PLAYER_WIDTH
			self.height = PLAYER_HEIGHT
			self.color = PLAYER_1_COLOR 
		elif position == "Player 1": #right player
			self.orientation = 'v'
			self.xpos = config.WIN_WIDTH - config.WIN_WIDTH // 50
			self.ypos = config.WIN_HEIGHT // 2
			self.width = PLAYER_WIDTH
			self.height = PLAYER_HEIGHT
			self.color = PLAYER_2_COLOR 
		elif position == "Player 2" : #bottom player
			self.orientation = 'h'
			self.xpos = config.WIN_WIDTH // 2
			self.ypos = config.WIN_HEIGHT - config.WIN_HEIGHT // 50
			self.width = PLAYER_HEIGHT
			self.height = PLAYER_WIDTH
			self.color = PLAYER_3_COLOR 
		elif position == "Player 3" : #top player
			self.orientation = 'h'
			self.xpos = config.WIN_WIDTH // 2
			self.ypos = config.WIN_HEIGHT // 50
			self.width = PLAYER_HEIGHT
			self.height = PLAYER_WIDTH
			self.color = PLAYER_4_COLOR 

	def add_score(self):
		self.score += 1

	def move_up(self):
		if self.orientation = 'v':
			if self.ypos - self.height//2 >= 0:
				self.ypos -= self.vel
		else:
			if self.xpos - self.width//2 >= 0:
				self.xpos -= self.vel

	def move_down(self, window):
		if self.orientation = 'v':
			if self.ypos + self.height//2 <= window.height:
				self.ypos += self.vel
		else:
			if self.xpos + self.width//2 <= window.width:
				self.xpos += self.vel

	def curse_players(self, players):
		for player in players:
			if player.position != self.position :
				if player.orientation == 'v' :
					player.height = POWERUP_CURSE_SIZE
				elif player.orientation == 'h' :
					player.width = POWERUP_CURSE_SIZE

	def reset(self, window):
		if self.orientation == 'v' :
			self.y = window.height//2
		else :
			self.x = window.width//2

	def add_powerup(self, powerup):
		if not self.powerups:
			self.powerups.append(powerup)
	
	def use_powerup(self, wall, ball, players):
		if self.powerups:
			if (self.powerups[0].type == config.POWERUP_WALL and not wall.isActive):
				wall.activate(self.color)
				self.powerups.pop(0)
			elif self.powerups[0].type == config.POWERUP_REVERSE:
				ball.reverse_effect()
				self.powerups.pop(0)
			elif self.powerups[0].type == config.POWERUP_CURSE:
				for player in players :
					if player.position != self.position :
						player.curse_time_start = pygame.time.get_ticks()
				self.curse_players(players)
				self.powerups.pop(0)

	def collides_with(self, ball):
		# Simplified collision check with AABB (Axis-Aligned Bounding Box)
		return (self.xpos < ball.xpos + ball.radius and
				self.xpos + self.width > ball.xpos - ball.radius and
				self.ypos < ball.ypos + ball.radius and
				self.ypos + self.height > ball.ypos - ball.radius)

	def update(self):
		if self.height == POWERUP_CURSE_SIZE and self.orientation == 'v' or self.width == POWERUP_CURSE_SIZE and self.orientation == 'h': #if players are cursed, check for timer and revert there size back if duration is over
			if current_time - self.curse_time_start >= POWERUP_CURSE_DURATION * 1000:
				if self.orientation == 'v':
					self.height = PLAYER_HEIGHT
					if self.y - PLAYER_HEIGHT // 2 < 0 :
						self.y = PLAYER_HEIGHT // 2
					if self.y + PLAYER_HEIGHT // 2 > config.WIN_HEIGHT :
						self.y = config.WIN_HEIGHT - PLAYER_HEIGHT // 2
				else:
					self.width = PLAYER_HEIGHT
					if self.x - PLAYER_HEIGHT // 2 < 0 :
						self.x = PLAYER_HEIGHT // 2
					if self.x + PLAYER_HEIGHT // 2 > config.WIN_WIDTH :
						self.x = config.WIN_WIDTH - PLAYER_HEIGHT // 2
				self.curse_time_start = 0



def handle_score(players, ball):
	if ball.x < 0:
		give_score_by_color(players, ball.color)
		ball.reset()
	elif ball.x > config.WIN_WIDTH:
		give_score_by_color(players, ball.color)
		ball.reset()

	if config.NUM_OF_PLAYERS > 2:
		if ball.y > config.WIN_HEIGHT:
			if ball.color != players[2].color :
				give_score_by_color(players, ball.color)
			ball.reset()
		if config.NUM_OF_PLAYERS == 4 and ball.y < 0:
			give_score_by_color(players, ball.color)
			ball.reset()

	#handle winning
	for player in players:
		if player.score == WINNING_SCORE:
			print(player.position, "WON !")
			return (True)