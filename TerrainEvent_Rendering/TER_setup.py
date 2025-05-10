import pygame
import math
import math
pygame.init()

SCREEN_WIDTH = 1920 // 2
SCREEN_HEIGHT = 1080 // 2

backgroundImage = pygame.image.load("TER_Sprites/backdrop.png")
scale_factor = 1

new_width = int(backgroundImage.get_width() * scale_factor)
new_height = int(backgroundImage.get_height() * scale_factor)
background = pygame.transform.smoothscale(backgroundImage, (new_width, new_height))

rotation_angle = 0
rotation_target = 0
rotation_speed = 0.25
rotating = False
rotation_timer = 0

class Cloud:
	def __init__(self, spawn_pos_x, spawn_pos_y):
		self.cloudImage = pygame.image.load("TER_Sprites/cloud.png").convert_alpha()
		self.x = spawn_pos_x
		self.y = spawn_pos_y
		self.x_size = 10
		self.y_size = 1

	def draw(self, screen, rotation_angle):
		cloud = pygame.transform.smoothscale(self.cloudImage, (self.x_size, self.y_size))
		rotated_cloud = pygame.transform.rotate(cloud, rotation_angle)
		#new_rect = rotated_cloud.get_rect(topleft=(self.x, self.y))
		screen.blit(rotated_cloud, (self.x, self.y))

	def move(self):
		distance = ( ( self.x ) - (SCREEN_WIDTH / 2) ) / 1000
		self.x += distance
		self.x_size += (0.01*math.exp((0.05*self.x_size)-(0.045*self.x_size)))+0.1
		self.y_size += (0.01*math.exp((0.05*self.y_size)-(0.045*self.y_size)))+0.1

		self.x_size = min(self.x_size, 3000)
		self.y_size = min(self.y_size, 3000)

	def rotation_translate(self, rotation_angle):
		if rotation_angle != 0:
			angle_rad = math.radians(rotation_angle)
			y_pos_dampener = -rotation_angle / rotation_angle

			self.x += (self.x*math.cos(angle_rad))*0.0077
			self.y -= (self.y*math.sin(angle_rad))*0.0077 + (y_pos_dampener*0.1)





