import pygame
import random

class Creature2(pygame.sprite.Sprite):
    def __init__(self, image, position, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=position)
        self.position = pygame.math.Vector2(position)
        self.speed = speed
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.direction.normalize_ip()
        self.next_direction_change_time = pygame.time.get_ticks() + random.randint(3000, 5000)

    def update(self, dt, screen_width, screen_height):
        current_time = pygame.time.get_ticks()

        if current_time >= self.next_direction_change_time:
            self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            self.direction.normalize_ip()
            self.next_direction_change_time = current_time + random.randint(3000, 4000)

        movement = self.direction * self.speed * dt
        self.position += movement

        self.position.x = max(0, min(self.position.x, screen_width - self.rect.width))
        self.position.y = max(0, min(self.position.y, screen_height - self.rect.height))

        self.rect.midbottom = self.position
