import pygame
import random
import sys

from TER_setup import SCREEN_HEIGHT, SCREEN_WIDTH
from TER_buttons import menu_x_pos, menu_y_pos

pygame.init()

class Light:
	def __init__(self, x_pos, max_flashes):
		#images
		self.sprite_inactive = pygame.image.load("TER_Sprites/lightinactive.png").convert_alpha()
		self.sprite_active = pygame.image.load("TER_Sprites/lightactive.png").convert_alpha()

		self.y_pos = menu_y_pos - 15
		self.x_pos = x_pos

		self.active = False # is it supposed to flash ?
		self.flash_count = 0 # will increase each time flash is called
		self.max_flashes = random.randint(2, max_flashes)
		self.flash_length = 30 #0.5 seconds when 60 ticks, always constant
		self.flash_timer = 0 # will turn into the length and count down

		self.flash_times = sorted(random.sample(range(18000), self.max_flashes))
		self.flash_index = 0
		self.elapsed_time = 0

	def update(self):
		self.elapsed_time += 1

		if self.active:
			self.flash_timer -= 1
			if self.flash_timer <= 0:
				self.active = False

		else:
			if self.flash_index < len(self.flash_times) and self.elapsed_time >= self.flash_times[self.flash_index]:
				self.flash()
				self.flash_index += 1


	def flash(self):
		self.active = True
		self.flash_timer = self.flash_length
		self.flash_count += 1


	def draw(self, screen):
		if self.active:
			img = self.sprite_active
		else:
			img = self.sprite_inactive

		screen.blit(img, (self.x_pos, self.y_pos))
