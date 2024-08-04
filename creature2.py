import pygame
import random

class Creature2(pygame.sprite.Sprite):
    def __init__(self, image, initial_scale, position, speed):
        super().__init__()
        self.image = image
        self.position = pygame.math.Vector2(position)
        self.scale_factor = initial_scale
        self.image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * self.scale_factor),
             int(self.image.get_height() * self.scale_factor))
        )
        self.rect = self.image.get_rect(midbottom=self.position)
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.next_direction_change_time = pygame.time.get_ticks() + random.randint(3000, 5000)
        # *** Genetic Traits ***
        # is hungrt, stomach size, is full,
        # days without eating, range of vision, range of smell,
        # speed, size, allowed foods (plants or other creatures, seeds),
        # toughness (akin to 'suceptibility to being eaten')
        self.speed = speed
        self.stomach_size = random.randint(2, 5)
        self.food_in_stomach = random.randint(1, self.stomach_size)
        self.is_hungry = self.determine_hunger(self.food_in_stomach, self.stomach_size)
        self.is_full = self.determine_full(self.food_in_stomach, self.stomach_size)

    # If stomach is over 3/5ths full creature is not hungry
    def determine_hunger(self, food, stomach):
        if (food/stomach) < (3/5):
            return True
        else:
            return False
        
    # Creature is full if stomach is completely full
    def determine_full(self, food, stomach):
        if (food >= stomach):
            return True
        else:
            return False
    # eat and then update is_hungry
    def eat(self):
        if (self.food_in_stomach < self.stomach_size):
            self.food_in_stomach += 1
            print(f"creature eat")
            print(str(self))
            self.is_hungry = self.determine_hunger(self.food_in_stomach, self.stomach_size)
            self.is_full = self.determine_full(self.food_in_stomach, self.stomach_size)

    def move(self, dt, screen_width, screen_height):
        current_time = pygame.time.get_ticks()

        if current_time >= self.next_direction_change_time:
            self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            self.next_direction_change_time = current_time + random.randint(3000, 4000)

        movement = self.direction * self.speed * dt
        self.position += movement

        self.position.x = max(0, min(self.position.x, screen_width - self.rect.width))
        self.position.y = max(0, min(self.position.y, screen_height - self.rect.height))

        self.rect.midbottom = self.position

    def update(self, dt, screen_width, screen_height):
        self.move(dt, screen_width, screen_height)

    def __str__(self):
        return (f"Creature(Position: {self.position}, Speed: {self.speed:.2f}, "
                f"Stomach Size: {self.stomach_size}, Food in Stomach: {self.food_in_stomach}, "
                f"Is Hungry: {self.is_hungry}, Is Full: {self.is_full})")
