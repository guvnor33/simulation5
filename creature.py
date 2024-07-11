import pygame
import random

class Creature:
    def __init__(self, image, position, speed):
        self.image = image
        self.position = position
        self.speed = speed
        self.rect = self.image.get_rect(midbottom=self.position)

    def move(self, screen_width, screen_height):
        direction = random.choice(['left', 'right', 'up', 'down'])
        if direction == 'left':
            self.rect.x -= self.speed
        elif direction == 'right':
            self.rect.x += self.speed
        elif direction == 'up':
            self.rect.y -= self.speed
        elif direction == 'down':
            self.rect.y += self.speed

        # Keep the creature within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
