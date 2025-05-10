import pygame
import sys

class Button():
    def __init__(self, x, y, image, scale):
        # initialising all details of a button required
        width = image.get_width()
        height = image.get_height()
        self.original_width = width
        self.original_height = height
        self.original_image = image
        self.image = pygame.transform.scale(image, (int(self.original_width * scale), int(self.original_height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False
        self.enlarged = False
        self.scale = scale

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check if position of mouse and the button overlap
        if self.rect.collidepoint(pos):
            if not self.enlarged:
                self.enlarged = True
                # enlarge by 20%
                enlarged_width = int(self.original_width * self.scale * 1.2) 
                enlarged_height = int(self.original_height * self.scale * 1.2)
                self.image = pygame.transform.scale(self.original_image, (enlarged_width, enlarged_height))
                # keeps it centered 
                self.rect = self.image.get_rect(center=self.rect.center)

            # checks to see if mouse is clicked once and isnt already active
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            # if not clicked then clicked is false
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        else:
            if self.enlarged:
                self.enlarged = False
                # puts image back to original size and stuff
                self.image = pygame.transform.scale(self.original_image, (int(self.original_width * self.scale), int(self.original_height * self.scale)))
                self.rect = self.image.get_rect(center=self.rect.center)


        #actually outputs the button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        #returns the boolean action variable which is active when clicked
        return action
