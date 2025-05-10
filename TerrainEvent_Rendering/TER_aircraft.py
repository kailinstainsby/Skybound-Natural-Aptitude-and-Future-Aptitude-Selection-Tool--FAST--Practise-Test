import pygame
import random
import sys

import math

from TER_setup import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()


class Aircraft:
	def __init__(self, x_pos, y_pos, aircraft_type):
		self.clicked = False

		if aircraft_type == 3:
			self.speed = 0.5
			self.image = pygame.image.load("TER_Sprites/plane3.png").convert_alpha()
			self.x_size, self.y_size = 40, 40

		if aircraft_type == 4:
			self.speed = 0.5
			self.image = pygame.image.load("TER_Sprites/plane3.png").convert_alpha()
			self.x_size, self.y_size = 40, 40

		if aircraft_type == 5:
			self.speed = 2.0
			self.image = pygame.image.load("TER_Sprites/plane5.png").convert_alpha()
			self.x_size, self.y_size = 100, 100

		if aircraft_type == 6:
			self.speed = 0.8
			self.image = pygame.image.load("TER_Sprites/plane6.png").convert_alpha()
			self.x_size, self.y_size = 40, 40

		if aircraft_type == 7:
			self.speed = 2.7
			self.image = pygame.image.load("TER_Sprites/plane7.png").convert_alpha()
			self.x_size, self.y_size = 100, 100

		if aircraft_type == 8:
			self.speed = 3.0
			self.image = pygame.image.load("TER_Sprites/plane8.png").convert_alpha()
			self.x_size, self.y_size = 40, 40

		else:
			self.speed = 0.5
			self.image = pygame.image.load("TER_Sprites/plane0.png").convert_alpha()
			self.x_size, self.y_size = 30, 30


		self.y_pos = y_pos

		if x_pos == False:
			self.x_pos = 0 - self.x_size
			self.image = pygame.transform.flip(self.image, True, False)
		else:
			self.x_pos = SCREEN_WIDTH
			self.speed = - self.speed

		self.original_y_pos = self.y_pos
		self.original_x_pos = self.x_pos

		self.radius = 100

	def draw(self, screen, rotation_angle):
		aircraft = pygame.transform.smoothscale(self.image, (self.x_size, self.y_size))
		rotated_aircraft = pygame.transform.rotate(aircraft, rotation_angle)
		new_rect = rotated_aircraft.get_rect(topleft=(self.x_pos, self.y_pos))
		screen.blit(rotated_aircraft, new_rect.topleft)


	def move(self):
		self.x_pos += self.speed
		self.y_size += 0.05
		self.x_size += 0.05

	def rotation_translate(self, rotation_angle):
		if rotation_angle != 0:
			angle_rad = math.radians(rotation_angle)
			y_pos_dampener = -rotation_angle / rotation_angle

			self.x_pos += (self.x_pos*math.cos(angle_rad))*0.0077
			self.y_pos -= (self.y_pos*math.sin(angle_rad))*0.0077 + (y_pos_dampener*0.1)




