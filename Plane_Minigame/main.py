import random
from setup import GAME, SCREEN_WIDTH, SCREEN_HEIGHT, PLANE_WIDTH, PLANE_HEIGHT, white, black, cloud_spacing, SCREEN
from plane import Plane
import pygame
import sys
from clouds import Cloud
from hitbox import Collision

import os

# get absolute path
base_path = os.path.dirname(os.path.dirname(__file__))  # Go one path level up

difficulty_path = os.path.join(base_path, "difficulty.txt")

pygame.init()

plane = Plane()

collisions = 0
collision_cooldown = 1000
last_collision = 0

cloudList = []
cloud_spawn_timer = 0

clock = pygame.time.Clock()

try:
    with open(difficulty_path, "r") as file:
        Difficulty = int(file.read().strip())
except:
    Difficulty = 3
print(f"Game started with Difficulty: {Difficulty}")

cloud_spawn_rate = 80
cloud_spawn_chance = 0.3

if Difficulty == 1:
    cloud_spawn_rate = 300
if Difficulty == 2:
    cloud_spawn_rate = 200
if Difficulty == 3:
    cloud_spawn_rate = 125
if Difficulty == 4:
    cloud_spawn_chance = 0.5
    cloud_spawn_rate = 200
if Difficulty == 5:
    cloud_spawn_chance = 0.7
    cloud_spawn_rate = 150


while GAME == True: # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME = False

    # plane movement
    plane.movement()

    # cloud spawn timer
    cloud_spawn_timer += 1
    if cloud_spawn_timer > cloud_spawn_rate:

        gap_height = PLANE_HEIGHT + 50
        gap_start = random.randint(0, SCREEN_HEIGHT - gap_height)

        if Difficulty >= 4:
            for y in range(0, SCREEN_HEIGHT, cloud_spacing):
                if not (gap_start <= y < gap_start + gap_height):
                    if random.random() < cloud_spawn_chance:
                        cloudList.append(Cloud(SCREEN_WIDTH, y))

        if Difficulty < 4:
            y = random.randint(0, SCREEN_HEIGHT//30) * 30
            cloud_count = random.randint(2,8)

            for i in range(cloud_count):
                cloudList.append(Cloud(SCREEN_WIDTH + i* cloud_spacing, y))

        cloud_spawn_timer = 0

    current_time = pygame.time.get_ticks()
    # moves and REmoves clouds 
    for cloud in cloudList:
        cloud.move()
        if cloud.off_screen():
            cloudList.remove(cloud)

        # collision detection
        if current_time - last_collision > collision_cooldown:
            if plane.hitbox.colliderect(cloud.hitbox):
                collisions += 1
                print(collisions)
                last_collision = current_time
                plane.start_notify()


            elif plane.hitbox_topWing.colliderect(cloud.hitbox):
                collisions += 1
                print(collisions)
                last_collision = current_time
                plane.start_notify()


            elif plane.hitbox_botWing.colliderect(cloud.hitbox):
                collisions += 1
                print(collisions)
                last_collision = current_time
                plane.start_notify()

    # setting the screen / drawing screen
    SCREEN.fill(black)

    plane.notify()
    plane.add_plane_at_location(SCREEN)

    # spawn the clouds
    for cloud in cloudList:
        cloud.draw(SCREEN)

    # update the screen
    pygame.display.update()
    clock.tick(60) # fps / refresh rate

pygame.quit()

