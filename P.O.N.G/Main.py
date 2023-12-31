import pygame
import sys
import config
import Player
import Ball
import Wall

#draw function to update the display of the background, players and everything else
def draw(win, players, ball, powerups, wall):
	win.fill(BLACK)

	# left_score_text = SCORE_FONT.render(f"{left_score}", 1, PLAYER_1_COLOR)
	# right_score_text = SCORE_FONT.render(f"{right_score}", 1, PLAYER_2_COLOR)
	# win.blit(left_score_text, (WIN_WIDTH//4 - left_score_text.get_width()//2, 20))
	# win.blit(right_score_text, (WIN_WIDTH * (3/4) - right_score_text.get_width()//2, 20))

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
	NUM_OF_PLAYERS = get_num_of_players()
	if NUM_OF_PLAYERS > 2:
		WIN_WIDTH = WIN_HEIGHT # if there is more than 2 player, the game area should be a square
	WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # pygame window init
	pygame.display.set_caption("P.O.N.G")

	#init players
	players = init_players(NUM_OF_PLAYERS)
	for player in players:
		player.init_from_pos(player.position)

	run = True
	clock = pygame.time.Clock()

	ball = Ball(WIN_WIDTH//2, WIN_HEIGHT//2, BALL_RADIUS, WHITE)
	wall = Wall()

	#handling powerups instances
	powerups = []
	last_empty_time = pygame.time.get_ticks()

	#Game loop
	while run :
		clock.tick(FPS)
		draw(WIN, players, ball, powerups, wall)

		for event in pygame.event.get ():
			if event.type == pygame.QUIT:
				run = False
				break

		# if power_can_spawn(powerups, last_empty_time):
		# 	powerups.append(spawn_power()) 

		keys = pygame.key.get_pressed()
		handle_inputs(keys, players, ball, wall)
		ball.move()
		handle_ball_collision(ball, players, wall)

		# if powerups:
		# 	if handle_power_collision(ball, powerups[0], left_player, right_player):
		# 		powerups.pop(0)
		# 		last_empty_time = pygame.time.get_ticks()

		ball.update()
		wall.update()
		for player in players:
			player.update()

		if handle_score(players, ball):
			break

	pygame.quit()

if __name__ == "__main__":
	main()