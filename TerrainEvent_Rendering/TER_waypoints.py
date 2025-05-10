import pygame
import random
import sys
import math

from TER_setup import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()

class Waypoint:
	def __init__(self, x_pos, waypoint_type):
		self.speed = 0.5
		self.x_size, self.y_size = 30, 30

		if waypoint_type == 0:
			self.image = pygame.image.load("TER_Sprites/waypoint0.png").convert_alpha()
		if waypoint_type == 1:
			self.image = pygame.image.load("TER_Sprites/waypoint1.png").convert_alpha()
		else:
			self.image = pygame.image.load("TER_Sprites/wapoint2.png").convert_alpha()

		self.x_pos = x_pos
		self.y_pos = 180

	def draw(self, screen, rotation_angle):
		waypoint = pygame.transform.smoothscale(self.image, (self.x_size, self.y_size))
		rotated_waypoint = pygame.transform.rotate(waypoint, rotation_angle)
		#new_rect = rotated_waypoint.get_rect(center=(self.x_pos, self.y_pos))
		screen.blit(rotated_waypoint, (self.x_pos, self.y_pos))
		#screen.blit(rotated_waypoint, new_rect.topleft)

	def move(self):
		distance = ( ( self.x_pos ) - (SCREEN_WIDTH / 2) ) / 1000
		self.x_pos += distance
		self.x_size += (0.01*math.exp((0.05*self.x_size)-(0.045*self.x_size)))+0.05
		self.y_size += (0.01*math.exp((0.05*self.y_size)-(0.045*self.y_size)))+0.05

		self.x_size = min(self.x_size, 3000)
		self.y_size = min(self.y_size, 3000)

	def rotation_translate(self, rotation_angle):
		if rotation_angle != 0:
			angle_rad = math.radians(rotation_angle)
			y_pos_dampener = -rotation_angle / rotation_angle

			self.x_pos += (self.x_pos*math.cos(angle_rad))*0.0077
			self.y_pos -= (self.y_pos*math.sin(angle_rad))*0.0077 + (y_pos_dampener*0.1)

