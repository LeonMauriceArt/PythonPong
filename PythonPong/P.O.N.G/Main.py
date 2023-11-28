import Ball
import Players
import Powerup
import Colors
import config
import Wall

from Wall import Wall
from config import *
from Players import *
from Powerup import *
from Ball import *
from Colors import *

POWERUP_SPAWN_INTERVAL = 5

#DISPLAY INIT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("P.O.N.G")

#draw function to update the display of the background, paddles and everything else
def draw(win, paddles, ball, left_score, right_score, powerups, wall):
	win.fill(BLACK)
	#Drawing the middle line
	for i in range (10, HEIGHT, HEIGHT//20):
		if i % 2 == 1:
			continue
		pygame.draw.rect(win, GREY, (WIDTH//2 - 3, i, 6, HEIGHT//20))
	left_score_text = SCORE_FONT.render(f"{left_score}", 1, PLAYER_1_COLOR)
	right_score_text = SCORE_FONT.render(f"{right_score}", 1, PLAYER_2_COLOR)
	win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
	win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

	for paddle in paddles:
		paddle.draw(win)

	for powerup in powerups:
		powerup.draw(win)
	
	wall.draw(win)

	ball.draw(win)

	pygame.display.update()

def power_can_spawn(powerups, last_empty_time):
	current_time = pygame.time.get_ticks()
	if not powerups and (current_time - last_empty_time) > POWERUP_SPAWN_INTERVAL * 1000:
		return True
	return False

def return_player_to_normal(left_player, right_player):
	current_time = pygame.time.get_ticks()
	if left_player.height == POWERUP_CURSE_SIZE and (current_time - left_player.CURSE_time_start) >= POWERUP_CURSE_DURATION * 1000:
		left_player.height = PADDLE_HEIGHT
		left_player.CURSE_time_start = 0
	if right_player.height == POWERUP_CURSE_SIZE and (current_time - right_player.CURSE_time_start) >= POWERUP_CURSE_DURATION * 1000:
		right_player.height = PADDLE_HEIGHT
		right_player.CURSE_time_start = 0

#Main function
def main():
	run = True
	clock = pygame.time.Clock()

	left_player = Player(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PLAYER_1_COLOR)
	right_player = Player(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PLAYER_2_COLOR)
	ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS, WHITE)
	wall = Wall()

	#handling powerups instances
	powerups = []
	last_empty_time = pygame.time.get_ticks()

	left_score = 0
	right_score = 0

	#Game loop
	while run :
		clock.tick(FPS)
		draw(WIN, [left_player, right_player], ball, left_score, right_score, powerups, wall)

		for event in pygame.event.get ():
			if event.type == pygame.QUIT:
				run = False
				break

		if power_can_spawn(powerups, last_empty_time):
			powerups.append(spawn_power()) 

		keys = pygame.key.get_pressed()
		handle_inputs(keys, left_player, right_player, ball, wall)
		ball.move()
		handle_ball_collision(ball, left_player, right_player, wall)

		if powerups:
			if handle_power_collision(ball, powerups[0], left_player, right_player):
				powerups.pop(0)
				last_empty_time = pygame.time.get_ticks()

		ball.update()
		wall.update()
		left_player.update()
		right_player.update()
		
		#handle score
		if ball.x < 0:
			right_score += 1
			if right_score < WINNING_SCORE:
				ball.reset()
		elif ball.x > WIDTH:
			left_score += 1
			if left_score < WINNING_SCORE:
				ball.reset()
		
		#handle winning
		if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
			left_score = 0
			right_score = 0
			left_player.reset()
			right_player.reset()
			ball.reset()

	pygame.quit()

if __name__ == '__main__':
	main()