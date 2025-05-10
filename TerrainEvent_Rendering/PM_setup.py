import pygame
import sys

GAME = True

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 246

# window declaration and settings
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plane Minigame")

PLANE_HEIGHT = round(SCREEN_WIDTH * (1/7))
PLANE_WIDTH = (PLANE_HEIGHT*1.2)

cloud_spacing = 15

white = (255, 255, 255)
black = (0, 0, 0)
red = (170, 74, 68)

