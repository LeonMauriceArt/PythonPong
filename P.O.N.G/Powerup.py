import random
import math

class Powerup:
	def __init__(self, x, y, radius, type):
		self.x = x
		self.y = y
		self.radius = radius
		self.type = type
		self.color = self.getColorType()

	def getColorType(self):
		if self.type == POWERUP_REVERSE:
			return (0, 255, 0)
		elif self.type == POWERUP_WALL:
			return (255, 0, 255)
		elif self.type == POWERUP_CURSE:
			return (0, 255, 255)

	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y),self.radius)
	
	def printuse(self, player):
		print(player, "is using", self.type, "power!")


def spawn_power():
	types = [POWERUP_REVERSE, POWERUP_CURSE, POWERUP_WALL]
	newpower_type =  random.randint(0, 2)
	newpower_x_pos = random.randint(SPAWN_MIN_X, SPAWN_MAX_X)
	newpower_y_pos = random.randint(SPAWN_MIN_Y, SPAWN_MAX_Y)
	newpower = Powerup(newpower_x_pos, newpower_y_pos, POWERUP_RADIUS, types[newpower_type])
	return newpower


def handle_power_collision(ball, powerup, left_player, right_player):
	# Calculate the distance between the centers of the ball and the powerup
	distance = math.sqrt((ball.x - powerup.x)**2 + (ball.y - powerup.y)**2)
	# Check if there is a collision
	if distance <= (ball.radius + powerup.radius):
		if ball.color == PLAYER_1_COLOR and not left_player.powerups:
			left_player.add_powerup(powerup)
			return True
		elif ball.color == PLAYER_2_COLOR and not right_player.powerups:
			right_player.add_powerup(powerup)
			return True
	return False

def power_can_spawn(powerups, last_empty_time):
	current_time = pygame.time.get_ticks()
	if not powerups and (current_time - last_empty_time) > POWERUP_SPAWN_INTERVAL * 1000:
		return True
	return False