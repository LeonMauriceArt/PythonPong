import pygame
pygame.init()

WIN_WIDTH, WIN_HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("LeoPong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100,100,100)

WINNING_SCORE = 5

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

PLAYER_WIDTH, PLAYER_HEIGHT = 20, 100
BALL_RADIUS = 10

#Paddle class
class Paddle:
	#Color of the paddle
	COLOR = WHITE
	#Movement speed of the paddle
	VEL = 6

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	#paddle draw function
	def draw(self, win):
		pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

	#Move function
	def move(self, up=True):
		if up:
			self.y -= self.VEL
		else:
			self.y += self.VEL

	def reset(self):
		self.y = WIN_HEIGHT//2 - PLAYER_HEIGHT//2

#Ball class
class Ball:
	MAX_VEL = 10
	RESET_COOLDOWN = 1500
	COLOR = WHITE

	def __init__(self, x, y, radius):
		self.x = self.original_x = x
		self.y = self.original_y = y
		self.radius = radius
		self.x_vel = self.MAX_VEL
		self.y_vel = 0

	def draw(self, win):
		pygame.draw.circle(win, self.COLOR, (self.x, self.y),self.radius)

	def move(self):
		self.x += self.x_vel
		self.y += self.y_vel

	def	reset(self):
		self.wait_start = pygame.time.get_ticks()
		self.direction = (self.x_vel * -1)
		self.x_vel = 0
		self.y_vel = 0
		self.x = self.original_x
		self.y = self.original_y

	def update(self):
		if self.x_vel == 0:
			current_time = pygame.time.get_ticks()
			if current_time - self.wait_start >= self.RESET_COOLDOWN:
				self.x_vel = self.direction
				self.direction = 0

#draw function to update the display of the background, paddles and everything else
def draw(win, paddles, ball, left_score, right_score):
	win.fill(BLACK)
	left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
	right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
	win.blit(left_score_text, (WIN_WIDTH//4 - left_score_text.get_width()//2, 20))
	win.blit(right_score_text, (WIN_WIDTH * (3/4) - right_score_text.get_width()//2, 20))

	#calling the paddles draw function
	for paddle in paddles:
		paddle.draw(win)
	
	#Drawing the middle line
	for i in range (10, WIN_HEIGHT, WIN_HEIGHT//20):
		if i % 2 == 1:
			continue
		pygame.draw.rect(win, GREY, (WIN_WIDTH//2 - 3, i, 6, WIN_HEIGHT//20))

	ball.draw(win)

	pygame.display.update()

#Handling ball collision
def handle_ball_collision(ball, left_player, right_player):
	#Handling ceiling and floor collision
	if ball.y + ball.radius >= WIN_HEIGHT:
		ball.y_vel *= -1
	elif ball.y - ball.radius <= 0:
		ball.y_vel *= -1

	#Handling left paddle collision with ball
	if ball.x_vel < 0:
		if ball.y >= left_player.y and ball.y <= left_player.y + left_player.height:
			if ball.x - ball.radius <= left_player.x + left_player.width:
				#ball is hitting and bouncing off the left paddle
				ball.x_vel *= -1
				#handling ball y direction based on where it hits
				middle_y = left_player.y + left_player.height / 2
				difference_in_y = middle_y - ball.y
				reduction_factor = (left_player.height / 2) / ball.MAX_VEL
				y_vel = difference_in_y / reduction_factor
				ball.y_vel = -1 * y_vel
	#Handling right paddle collision with ball
	else:
		if ball.y >= right_player.y and ball.y <= right_player.y + right_player.height:
			if ball.x + ball.radius >= right_player.x:
				#ball is hitting and bouncing off the right paddle
				ball.x_vel *= -1
				#handling ball y direction based on where it hits
				middle_y = right_player.y + right_player.height / 2
				difference_in_y = middle_y - ball.y
				reduction_factor = (right_player.height / 2) / ball.MAX_VEL
				y_vel = difference_in_y / reduction_factor
				ball.y_vel = -1 * y_vel


#Handling key pressing for paddle movement
def handle_inputs(keys, left_player, right_player):
	#Left paddle input
	if keys[pygame.K_w] and left_player.y - left_player.VEL >= 0:
		left_player.move(up=True)
	if keys[pygame.K_s] and left_player.y + left_player.VEL + left_player.height <= WIN_HEIGHT:
		left_player.move(up=False)
	#Right paddle input
	if keys[pygame.K_UP] and right_player.y - right_player.VEL >= 0:
		right_player.move(up=True)
	if keys[pygame.K_DOWN] and right_player.y + right_player.VEL + right_player.height <= WIN_HEIGHT:
		right_player.move(up=False)


#Main function
def main():
	run = True
	clock = pygame.time.Clock()

	left_player = Paddle(10, WIN_HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
	right_player = Paddle(WIN_WIDTH - 10 - PLAYER_WIDTH, WIN_HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
	ball = Ball(WIN_WIDTH//2, WIN_HEIGHT//2, BALL_RADIUS)

	left_score = 0
	right_score = 0

#Game loop
	while run :
		clock.tick(FPS)
		draw(WIN, [left_player, right_player], ball, left_score, right_score)

		for event in pygame.event.get ():
			if event.type == pygame.QUIT:
				run = False
				break

		keys = pygame.key.get_pressed()
		handle_inputs(keys, left_player, right_player)
		ball.move()
		handle_ball_collision(ball, left_player, right_player)

		ball.update()
		
		#handle score
		if ball.x < 0:
			right_score += 1
			if right_score < WINNING_SCORE:
				ball.reset()
		elif ball.x > WIN_WIDTH:
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