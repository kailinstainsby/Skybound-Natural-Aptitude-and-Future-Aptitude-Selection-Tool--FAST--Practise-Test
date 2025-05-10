import pygame

pygame.init()

# screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 450

class Button:
    def __init__(self, text, pos):
        self.text = text  # store answer text
        self.width = SCREEN_WIDTH // 2  # each button fills half width or height
        self.height = SCREEN_HEIGHT // 2
        self.set_position(pos)

    def set_position(self, pos):
        if pos == 1:
            self.button = pygame.Rect(0, 0, self.width, self.height)  # Top-left
        elif pos == 2:
            self.button = pygame.Rect(self.width, 0, self.width, self.height)  # Top-right
        elif pos == 3:
            self.button = pygame.Rect(0, self.height, self.width, self.height)  # Bottom-left
        elif pos == 4:
            self.button = pygame.Rect(self.width, self.height, self.width, self.height)  # Bottom-right

    def draw(self, screen, font, selected):
    	if font is None:
    		font = pygame.font.Font(None, 36)

    	# draw the button with text and highlight if selected
    	color = (50, 50, 50) if selected else (0, 0, 0)  # green if selected, gray otherwise
    	pygame.draw.rect(screen, color, self.button)

    	# render text in the center of the button
    	text_surface = font.render(self.text, True, (0, 255, 0))
    	text_rect = text_surface.get_rect(center=self.button.center)
    	screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        # check if  button is clicked
        return self.button.collidepoint(pos)
