from setup import GAME, SCREEN_WIDTH, SCREEN_HEIGHT, PLANE_WIDTH, PLANE_HEIGHT, SCREEN, red
import pygame
import sys
import math

class Plane:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/plane-topdown-sprite.png').convert_alpha() # transparent background
        self.x = 20
        self.y = 0

        self.hitbox = (self.x+16, self.y+38, PLANE_WIDTH-30, PLANE_HEIGHT-75)
        self.hitbox_topWing = (self.x+27, self.y+5, PLANE_WIDTH-90, PLANE_HEIGHT-80)
        self.hitbox_botWing = (self.x+27, self.y+75, PLANE_WIDTH-90, PLANE_HEIGHT-80)

        self.visible = True
        self.flicker_start_time = 0
        self.flickering = False

    def movement(self): # movement of plane on input
        key = pygame.key.get_pressed()
        distance = 6
        if key[pygame.K_DOWN]:
            if key[pygame.K_UP]: # makes sure if both keys are pressed, plane stops moving
                self.y = self.y
            else:
                self.y += distance
        elif key[pygame.K_UP]:
            self.y -= distance

        if self.y < 0: # ensures plane does not go off the window
            self.y = 0
        elif self.y > SCREEN_HEIGHT-PLANE_HEIGHT:
            self.y = SCREEN_HEIGHT-PLANE_HEIGHT

    def plane_hitbox(self):
        self.hitbox = pygame.Rect(self.x+16, self.y+38, PLANE_WIDTH-30, PLANE_HEIGHT-75)
        self.hitbox_topWing = pygame.Rect(self.x+27, self.y+5, PLANE_WIDTH-90, PLANE_HEIGHT-80)
        self.hitbox_botWing = pygame.Rect(self.x+27, self.y+75, PLANE_WIDTH-90, PLANE_HEIGHT-80)


    def add_plane_at_location(self, SCREEN): # scales plane to preferences and adds to window
        if self.visible == True:
            self.image = pygame.transform.scale(self.image, (PLANE_WIDTH, PLANE_HEIGHT))
            SCREEN.blit(self.image, (self.x,self.y))
        Plane.plane_hitbox(self)

    def start_notify(self):
        self.flicker_start_time = pygame.time.get_ticks()
        self.flickering = True

    def notify(self):
        if self.flickering:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.flicker_start_time

            if elapsed_time <= 1000:
                if (elapsed_time // 167) % 2 == 0:
                    self.visible = True
                else:
                    self.visible = False

            else:
                self.flickering = False
                self.visible = True