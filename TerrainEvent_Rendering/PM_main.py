import random
import pygame
import os
from PM_setup import SCREEN_WIDTH, SCREEN_HEIGHT, PLANE_WIDTH, PLANE_HEIGHT, white, black, cloud_spacing
from PM_plane import Plane
from PM_clouds import Cloud
from PM_hitbox import Collision

# Get absolute path
base_path = os.path.dirname(os.path.dirname(__file__))  # Go one path level up
difficulty_path = os.path.join(base_path, "difficulty.txt")

pygame.init()

# Load difficulty setting
try:
    with open(difficulty_path, "r") as file:
        Difficulty = int(file.read().strip())
except:
    Difficulty = 3
print(f"Game started with Difficulty: {Difficulty}")

# Adjust difficulty settings
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

# Initialize game objects
plane = Plane()
cloudList = []
cloud_spawn_timer = 0
collisions = 0
collision_cooldown = 1000
last_collision = 0

def run_plane_minigame(surface, delta_time):
    global cloud_spawn_timer, last_collision, collisions, cloudList
    
    # Plane movement
    plane.movement()

    # Cloud spawning logic
    cloud_spawn_timer += 1
    if cloud_spawn_timer > cloud_spawn_rate:
        gap_height = PLANE_HEIGHT + 50
        gap_start = random.randint(0, SCREEN_HEIGHT - gap_height)

        if Difficulty >= 4:
            for y in range(0, SCREEN_HEIGHT, cloud_spacing):
                if not (gap_start <= y < gap_start + gap_height):
                    if random.random() < cloud_spawn_chance:
                        cloudList.append(Cloud(surface.get_width(), y))
        else:
            y = random.randint(0, SCREEN_HEIGHT//15) * 15
            cloud_count = random.randint(2, 8)
            for i in range(cloud_count):
                cloudList.append(Cloud(surface.get_width() + i * cloud_spacing, y))

        cloud_spawn_timer = 0

    current_time = pygame.time.get_ticks()

    # Move and remove clouds
    for cloud in cloudList[:]:  # Iterate over a copy to avoid modifying while looping
        cloud.move()
        if cloud.off_screen():
            cloudList.remove(cloud)

        # Collision detection
        if current_time - last_collision > collision_cooldown:
            if (
                plane.hitbox.colliderect(cloud.hitbox)
                or plane.hitbox_topWing.colliderect(cloud.hitbox)
                or plane.hitbox_botWing.colliderect(cloud.hitbox)
            ):
                collisions += 1
                print(collisions)
                last_collision = current_time
                plane.start_notify()

    # Draw everything on the given surface
    surface.fill(black)
    plane.notify()
    plane.add_plane_at_location(surface)
    
    for cloud in cloudList:
        cloud.draw(surface)
