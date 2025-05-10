import pygame
import random

from TER_setup import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()

menu_width = SCREEN_WIDTH // 5 #192
menu_height = SCREEN_HEIGHT // 2.5 + 30 #246
menu_x_pos = SCREEN_WIDTH // 2 - menu_width//2
menu_y_pos = SCREEN_HEIGHT//2

menu_rect = pygame.Rect(menu_x_pos, menu_y_pos, menu_width, menu_height)

menu_overlay_img = pygame.image.load("TER_Sprites/menu1.png")
menu_overlay = pygame.transform.smoothscale(menu_overlay_img, (menu_width, menu_height))

class Button:
	def __init__(self, img):
		self.x_pos = menu_x_pos + 20
		#image changes based on boolean, if true, button = aircraft button
		if img == True:
			self.img = pygame.image.load("TER_Sprites/aircraftbutton.png")
			self.y_pos = menu_y_pos + 20
		else:
			self.img = pygame.image.load("TER_Sprites/waypointbutton.png")
			self.y_pos = menu_y_pos + 60

		self.rect = self.img.get_rect()
		self.rect.topleft = (self.x_pos, self.y_pos)
		self.was_clicked = False

	def draw(self, screen):
		action = False
		# get mouse pos
		pos = pygame.mouse.get_pos()
		mouse_input = pygame.mouse.get_pressed()[0]

		# checks if the mouse is on the button, and also if the mouse clicks
		if self.rect.collidepoint(pos):
			if mouse_input and not self.was_clicked:
				action = True

		self.was_clicked = mouse_input

		#blits image
		screen.blit(self.img, (self.x_pos, self.y_pos))

		#returns if the button is clicked or not
		return action

