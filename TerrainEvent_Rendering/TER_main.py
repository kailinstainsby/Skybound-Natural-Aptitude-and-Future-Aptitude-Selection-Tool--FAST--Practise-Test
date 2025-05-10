import pygame
import sys
import random
import math

from TER_setup import SCREEN_WIDTH, SCREEN_HEIGHT, background, scale_factor, Cloud, rotation_angle, rotation_target, rotation_speed, rotating, rotation_timer
from TER_aircraft import Aircraft
from TER_waypoints import Waypoint

from TER_buttons import menu_rect, menu_overlay, menu_x_pos, menu_y_pos, Button

from TER_lights import Light

from PM_main import run_plane_minigame, collisions

from ARC_main import ARCMinigame

from PRC_main1 import QuizPopup

from button import Button_Report

#basic init and setup
pygame.init()

clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MAIN")

# difficulty
import os

base_path = os.path.dirname(os.path.dirname(__file__))  # Go one path level up

difficulty_path = os.path.join(base_path, "difficulty.txt")

try:
    with open(difficulty_path, "r") as file:
        Difficulty = int(file.read().strip())
except:
    Difficulty = 3
print(f"Game started with Difficulty: {Difficulty}")

#plane minigame set
plane_minigame_surface = pygame.Surface((300, 246))

#active reasoning minigame set
arc_minigame = ARCMinigame()

reasoning_minigame_surface = pygame.Surface((300, 246))


#cloud setup
cloudList = []
cloud_timer = 0
cloud_cooldown = random.randint(600, 800)

#aircraft setup
aircraftList = []
aircraft_timer = 0
aircraft_cooldown = random.randint(150,300)
aircraft_number = 0

#waypoint setup
waypointList = []
waypoint_timer = 0
waypoint_cooldown = random.randint(150, 300)
waypoint_number = 0
waypoint_active = False

#buttons
aircraft_button = Button(True)
aircraft_clicked_correct = 0
aircraft_clicked_incorrect = 0

waypoint_button = Button(False)
waypoint_clicked_correct = 0
waypoint_clicked_incorrect = 0

#max flashes based on difficulty
max_flashes = Difficulty + 5

