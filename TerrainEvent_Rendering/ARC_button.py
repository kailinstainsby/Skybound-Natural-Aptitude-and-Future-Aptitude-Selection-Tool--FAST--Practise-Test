import pygame

pygame.init()

# screen dimensions
ARC_SCREEN_WIDTH = 300
ARC_SCREEN_HEIGHT = 246
pos_x = 960-ARC_SCREEN_WIDTH-45
pos_y = 270

class Button:
    def __init__(self, text, pos, ARC_SCREEN_WIDTH, ARC_SCREEN_HEIGHT):
        self.text = text  # store answer text
        self.font = pygame.font.Font(None, 18)

        self.width = ARC_SCREEN_WIDTH // 2  # each button fills half width or height
        self.height = ARC_SCREEN_HEIGHT // 2

        positions = [
            (0, 0),
            (self.width, 0),
            (0, self.height),
            (self.width, self.height),
        ]

        self.x, self.y = positions[pos - 1]
        self.button = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, font, selected):
        # draw the button with text and highlight if selected
        color = (50, 50, 50) if selected else (0, 0, 0)  # green if selected, gray otherwise
        pygame.draw.rect(screen, color, self.button)

        # render text in the center of the button
        text_surface = self.font.render(self.text, True, (0, 255, 0))
        text_rect = text_surface.get_rect(center=self.button.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        # check if  button is clicked
        return self.button.collidepoint(pos)
