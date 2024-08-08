import pygame
import random
import math
import logging
import os
import time
import datetime

from tree2 import Tree2
from creature2 import Creature2

NUM_CREATURES = 70
NUM_TREES = 50

# Log file path
log_file = 'simulation5.log'

# Check if the log file exists and delete it
if os.path.exists(log_file):
    os.remove(log_file)

# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Log the start time of the run
start_time = time.time()
start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
logger.info(f"Simulation started at {start_time_str}")
print(f"Simulation started at {start_time_str}")

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simulation5')

#tree_surf = pygame.image.load('images/fruit_tree-8.png').convert_alpha()

creature_images = [
    pygame.image.load(f'images/creature_g{i}.png').convert_alpha() for i in range(9)
]
tree_images = [
    pygame.image.load(f'images/fruit_tree-{i}.png').convert_alpha() for i in range(1, 9)
]

# Add trees from nothing, these trees have no genetic inheritance from parents
def add_initial_tree(trees, image, screen_width, screen_height):
    new_tree = Tree2(
        image=image[0],
        initial_scale=0.1,
        parent=0,
        carrier=0,
        position=(random.randint(0, screen_width), random.randint(0, screen_height)),
        growth_rate=random.uniform(0.05, 0.12),
        growth_interval=random.randint(4000, 8000)
    )
    trees.add(new_tree)

# Add tree spread by creature
def add_tree_from_creature(trees, creature, image, screen_width, screen_height):
    if creature.trees_eaten_from:
        parent = creature.trees_eaten_from[0]
    else:
        parent = 000  # this would indicate that the creature has just digested "initial" food
    new_tree = Tree2(
        image=image[0],
        initial_scale=0.1,
        parent=parent,
        carrier=creature.unique_id,
        position=(random.randint(0, screen_width), random.randint(0, screen_height)),
        growth_rate=random.uniform(0.05, 0.12),
        growth_interval=random.randint(4000, 8000)
    )
    trees.add(new_tree)

# Add creatures from nothing, these creatures have no genetic inheritance from parents
#def add_initial_creature(creatures, image, screen_width, screen_height):
def add_initial_creature(creatures, creature_images, screen_width, screen_height):
    generation = 0
    image = creature_images[generation]
    # These variables are genetic traits that must be created here new:
    #   speed,
    #   stomach_size,
    #   starvation_time_limit,
    #   food_reduction_interval
    new_creature = Creature2(
        image=image,
        initial_scale=0.5,
        parent1=0,
        parent2=0,
        position=(random.randint(0, screen_width), random.randint(0, screen_height)),
        speed=random.uniform(6, 12),
        generation=generation,
        stomach_size = random.randint(2, 5),
        starvation_time_limit = random.randint(15000, 25000),  # Time limit before starvation in milliseconds, can represent fat/energy stores
        food_reduction_interval = random.randint(7500, 12500)  # Time interval to reduce food in stomach by 1 in milliseconds
    )
    creatures.add(new_creature)
    logger.debug("New creature spawned from nothing:")
    logger.debug(new_creature)

def print_trees_and_creatures(trees, dead_trees, creatures, dead_creatures):
    logger.info("Alive Trees:")
    for tree in trees:
        logger.info(tree)
    logger.debug("\nDead Trees:")
    for tree in dead_trees:
        logger.debug(tree)
    logger.debug("\nCreatures:")
    for creature in creatures:
        logger.info(creature)
    logger.debug("\nDead Creatures:")
    for creature in dead_creatures:
        logger.debug(creature)
    logger.debug("-" * 40)

def print_only_creatures(creatures, dead_creatures):
    logger.info("\nCreatures:")
    for creature in creatures:
        logger.info(creature)
        print(creature)
    for creature in dead_creatures:
        logger.info(creature)
        # print(creature)
    logger.info("-" * 40)
    print("-" * 40)

