import pygame
import sys

import config

from Player import Player, handle_inputs, handle_score
from Ball import Ball, handle_ball_collision
from Wall import Wall
from Powerup import Powerup, spawn_power, handle_power_collision, power_can_spawn

def init_players(num_of_players): #init players
	players = []
	players = [Player(f'Player {i}') for i in range(num_of_players)]
	return players

#Main function
# def main():
# 	if config.NUM_OF_PLAYERS > 2:
# 		config.WIN_WIDTH = config.WIN_HEIGHT # if there is more than 2 player, the game area should be a square
# 		config.SPAWN_MIN_X = config.WIN_WIDTH // 4
# 		config.SPAWN_MAX_X = config.WIN_WIDTH - config.WIN_WIDTH // 4
# 		config.SPAWN_MIN_Y = config.WIN_HEIGHT // 4
# 		config.SPAWN_MAX_Y = config.WIN_HEIGHT - config.WIN_HEIGHT // 4


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
			self.handle_score()
			self.ball.reset()

	def handle_score(self):
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
				return (True)

	def give_score_by_color(self): #add a point to the player with the same color as the ball when it hits a player goal
		for player in self.players:
			if player.color == self.ball.color:
				player.add_score()
				return

	def get_state(self):
		return {
			'window': self.window.to_dict(),
			'player1': self.player1.to_dict(),
			'player2': self.player2.to_dict(),
			'player3': self.player3.to_dict(),
			'player4': self.player4.to_dict(),
			'ball': self.ball.to_dict(),
			'pause': self.pause_game
		}
