import pygame
import sys

GAME = True

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 450

# window declaration and settings
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plane Minigame")

PLANE_HEIGHT = SCREEN_WIDTH//7
PLANE_WIDTH = PLANE_HEIGHT*1.2

cloud_spacing = 30

white = (255, 255, 255)
black = (0, 0, 0)
red = (170, 74, 68)

