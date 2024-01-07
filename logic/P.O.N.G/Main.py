import pygame
import sys

import config

from Player import Player, handle_inputs, handle_score
from Ball import Ball, handle_ball_collision
from Wall import Wall
from Powerup import Powerup, spawn_power, handle_power_collision, power_can_spawn

def get_num_of_players(): #get and set the number of players from the program arguments
	if len(sys.argv) != 2:
		return 2
	else:
		number_of_players = int(sys.argv[1])
		if number_of_players < 2:
			return 2
		if number_of_players > 4:
			return 4
		return number_of_players

def init_players(num_of_players): #init players
	players = []
	players = [Player(f'Player {i}') for i in range(num_of_players)]
	return players

#Main function
def main():
	config.NUM_OF_PLAYERS = get_num_of_players()
	if config.NUM_OF_PLAYERS > 2:
		config.WIN_WIDTH = config.WIN_HEIGHT # if there is more than 2 player, the game area should be a square
		config.SPAWN_MIN_X = config.WIN_WIDTH // 4
		config.SPAWN_MAX_X = config.WIN_WIDTH - config.WIN_WIDTH // 4
		config.SPAWN_MIN_Y = config.WIN_HEIGHT // 4
		config.SPAWN_MAX_Y = config.WIN_HEIGHT - config.WIN_HEIGHT // 4
	config.WIN = pygame.display.set_mode((config.WIN_WIDTH, config.WIN_HEIGHT)) # pygame window init
	pygame.display.set_caption("P.O.N.G")

	#init players
	players = init_players(config.NUM_OF_PLAYERS)
	for player in players:
		player.init_from_pos(player.position)

	run = True
	clock = pygame.time.Clock()

	ball = Ball(config.WIN_WIDTH//2, config.WIN_HEIGHT//2, config.BALL_RADIUS, config.WHITE)
	wall = Wall()

	#handling powerups instances
	powerups = []
	last_empty_time = pygame.time.get_ticks()

	#Game loop
	while run :
		clock.tick(config.FPS)
		draw(config.WIN, players, ball, powerups, wall)

		for event in pygame.event.get ():
			if event.type == pygame.QUIT:
				run = False
				break


		keys = pygame.key.get_pressed()
		handle_inputs(keys, players, ball, wall)
		ball.move()
		handle_ball_collision(ball, players, wall)



		ball.update()
		wall.update(ball)
		for player in players:
			player.update()

		if handle_score(players, ball):
			break


class Window:
	def __init__(self, width, height):
		self.width, self.height = width, height

	def to_dict(self):  
		return {
			'width': self.width,
			'height': self.height
		}

class Game:
	def __init__(self, window, num_of_players):
		self.window = window
		self.num_of_players = num_of_players
		self.reset_game()
		print('Game initialized')

	def reset_game(self):
		self.players = {0: None, 1: None, 2:None, 3:None}
		self.player1 = Player(50, self.window.height / 2)
		self.player2 = Player(self.window.width - 50, self.window.height / 2)
		self.ball = Ball(self.window.width / 2, self.window.height / 2)
		self.powerups = []
		self.pause_game = True
		self.running = False

	def loop(self):
		if not self.pause_game:
			self.ball.move()
			self.check_collisions()
		if config.POWERUP_ENABLE :
			if power_can_spawn(powerups, last_empty_time):
				powerups.append(spawn_power()) 
			if powerups:
				if handle_power_collision(ball, powerups[0], players):
					powerups.pop(0)
					last_empty_time = pygame.time.get_ticks()

	def move_player(self, player, direction):
		if player == 1:
			if direction == 'up':
				self.player1.move_up()
			elif direction == 'down':
				self.player1.move_down(self.window)
		elif player == 2:
			if direction == 'up':
				self.player2.move_up()
			elif direction == 'down':
				self.player2.move_down(self.window)

	def check_collisions(self):
		# Player and ball collision
		if self.player1.collides_with(self.ball):
			self.ball.handle_ball_collision(self.player1)
			self.ball.xpos = self.player1.xpos + self.player1.width + self.ball.radius

		if self.player2.collides_with(self.ball):
			self.ball.handle_ball_collision(self.player2)
			self.ball.xpos = self.player2.xpos - self.ball.radius

		if self.ball.ypos - self.ball.radius <= 0 or self.ball.ypos + self.ball.radius >= self.window.height:
			self.ball.reflect_vertical()

		if self.powerups[0] and self.powerups[0].collides_with(self.ball):
			
		#borders
		if self.ball.xpos - self.ball.radius <= 0 or self.ball.xpos + self.ball.radius >= self.window.width:
			self.ball.reset()
			self.handle_score()

	def handle_score(self):
		if self.ball.xpos - self.ball.radius <= 0:
			self.player2.add_score()
		if self.ball.xpos + self.ball.radius >= self.window.width:
			self.player1.add_score()
		if self.player1.score == WINNING_SCORE or self.player2.score == WINNING_SCORE:
			if self.player1.score == WINNING_SCORE:
				print("Player 1 won !")
			else:
				print("Player 2 won !")
			self.running = False
			self.pause_game = True

	def get_state(self):
		return {
			'window': self.window.to_dict(),
			'player1': self.player1.to_dict(),
			'player2': self.player2.to_dict(),
			'ball': self.ball.to_dict(),
			'pause': self.pause_game
		}
