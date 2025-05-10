from setup import GAME, SCREEN_WIDTH, SCREEN_HEIGHT, PLANE_WIDTH, PLANE_HEIGHT, white, black, cloud_spacing, SCREEN
import pygame
import sys
from clouds import Cloud
from plane import Plane

class Collision:
	def __init__(self, Cloud, Plane):
		self.cloud = Cloud
		self.plane = Plane

	def collide(self):
		return self.cloud.cloud_hitbox > self.plane.plane_hitbox