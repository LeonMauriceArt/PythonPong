import pygame
import sys

import config

from Player import Player, handle_inputs, handle_score
from Ball import Ball, handle_ball_collision
from Wall import Wall
from Powerup import Powerup, spawn_power, handle_power_collision, power_can_spawn

#draw function to update the display of the background, players and everything else
def draw(win, players, ball, powerups, wall):
	win.fill(config.BLACK)
	for player in players:
		player.draw(win)
	for powerup in powerups:
		powerup.draw(win)
	#updating 
	wall.draw(win)
	ball.draw(win)
	pygame.display.update()


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
	pygame.init()
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

		if config.POWERUP_ENABLE :
			if power_can_spawn(powerups, last_empty_time):
				powerups.append(spawn_power()) 
			if powerups:
				if handle_power_collision(ball, powerups[0], players):
					powerups.pop(0)
					last_empty_time = pygame.time.get_ticks()

		ball.update()
		wall.update()
		for player in players:
			player.update()

		if handle_score(players, ball):
			break

	pygame.quit()

if __name__ == "__main__":
	main()