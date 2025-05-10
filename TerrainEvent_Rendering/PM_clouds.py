import random
import pygame
import sys
from PM_setup import GAME, SCREEN_WIDTH, SCREEN_HEIGHT, PLANE_WIDTH, PLANE_HEIGHT, white, SCREEN, red

class Cloud:
	def __init__(self, x, y, width=15, height=15):
		self.width = width
		self.height = height
		self.colour = (white)
		self.x = x
		self.y = y
		self.hitbox = (self.x, self.y, self.width, self.height)

	def cloud_hitbox(self):
		self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

	def draw(self, SCREEN): # adding the cloud to the screen
		pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.width, self.height))
		Cloud.cloud_hitbox(self)

	def move(self): # moving the cloud's x value each time method is called
		distance = 2
		self.x -= distance

	def off_screen(self): # returns a boolean for when the entire square is off-screen
		return self.width + self.x < 0

