import pygame
import random
from tree import Tree
from creature import Creature

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simulation5')

tree_surf = pygame.image.load('images/pine_tree.png').convert_alpha()
creature_surf = pygame.image.load('images/creature.png').convert_alpha()

def add_tree(trees, image, screen_width, screen_height):
    new_tree = Tree(
        image=image,
        initial_scale=0.1,
        position=(random.randint(0, screen_width), random.randint(0, screen_height)),
        growth_rate=random.uniform(0.05, 0.15),
        growth_interval=random.randint(4000, 8000)
    )
    trees.append(new_tree)

# Create initial trees
trees = []
for _ in range(30):
    add_tree(trees, tree_surf, SCREEN_WIDTH, SCREEN_HEIGHT)

def add_creature(creatures, image, screen_width, screen_height):
    new_creature = Creature(
        image=image,
        position=(random.randint(0, screen_width), random.randint(0, screen_height)),
        speed=random.uniform(3, 6)  # Adjust speed range as needed
    )
    creatures.append(new_creature)

# Create initial creatures
creatures = []
for _ in range(10):  # Example: Adding 10 initial creatures
    add_creature(creatures, creature_surf, SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()

run = True
while run:
    dt = clock.tick(60) / 1000.0  # Calculate delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        for tree in trees:
            if tree.alive:
                if event.type == tree.timer_event:
                    tree.grow()

    keys = pygame.key.get_pressed()
    just_pressed = pygame.key.get_just_pressed()

    if just_pressed[pygame.K_SPACE]:
        add_tree(trees, tree_surf, SCREEN_WIDTH, SCREEN_HEIGHT)

    if just_pressed[pygame.K_x]:
        run = False

    display_surface.fill("lightgreen")

    # Update and draw creatures
    for creature in creatures:
        creature.move(dt, SCREEN_WIDTH, SCREEN_HEIGHT)
        creature.draw(display_surface)

    # Draw trees
    for tree in trees:
        if tree.alive:
            tree.draw(display_surface)

    pygame.display.update()

pygame.quit()
