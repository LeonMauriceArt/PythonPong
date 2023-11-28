import pygame

pygame.init()

WIDTH, HEIGHT = 700, 500

FPS = 60

#RULE SETTINGS
WINNING_SCORE = 5

#POWERUPS
POWERUP_RADIUS = 15
POWERUP_SPAWN_TIME = 5
SPAWN_MIN_X = 100
SPAWN_MAX_X = 600
SPAWN_MIN_Y = 100
SPAWN_MAX_Y = 400

#PADDLE AND BALL SETTINGS
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_RADIUS = 10
BALL_SPEED = 5

POWERUP_REVERSE = "Reverse"
POWERUP_WALL = "Wall"
POWERUP_CURSE = "Curse"
POWERUP_WALL_DURATION = 0.5
POWERUP_CURSE_SIZE = PADDLE_HEIGHT * 0.3
POWERUP_CURSE_DURATION = 5

WALL_WIDTH = 10



SCORE_FONT = pygame.font.SysFont("comicsans", 50)