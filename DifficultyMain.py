import pygame
import sys
from button import Button
import subprocess

import os

pygame.init()

# screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360

# initialise screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# text settings
font = pygame.font.SysFont(None, 30)
TEXT_COL = (0, 0, 0)

Difficulty_1 = pygame.image.load("UI_Sprites/1.png").convert_alpha()
Difficulty_2 = pygame.image.load("UI_Sprites/2.png").convert_alpha()
Difficulty_3 = pygame.image.load("UI_Sprites/3.png").convert_alpha()
Difficulty_4 = pygame.image.load("UI_Sprites/4.png").convert_alpha()
Difficulty_5 = pygame.image.load("UI_Sprites/5.png").convert_alpha()

SkyboundLogo = pygame.image.load("UI_Sprites/skybound_title.png").convert_alpha()

InfoImage = pygame.image.load("UI_Sprites/info-button.png").convert_alpha()
LeftImage = pygame.image.load("UI_Sprites/left.png").convert_alpha()
RightImage = pygame.image.load("UI_Sprites/right.png").convert_alpha()

LogoButton = Button(190, 55, SkyboundLogo, 0.15)
InfoButton = Button(20, 10, InfoImage, 0.4)
LeftButton = Button(280, 300, LeftImage, 0.4)
RightButton = Button(310, 300, RightImage, 0.4)
Button1 = Button(50, 205, Difficulty_1, 1)
Button2 = Button(150, 205, Difficulty_2, 1)
Button3 = Button(250, 205, Difficulty_3, 1)
Button4 = Button(350, 205, Difficulty_4, 1)
Button5 = Button(450, 205, Difficulty_5, 1)


# text method
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	SCREEN.blit(img, (x, y))

GAME = True 

Difficulty = 0
info = False
page = 1

###################################################
while GAME == True:

	SCREEN.fill((255, 255, 255))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME = False

	if info == True:
		if page == 1:
			draw_text("SKYBOUND is a Pilot Natural Aptitude Test simulator,", font, TEXT_COL, 80, 30)
			draw_text("which is intended to be used for aspiring cadets, or", font, TEXT_COL, 80, 60)
			draw_text("anyone who wishes to practise their natural ability to", font, TEXT_COL, 80, 90)
			draw_text("multitask, problem-solve and improve.", font, TEXT_COL, 80, 120)
			draw_text("To start the program, you must first click on a difficulty", font, TEXT_COL, 80, 170)
			draw_text("button, and then you may proceed by pressing the logo,", font, TEXT_COL, 80, 200)
			draw_text("which will then start the practise test.", font, TEXT_COL, 80, 230)

		if page == 2:
			draw_text("During the test, there will be 3 sections which you will", font, TEXT_COL, 80, 10)
			draw_text("be required to interact with, such as:", font, TEXT_COL, 80, 40)
			draw_text("Plane Minigame: you will be required to use your up/down", font, TEXT_COL, 50, 90)
			draw_text("arrow keys to ensure your plane avoids the obstacles.", font, TEXT_COL, 50, 120)
			draw_text("Questions: you will be asked basic reasoning questions", font, TEXT_COL, 50, 150)
			draw_text("throughout, requiring you to choose an answer.", font, TEXT_COL, 50, 180)
			draw_text("POV: you will need to watch the terrain as you 'fly' in", font, TEXT_COL, 50, 210)
			draw_text("your plane, clicking the 'Aircraft' button when you spot one,", font, TEXT_COL, 50, 240)
			draw_text("an aircraft, and the 'Waypoint' button when you change", font, TEXT_COL, 50, 270)
			draw_text("your bearing.", font, TEXT_COL, 50, 300)

		if page > 1:
			if LeftButton.draw(SCREEN):
				page -= 1

		if page < 2:
			if RightButton.draw(SCREEN):
				page += 1

		if InfoButton.draw(SCREEN):
			info = False
	else:

		if InfoButton.draw(SCREEN):
			info = True

		if Button1.draw(SCREEN):
			Difficulty = 1
			print(Difficulty)

		if Button2.draw(SCREEN):
			Difficulty = 2
			print(Difficulty)

		if Button3.draw(SCREEN):
			Difficulty = 3
			print(Difficulty)

		if Button4.draw(SCREEN):
			Difficulty = 4
			print(Difficulty)

		if Button5.draw(SCREEN):
			Difficulty = 5
			print(Difficulty)

		if LogoButton.draw(SCREEN):
			print("logo clicked")
			if Difficulty > 0:
				print(f"Launching Plane Minigame with Difficulty: {Difficulty}")

				with open("difficulty.txt", "w") as file:
					file.write(str(Difficulty))

		        # run plane minigame
				subprocess.run(["python", "TER_main.py"], cwd="TerrainEvent_Rendering")
				GAME = False  # exit menu after launching game

	pygame.display.update()

pygame.quit()

