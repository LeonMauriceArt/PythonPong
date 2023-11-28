import config
import Colors

from config import *
from Colors import *

#Ball class
class Ball:
	RESET_COOLDOWN = 1500

	def __init__(self, x, y, radius, color):
		self.x = self.original_x = x
		self.y = self.original_y = y
		self.radius = radius
		self.x_vel = BALL_SPEED
		self.y_vel = 0
		self.color = color

	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y),self.radius)

	def move(self):
		self.x += self.x_vel
		self.y += self.y_vel

	def	reset(self):
		self.wait_start = pygame.time.get_ticks()
		self.direction = (self.x_vel * -1)
		self.color = WHITE
		self.x_vel = 0
		self.y_vel = 0
		self.x = self.original_x
		self.y = self.original_y

	def reverse_effect(self):
		self.x_vel *= -1
		self.y_vel *= -1

	def update(self):
		if self.x_vel == 0:
			current_time = pygame.time.get_ticks()
			if current_time - self.wait_start >= self.RESET_COOLDOWN:
				self.x_vel = self.direction
				self.direction = 0


#Handling ball collision
def handle_ball_collision(ball, left_player, right_player, wall):
	#Handling ceiling and floor collision
	if ball.y + ball.radius >= HEIGHT:
		ball.y_vel *= -1
	elif ball.y - ball.radius <= 0:
		ball.y_vel *= -1

	#Handling left paddle collision with ball
	if ball.x_vel < 0:
		#Wall collision
		if ball.x >= WIDTH//2:
			if ball.x - wall.width <= WIDTH//2 + wall.width and wall.isActive:
				ball.x_vel *= -1
				middle_y = HEIGHT//2
				difference_in_y = middle_y - ball.y
				reduction_factor = (middle_y / 2) / BALL_SPEED
				y_vel = difference_in_y / reduction_factor
				ball.y_vel = -1 * y_vel
		#Player collision
		elif ball.y >= left_player.y and ball.y <= left_player.y + left_player.height:
			if ball.x - ball.radius <= left_player.x + left_player.width:
				#ball is hitting and bouncing off the left paddle
				ball.x_vel *= -1
				ball.color = PLAYER_1_COLOR
				#handling ball y direction based on where it hits
				middle_y = left_player.y + left_player.height / 2
				difference_in_y = middle_y - ball.y
				reduction_factor = (left_player.height / 2) / BALL_SPEED
				y_vel = difference_in_y / reduction_factor
				ball.y_vel = -1 * y_vel
	#Handling right paddle collision with ball
	else:
		#Wall collision
		if ball.x <= WIDTH//2:
			if ball.x + wall.width >= WIDTH//2 - wall.width and wall.isActive:
				ball.x_vel *= -1
				middle_y = HEIGHT//2
				difference_in_y = middle_y - ball.y
				reduction_factor = (middle_y / 2) / BALL_SPEED
				y_vel = difference_in_y / reduction_factor
				ball.y_vel = -1 * y_vel
		#Player collision
		elif ball.y >= right_player.y and ball.y <= right_player.y + right_player.height:
			if ball.x + ball.radius >= right_player.x:
				#ball is hitting and bouncing off the right paddle
				ball.x_vel *= -1
				ball.color = PLAYER_2_COLOR
				#handling ball y direction based on where it hits
				middle_y = right_player.y + right_player.height / 2
				difference_in_y = middle_y - ball.y
				reduction_factor = (right_player.height / 2) / BALL_SPEED
				y_vel = difference_in_y / reduction_factor
				ball.y_vel = -1 * y_vel