#lights
light_left = Light(SCREEN_WIDTH // 2, max_flashes)
light_right = Light((SCREEN_WIDTH // 2) + 40, max_flashes)

game_length = 7200
ticks = 0

rotation_origin = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)

QUIZwaypointList = []

quiz = QuizPopup(
    SCREEN, 
    aircraft_number, waypoint_number, 
    light_left.flash_count, light_right.flash_count, 
    light_left.flash_count + light_right.flash_count, 
    QUIZwaypointList
)

text_colour = ((0, 0, 0))

#Button section and creating instances
LeftButton_Img = pygame.image.load("Other_Sprites/left.png").convert_alpha()
RightButton_Img = pygame.image.load("Other_Sprites/right.png").convert_alpha()
LeftButton = Button_Report(420, 460, LeftButton_Img, 0.8)
RightButton = Button_Report(480, 460, RightButton_Img, 0.8)
page = 1

# Weightings
# multi tasking Rating
plane_collisions_weight = 0.7  # plane collisions weigh heaviest
active_recall_correct_weight = 0.2  # correct active recall answers have some weight
active_recall_incorrect_weight = 0.1  # wrong answers have a lower impact

# pattern Recognition Score
pattern_recognition_incorrect_penalty = 0.5  # harsh penalty for incorrect inputs
pattern_recognition_dropoff_threshold = 2  #large drop-off occurs after 2 incorrect answers

#memory Recall Score
memory_recall_percentage = 100  # direct % of correct answers
memory_recall_target = 100  # goal is full accuracy so this is target

# observation Rating
observation_missed_penalty = 10  # missed events penalized exponentially


def text(text,x,y, size):
	font = pygame.font.Font(None, size)
	text = font.render(text, True, text_colour)
	text_rect = text.get_rect(center=(x, y))
	SCREEN.blit(text, text_rect)

def pass_fail():
    # no division by 0 errors because itll crash the game
    waypoint_accuracy = waypoint_clicked_correct / waypoint_number if waypoint_number > 0 else 0
    aircraft_accuracy = aircraft_clicked_correct / aircraft_number if aircraft_number > 0 else 0
    arc_score = arc_minigame.correct_answers / arc_minigame.question_count if arc_minigame.question_count > 0 else 0
    quiz_score = quiz.correct_answers / (quiz.questions_asked - 1) if (quiz.questions_asked - 1) > 0 else 0
    
    # collision penalty (scaled so that high collisions reduce the score)
    collision_penalty = max(0, 1 - (collisions / 10))

    #weighted final score
    final_score = (0.3 * waypoint_accuracy) + (0.3 * aircraft_accuracy) + (0.2 * arc_score) + (0.2 * quiz_score) - (0.1 * collision_penalty)

    # determine pass/fail
    if final_score >= 0.8:
        text(f"PASS! Final Score: {final_score:.2f}", SCREEN_WIDTH//2, 50, 60)
    else:
        text(f"FAIL. Final Score: {final_score:.2f}", SCREEN_WIDTH//2, 50, 60)


#game loop
GAME = True
while GAME == True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME = False
		quiz.handle_event(event)

	ticks += 1
	if ticks >= game_length and quiz.active == False:
		quiz.aircraft_count = aircraft_number
		quiz.waypoint_count = waypoint_number
		quiz.left_flashes = light_left.flash_count
		quiz.right_flashes = light_right.flash_count
		quiz.total_flashes = light_left.flash_count + light_right.flash_count
		quiz.waypoints = QUIZwaypointList

		quiz.generate_question()

	if quiz.active:
		quiz.draw()

	if quiz.questions_asked >= 4:
		SCREEN.fill((255,255,255))
		if page == 1: # after prc report should come on screen
			text(f"You collided with {collisions} clouds", SCREEN_WIDTH//2, 150, 45)
			text(f"You detected {waypoint_clicked_correct} / {waypoint_number} waypoints, and misinput {waypoint_clicked_incorrect}", SCREEN_WIDTH//2, 200, 45)
			text(f"You detected {aircraft_clicked_correct} / {aircraft_number} aircraft, and misinput {aircraft_clicked_incorrect}", SCREEN_WIDTH//2, 250, 45)
			text(f"You correctly answered {arc_minigame.correct_answers} / {arc_minigame.question_count} active questions", SCREEN_WIDTH//2, 300, 45)
			text(f"You correctly recalled {quiz.correct_answers} / {quiz.questions_asked - 1} questions", SCREEN_WIDTH//2, 350, 45)
			pass_fail()

			if RightButton.draw(SCREEN):
				page += 1
		if page == 2:
			# Multi-tasking score
			collision_penalty = max(0, 1 - (collisions / 10))  # Strong penalty for collisions

			# Multi-tasking score calculation
			multitasking_score = (
			    (plane_collisions_weight * collision_penalty) +  # Strongly weighted on avoiding collisions
			    (active_recall_correct_weight * (arc_minigame.correct_answers / arc_minigame.question_count if arc_minigame.question_count > 0 else 0)) + 
			    (active_recall_incorrect_weight * (1 - (arc_minigame.correct_answers / arc_minigame.question_count if arc_minigame.question_count > 0 else 0)))  
			) * 100


			# Pattern recognition score
			active_recall_accuracy = (arc_minigame.correct_answers / arc_minigame.question_count) if arc_minigame.question_count > 0 else 0
			incorrect_penalty = min(1, (arc_minigame.question_count - arc_minigame.correct_answers) * pattern_recognition_incorrect_penalty / pattern_recognition_dropoff_threshold)

			pattern_recognition_score = max(0, (active_recall_accuracy - incorrect_penalty)) * 100


			# Memory recall score
			memory_recall_score = (quiz.correct_answers / (quiz.questions_asked - 1) * 100) if (quiz.questions_asked - 1) > 0 else 0

			# Observation score
			total_events = waypoint_number + aircraft_number  # Total things to observe
			correct_observations = waypoint_clicked_correct + aircraft_clicked_correct
			incorrect_observations = waypoint_clicked_incorrect + aircraft_clicked_incorrect
			missed_observations = total_events - correct_observations if total_events > 0 else 0

			# Score calculation
			observation_score = max(0, 100 - (incorrect_observations * observation_missed_penalty) - (missed_observations ** 1.5))


			text(f"You achieved a multitasking score of {multitasking_score:.2f}%", SCREEN_WIDTH//2, 100, 50)
			text(f"You achieved a pattern recognition score of {pattern_recognition_score:.2f}%", SCREEN_WIDTH//2, 150, 50)
			text(f"You achieved a memory recall score of {memory_recall_score:.2f}%", SCREEN_WIDTH//2, 200, 50)
			text(f"You achieved a observation rating of {observation_score:.2f}%", SCREEN_WIDTH//2, 250, 50)

			if LeftButton.draw(SCREEN):
				page -= 1

	if quiz.active == False and ticks <= game_length:
		# waypoint spawn logic
		waypoint_timer += 1
		if waypoint_timer > waypoint_cooldown and random.randint(0,1) == 1 and len(waypointList) == 0:

			waypoint_timer = 0
			waypoint_cooldown = random.randint(1500, 3000)

			waypoint_active = True

			#rotation logic
			rotation_timer = 300 #5 seconds
			rotating = True
			rotation_target = random.choice([-15, 15]) #randomly rotates either left or right

			if rotation_target > 0:
				x_pos = x_pos = random.randint(SCREEN_WIDTH // 2 + 100, SCREEN_WIDTH - 300)
			else:
				x_pos = random.randint(300, SCREEN_WIDTH // 2 - 100)
			waypoint_type = random.randint(0,2)
			waypointList.append(Waypoint(x_pos, waypoint_type))
			QUIZwaypointList.append(waypoint_type)

			waypoint_number += 1


		if rotating:
			if rotation_timer > 0:
				rotation_timer -= 1
			else:
				if abs(rotation_angle - rotation_target) >= 0.5:
					rotation_angle += rotation_speed * (1 if rotation_target > rotation_angle else -1)
				else:
					rotation_target = 0

				if abs(rotation_angle) <= 0.5 and rotation_target == 0:
					rotating = False
		else:
			rotation_angle = 0

		rotated_background = pygame.transform.rotate(background, rotation_angle)
		bg_rect = rotated_background.get_rect(center=rotation_origin)
		SCREEN.blit(rotated_background, bg_rect.topleft)

		for waypoint in waypointList:
			waypoint.draw(SCREEN, rotation_angle)
			waypoint.move()

			if waypoint.x_pos > SCREEN_WIDTH + 200 or waypoint.x_pos + waypoint.x_size < -200:
				waypointList.remove(waypoint)

				waypoint_active = False

			if rotating:
				waypoint.rotation_translate(rotation_angle)

		# cloud spawn logic
		cloud_timer += 1
		if cloud_timer > cloud_cooldown:
			isSpawnCloud = random.randint(0, 1)
			if isSpawnCloud == 1:
				cloud_spawn = random.randint(100, int(SCREEN_WIDTH - 100))
				cloudList.append(Cloud(cloud_spawn, 180))
			cloud_timer = 0
			cloud_cooldown = random.randint(120, 300)

		#spawning the clouds and moving them
		for cloud in cloudList:
			cloud.draw(SCREEN, rotation_angle)
			cloud.move()

			if cloud.x > SCREEN_WIDTH or cloud.x + cloud.x_size < 0:
				cloudList.remove(cloud)

			if rotating:
				cloud.rotation_translate(rotation_angle)

		aircraft_timer += 1
		if aircraft_timer > aircraft_cooldown and len(aircraftList) < 2 and random.randint(0, 1) == 1:
			if Difficulty > 3:
				plane_type = random.randint(0,8)
			else:
				plane_type = random.randint(0,3)

			x_pos = bool(random.randint(0,1))
			y_pos = random.randint(20, 80)

			aircraftList.append(Aircraft(x_pos, y_pos, plane_type))

			aircraft_number += 1

			aircraft_timer = 0
			aircraft_cooldown = random.randint(1500,3000)

		for aircraft in aircraftList:
			aircraft.draw(SCREEN, rotation_angle)
			aircraft.move()

			if aircraft.x_pos > SCREEN_WIDTH + 500 or aircraft.x_pos + aircraft.x_size < -500:
				aircraftList.remove(aircraft)

			if rotating:
				aircraft.rotation_translate(rotation_angle)
		#pygame.draw.rect(SCREEN, (50, 50, 50), (0, SCREEN_HEIGHT - SCREEN_HEIGHT//3, SCREEN_WIDTH, SCREEN_HEIGHT))

		pygame.draw.rect(SCREEN, (0, 0, 0), menu_rect)
		SCREEN.blit(menu_overlay, (menu_x_pos, menu_y_pos))

		if waypoint_button.draw(SCREEN) == True:
			if waypoint_active:
				waypoint_clicked_correct += 1
				print("correct",waypoint_clicked_correct)
				waypoint_active = False
			else:
				waypoint_clicked_incorrect += 1
				print("incorrect",waypoint_clicked_incorrect)

		if aircraft_button.draw(SCREEN):
			clicked_any = False

			for aircraft in aircraftList:
				if not aircraft.clicked:
					aircraft.clicked = True 
					aircraft_clicked_correct += 1
					clicked_any = True
					print("correct",aircraft_clicked_correct)
					break
			if not clicked_any:
				aircraft_clicked_incorrect += 1
				print("incorrect",aircraft_clicked_incorrect)

		#calling light updates
		light_left.update()
		light_left.draw(SCREEN)

		light_right.update()
		light_right.draw(SCREEN)

		delta_time = clock.tick(60) / 1000.0
		run_plane_minigame(plane_minigame_surface, delta_time)
		SCREEN.blit(plane_minigame_surface, (45, menu_y_pos))

		arc_minigame.update(SCREEN)

	pygame.display.update()
	clock.tick(60)

pygame.quit()

