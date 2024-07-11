import pygame
import random

class Creature:
    def __init__(self, image, position, speed):
        self.image = image
        self.position = pygame.math.Vector2(position)  # Convert position to Vector2
        self.speed = speed
        self.rect = self.image.get_rect(midbottom=self.position)
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.direction.normalize_ip()  # Normalize to maintain constant speed in all directions
        self.next_direction_change_time = pygame.time.get_ticks() + random.randint(3000, 5000)  # Initial direction change time

    def move(self, dt, screen_width, screen_height):
        current_time = pygame.time.get_ticks()

        # Check if it's time to change direction
        if current_time >= self.next_direction_change_time:
            self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            self.direction.normalize_ip()  # Normalize to maintain constant speed in all directions
            self.next_direction_change_time = current_time + random.randint(2500, 4000)  # Set next direction change time

        # Calculate movement based on current direction and speed
        movement = self.direction * self.speed * dt  # Scale by delta time

        # Update position
        self.position += movement

        # Keep the creature within the screen boundaries
        self.position.x = max(0, min(self.position.x, screen_width - self.rect.width))
        self.position.y = max(0, min(self.position.y, screen_height - self.rect.height))

        # Update rect based on updated position
        self.rect.midbottom = self.position

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
