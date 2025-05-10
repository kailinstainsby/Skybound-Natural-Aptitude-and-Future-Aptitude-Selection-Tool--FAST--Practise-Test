import random
import pygame
import os
from ARC_DB import QuestionDatabase
from ARC_button import Button, ARC_SCREEN_HEIGHT, ARC_SCREEN_WIDTH, pos_y, pos_x

class ARCMinigame:
    def __init__(self):
        pygame.init()

        self.question_count = 0

        # Game settings
        self.TEXT_COL = (0, 255, 0)

        # Minigame dimensions (adjust as needed)
        self.width, self.height = 300, 246
        self.surface = pygame.Surface((self.width, self.height))

        # Load difficulty setting
        base_path = os.path.dirname(os.path.dirname(__file__))  # Absolute path, one level up
        difficulty_path = os.path.join(base_path, "difficulty.txt")

        try:
            with open(difficulty_path, "r") as file:
                self.Difficulty = int(file.read().strip())
        except:
            self.Difficulty = 3

        print(f"ARC Minigame started with Difficulty: {self.Difficulty}")

        # Question settings
        self.question_cooldown = 120 + ((5 - self.Difficulty) * 30)
        self.question_timer = 0
        self.completed_questions = []
        self.question = random.randint(0, 202)

        # Button and answer tracking
        self.buttons = []
        self.selected_answer = None
        self.correct_answers = 0
        self.incorrect_answers = 0

        self.new_question()

    def new_question(self):
        """ Chooses a new question and shuffles the answer order. """
        self.selected_answer = None

        while self.question in self.completed_questions:
            self.question = random.randint(0, 202)

        self.completed_questions.append(self.question)

        order = [0, 1, 2, 3]
        random.shuffle(order)

        answers = [
            QuestionDatabase[self.question][2 + order[0]],
            QuestionDatabase[self.question][2 + order[1]],
            QuestionDatabase[self.question][2 + order[2]],
            QuestionDatabase[self.question][2 + order[3]],
        ]

        self.buttons.clear()  # Reset buttons before adding new ones
        for i in range(4):
            button = Button(answers[i], i + 1,self.width,self.height)
            self.buttons.append(button)

    def draw_text(self, text, y_position):
        """ Renders text onto the minigame surface. """
        font = pygame.font.Font(None, 25 if y_position else 25)
        text_render = font.render(text, True, self.TEXT_COL)
        text_rect = text_render.get_rect(center=(self.width / 2, self.height / (4 if y_position else 1.5)))
        self.surface.blit(text_render, text_rect)

    def update(self, main_surface):
        # updates the minigame logic and renders it onto the surface
        self.surface.fill((0, 0, 0))  # Clear the minigame area

        mouse_x, mouse_y = pygame.mouse.get_pos()
        relative_mouse_pos = (mouse_x - pos_x, mouse_y - pos_y)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(relative_mouse_pos):
                        self.selected_answer = button.text

        # Timer logic
        self.question_timer += 1
        if self.question_timer < self.question_cooldown:
            self.draw_text(QuestionDatabase[self.question][0], True)
            self.draw_text(QuestionDatabase[self.question][1], False)
        elif self.question_timer < 2 * self.question_cooldown:
            for button in self.buttons:
                button.draw(self.surface, None, self.selected_answer == button.text)
        else:
            if self.selected_answer == QuestionDatabase[self.question][2]:
                self.correct_answers += 1
                self.question_count += 1 
            else:
                self.incorrect_answers += 1
                self.question_count += 1 
            print("correct", self.correct_answers, "incorrect", self.incorrect_answers)

            self.question_timer = 0
            self.new_question()

        # Blit the minigame onto the main surface
        main_surface.blit(self.surface, (pos_x, pos_y))  # Adjust position as needed
