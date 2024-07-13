import pygame
import random
from tree2 import Tree2
from creature2 import Creature2

NUM_CREATURES = 50
NUM_TREES = 40

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simulation5')

tree_surf = pygame.image.load('images/pine_tree.png').convert_alpha()
creature_surf = pygame.image.load('images/creature.png').convert_alpha()

def add_tree(trees, image, screen_width, screen_height):
    new_tree = Tree2(
        image=image,
        initial_scale=0.1,
        position=(random.randint(0, screen_width), random.randint(0, screen_height)),
        growth_rate=random.uniform(0.05, 0.15),
        growth_interval=random.randint(4000, 8000)
    )
    trees.add(new_tree)

def add_creature(creatures, image, screen_width, screen_height):
    new_creature = Creature2(
        image=image,
        initial_scale=0.5,
        position=(random.randint(0, screen_width), random.randint(0, screen_height)),
        speed=random.uniform(3, 6)
    )
    creatures.add(new_creature)

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
    print("-" * 40)

# Create sprite groups
trees = pygame.sprite.Group()
creatures = pygame.sprite.Group()
dead_trees = []

# Add initial trees and creatures
for _ in range(NUM_TREES):
    add_tree(trees, tree_surf, SCREEN_WIDTH, SCREEN_HEIGHT)

for _ in range(NUM_CREATURES):
    add_creature(creatures, creature_surf, SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()

run = True
while run:
    dt = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed()

    if keys[pygame.K_x]:
        run = False

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
        if keys[pygame.K_SPACE]:
            add_tree(trees, tree_surf, SCREEN_WIDTH, SCREEN_HEIGHT)
        if keys[pygame.K_p]:
            print_trees_and_creatures(trees, dead_trees, creatures)

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

    trees.draw(display_surface)

    pygame.display.update()

pygame.quit()