def check_proximity(sprite1, sprite2, distance):
    """Check if sprite1 is within a certain distance of sprite2."""
    center1 = sprite1.rect.center
    center2 = sprite2.rect.center
    dx = center1[0] - center2[0]
    dy = center1[1] - center2[1]
    return math.sqrt(dx * dx + dy * dy) <= distance

# Create sprite groups
trees = pygame.sprite.Group()
creatures = pygame.sprite.Group()
dead_trees = []
dead_creatures = []

# Add initial trees and creatures
for _ in range(NUM_TREES):
    add_initial_tree(trees, tree_images, SCREEN_WIDTH, SCREEN_HEIGHT)
for _ in range(NUM_CREATURES):
    add_initial_creature(creatures, creature_images, SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()

# Log the initial trees and creatures
print_trees_and_creatures(trees, dead_trees, creatures, dead_creatures)

run = True
while run:
    dt = clock.tick(60) / 1000.0
    keys = pygame.key.get_just_pressed()

    if keys[pygame.K_x]:
        run = False
    if keys[pygame.K_t]:
        add_initial_tree(trees, tree_images, SCREEN_WIDTH, SCREEN_HEIGHT)
    if keys[pygame.K_c]:
        add_initial_creature(creatures, creature_images, SCREEN_WIDTH, SCREEN_HEIGHT)
    if keys[pygame.K_p]:
        print_trees_and_creatures(trees, dead_trees, creatures, dead_creatures)
    if keys[pygame.K_o]:
        print_only_creatures(creatures, dead_creatures)

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False

    display_surface.fill("lightgreen")

    # Update and draw creatures
    for creature in creatures:
        creature.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)
        if creature.just_ate is True:
            # 25% chance to spawn a new tree
            if random.random() < 0.25:
                add_tree_from_creature(trees, creature, tree_images, SCREEN_WIDTH, SCREEN_HEIGHT)
                logger.info(f"Creature ID:{creature.unique_id} spawned a new tree.")
                # print(f"Creature ID:{creature.unique_id} spawned a new tree.")
        creature.just_ate = False

    creatures.draw(display_surface)

    # Update trees and move dead ones to dead_trees list
    for tree in trees:
        tree.update(event_list,trees)
        if not tree.alive:
            trees.remove(tree)
            dead_trees.append(tree)

    # Move dead creatures to a save list
    for creature in creatures:
        if not creature.alive:
            creatures.remove(creature)
            dead_creatures.append(creature)

    # Check to see if a creature has found a tree
    for tree in trees:
        for creature in creatures:
            if check_proximity(tree, creature, 30):
                # logger.info(f"Creature at {creature.rect.topleft} is near tree at {tree.rect.topleft}")
                creature.found_tree(tree)
                
    # Check to see if a creature has found another creature
    for creature1 in creatures:
        for creature2 in creatures:
            if creature1 != creature2 and check_proximity(creature1, creature2, 30):
                creature1.found_creature(creature2, creatures, creature_images, SCREEN_WIDTH, SCREEN_HEIGHT)


    trees.draw(display_surface)

    pygame.display.update()
    if len(creatures) == 0:
        run = False
        logger.info(f"******* The simulation has ended because all creatures have died. *******")
        print(f"******* The simulation has ended because all creatures have died. *******")
    if run is False:
        # Log the final trees and creatures
        print_trees_and_creatures(trees, dead_trees, creatures, dead_creatures)
        # Log the end times of the run
        logger.info(f"Simulation started at {start_time_str}")
        print(f"Simulation started at {start_time_str}")
        end_time = time.time()
        end_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))
        logger.info(f"Simulation ended at {end_time_str}")
        print(f"Simulation ended at {end_time_str}")
        duration = end_time - start_time
        duration_str = str(datetime.timedelta(seconds=duration))
        logger.info(f"Simulation ran for {duration_str}")
        print(f"Simulation ran for {duration_str}")

pygame.quit()
