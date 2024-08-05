import pygame
import random
import math


from tree2 import Tree2
from creature2 import Creature2

NUM_CREATURES = 20
NUM_TREES = 60

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simulation5')

tree_surf = pygame.image.load('images/pine_tree.png').convert_alpha()
creature_surf = pygame.image.load('images/creature.png').convert_alpha()

# Add trees from nothing, these trees have no genetic inheritance from parents
def add_tree(trees, image, screen_width, screen_height):
    new_tree = Tree2(
        image=image,
        initial_scale=0.1,
        parent=0,
        carrier=0,
        position=(random.randint(0, screen_width), random.randint(0, screen_height)),
        growth_rate=random.uniform(0.05, 0.12),
        growth_interval=random.randint(4000, 8000)
    )
    trees.add(new_tree)

# Add creatures from nothing, these creatures have no genetic inheritance from parents
def add_creature(creatures, image, screen_width, screen_height):
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
        speed=random.uniform(3, 6),
        stomach_size = random.randint(2, 5),
        starvation_time_limit = random.randint(15000, 25000),  # Time limit before starvation in milliseconds, can represent fat/energy stores
        food_reduction_interval = random.randint(7500, 12500)  # Time interval to reduce food in stomach by 1 in milliseconds
    )
    creatures.add(new_creature)
    print("\nNew creature spawned from nothing:")
    print(new_creature)

def print_trees_and_creatures(trees, dead_trees, creatures):
    print("Alive Trees:")
    for tree in trees:
        print(tree)
    print("\nDead Trees:")
    for tree in dead_trees:
        print(tree)
    print("\nCreatures:")
    for creature in creatures:
        print(creature)
    print("\nDead Creatures:")
    for creature in dead_creatures:
        print(creature)
    print("-" * 40)

def print_only_creatures(creatures):
    print("\nCreatures:")
    for creature in creatures:
        print(creature)
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
    add_tree(trees, tree_surf, SCREEN_WIDTH, SCREEN_HEIGHT)

for _ in range(NUM_CREATURES):
    add_creature(creatures, creature_surf, SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()

run = True
while run:
    dt = clock.tick(60) / 1000.0
    keys = pygame.key.get_just_pressed()

    if keys[pygame.K_x]:
        run = False
    if keys[pygame.K_t]:
        add_tree(trees, tree_surf, SCREEN_WIDTH, SCREEN_HEIGHT)
    if keys[pygame.K_c]:
        add_creature(creatures, creature_surf, SCREEN_WIDTH, SCREEN_HEIGHT)
    if keys[pygame.K_p]:
        print_trees_and_creatures(trees, dead_trees, creatures)
    if keys[pygame.K_o]:
        print_only_creatures(creatures)

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False


    display_surface.fill("lightgreen")

    # Update and draw creatures
    creatures.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)
    creatures.draw(display_surface)

    # Update trees and move dead ones to dead_trees list
    for tree in trees:
        tree.update(event_list)
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
                # print(f"Creature at {creature.rect.topleft} is near tree at {tree.rect.topleft}")
                creature.found_tree(tree)
                
    # Check to see if a creature has found another creature
    for creature1 in creatures:
        for creature2 in creatures:
            if creature1 != creature2 and check_proximity(creature1, creature2, 30):
                creature1.found_creature(creature2, creatures, creature_surf, SCREEN_WIDTH, SCREEN_HEIGHT)


    trees.draw(display_surface)

    pygame.display.update()

pygame.quit()
