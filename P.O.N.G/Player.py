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
			self.x = config.WIN_WIDTH // 50
			self.y = config.WIN_HEIGHT // 2
			self.width = PLAYER_WIDTH
			self.height = PLAYER_HEIGHT
			self.color = PLAYER_1_COLOR 
		elif position == "Player 1": #right player
			self.orientation = 'v'
			self.x = config.WIN_WIDTH - config.WIN_WIDTH // 50
			self.y = config.WIN_HEIGHT // 2
			self.width = PLAYER_WIDTH
			self.height = PLAYER_HEIGHT
			self.color = PLAYER_2_COLOR 
		elif position == "Player 2" : #bottom player
			self.orientation = 'h'
			self.x = config.WIN_WIDTH // 2
			self.y = config.WIN_HEIGHT - config.WIN_HEIGHT // 50
			self.width = PLAYER_HEIGHT
			self.height = PLAYER_WIDTH
			self.color = PLAYER_3_COLOR 
		elif position == "Player 3" : #top player
			self.orientation = 'h'
			self.x = config.WIN_WIDTH // 2
			self.y = config.WIN_HEIGHT // 50
			self.width = PLAYER_HEIGHT
			self.height = PLAYER_WIDTH
			self.color = PLAYER_4_COLOR 
	
	def draw(self, win): #player draw function
		# print("---", self.position, " | ", self.orientation, self.x, self.y, self.width, self.height, self.color)
		pygame.draw.rect(win, self.color, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))

	#Move function
	def move(self, up=True):
		if self.orientation == 'v' :
			if up and self.y - self.VEL - self.height // 2 >= 0:
				self.y -= self.VEL
			elif not up and self.y + self.VEL + self.height // 2 <= config.WIN_HEIGHT:
				self.y += self.VEL
		elif self.orientation == 'h' :
			if up and self.x + self.VEL + self.width // 2 <= config.WIN_WIDTH:
				self.x += self.VEL
			elif not up and self.x - self.VEL - self.width // 2 >= 0:
				self.x -= self.VEL

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
			if opponent.y + opponent.height > config.WIN_HEIGHT:
				opponent.y = config.WIN_HEIGHT - opponent.height

	def reset(self):
		self.y = config.WIN_HEIGHT//2 - PLAYER_HEIGHT//2

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
				retract_amount = POWERUP_CURSE_SIZE - PLAYER_HEIGHT
				self.y += retract_amount // 2
				self.height -= retract_amount
				self.CURSE_time_start = 0


#Handling key pressing for paddle movement
def handle_inputs(keys, players, ball, wall):
	#Left paddle input
	if keys[pygame.K_UP] :
		for player in players:
			if player.orientation == 'v':
				player.move(up=True)
	if keys[pygame.K_DOWN] :
		for player in players:
			if player.orientation == 'v':
				player.move(up=False)	
	if keys[pygame.K_LEFT] :
		for player in players:
			if player.orientation == 'h':
				player.move(up=False)
	if keys[pygame.K_RIGHT] :
		for player in players:
			if player.orientation == 'h':
				player.move(up=True)

	#---POWERUP USAGE NEED TO BE REWORKED---
	# if keys[pygame.K_SPACE]:
	# 	for player in players:
	# 		player.use_powerup()

def return_player_to_normal(player):
	current_time = pygame.time.get_ticks()
	if left_player.height == POWERUP_CURSE_SIZE and (current_time - left_player.CURSE_time_start) >= POWERUP_CURSE_DURATION * 1000:
		left_player.height = PLAYER_HEIGHT
		left_player.CURSE_time_start = 0
	if right_player.height == POWERUP_CURSE_SIZE and (current_time - right_player.CURSE_time_start) >= POWERUP_CURSE_DURATION * 1000:
		right_player.height = PLAYER_HEIGHT
		right_player.CURSE_time_start = 0

def handle_score(players, ball):
	if ball.x < 0:
		players[0].score += 1
		ball.reset()
	elif ball.x > config.WIN_WIDTH:
		players[1].score += 1
		ball.reset()

	if config.NUM_OF_PLAYERS > 2:
		if ball.y > config.WIN_HEIGHT:
			players[2].score += 1
			ball.reset()
		if config.NUM_OF_PLAYERS == 4 and ball.y == 0:
			players[3].score += 1
			ball.reset()

	#handle winning
	for player in players:
		if player.score == WINNING_SCORE:
			print("PLAYER", player.position, "WON !")
			return (True)