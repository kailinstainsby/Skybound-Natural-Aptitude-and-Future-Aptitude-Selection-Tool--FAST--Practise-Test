import random
import sys
import pygame
from DB3 import QuestionDatabase
from button import Button, SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()


# game settings
TEXT_COL = (0, 255, 0)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Active Reasoning Challenges")

clock = pygame.time.Clock()


# difficulty settings
import os

base_path = os.path.dirname(os.path.dirname(__file__))  # get absolute path, go one path level up
difficulty_path = os.path.join(base_path, "difficulty.txt")
try:
    with open(difficulty_path, "r") as file:
        Difficulty = int(file.read().strip())
except:
    Difficulty = 3
print(f"Game started with Difficulty: {Difficulty}")


# put text onto screen
def text(text, y):
	if y == True:
		font = pygame.font.Font(None, 35)
		text = font.render(text, True, TEXT_COL)
		text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
	else:
		font = pygame.font.Font(None, 40)
		text = font.render(text, True, TEXT_COL)
		text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/1.5))
	SCREEN.blit(text, text_rect)


# question settings
question_cooldown = 120 + ((5-Difficulty) * 30)
question_timer = 0
question = random.randint(0, 203)
completed_questions = []

# button stuffs
buttons = []


# grabs and chooses random new question + buttons
def new_question():
	global question, buttons, selected_answer

	selected_answer = None

	while question in completed_questions:
		question = random.randint(0, 202)

	completed_questions.append(question)

	order = [0, 1, 2, 3]
	random.shuffle(order)

	answers = [
		QuestionDatabase[question][2 + order[0]],
		QuestionDatabase[question][2 + order[1]],
		QuestionDatabase[question][2 + order[2]],
		QuestionDatabase[question][2 + order[3]],
	]

	for i in range(4):
		button = Button(answers[i], i + 1)
		buttons.append(button)

new_question()

correct_answers = 0
incorrect_answers = 0

# game loop
GAME = True 
while GAME == True:

	SCREEN.fill((0, 0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			for button in buttons:
				if button.is_clicked(event.pos):
					selected_answer = button.text

	""" if the timer is reached after ticks, then the 
	questions are displayed, and after some more times 
	they are reset and a new question is chosen. """
	question_timer += 1
	if question_timer < question_cooldown:
		text(QuestionDatabase[question][0], True)
		text(QuestionDatabase[question][1], False)

	elif question_timer < 2*question_cooldown:
		for button in buttons:
			button.draw(SCREEN, None, selected_answer == button.text)

	else:
		if selected_answer == QuestionDatabase[question][2]:
			correct_answers += 1
		else:
			incorrect_answers += 1
		print(correct_answers)
		print(incorrect_answers)

		question_timer = 0
		new_question()


	pygame.display.update()
	clock.tick(30)

pygame.quit()

