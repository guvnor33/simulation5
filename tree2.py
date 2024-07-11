import pygame
import random

class Tree2(pygame.sprite.Sprite):
    MAX_GROWTHS = 10

    def __init__(self, image, initial_scale, position, growth_rate, growth_interval):
        super().__init__()
        self.original_image = image
        self.scale_factor = initial_scale
        self.image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * self.scale_factor),
             int(self.original_image.get_height() * self.scale_factor))
        )
        self.rect = self.image.get_rect(midbottom=position)
        self.growth_rate = growth_rate
        self.growth_count = 0
        self.max_growth_count = 8
        self.growth_interval = growth_interval
        self.alive = True
        self.times_grown = 0
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, self.growth_interval)

    def grow(self):
        self.times_grown += 1

        if self.times_grown >= self.MAX_GROWTHS:
            self.alive = False
        if self.growth_count < self.max_growth_count:
            self.growth_count += 1
            self.scale_factor += self.growth_rate
            self.image = pygame.transform.scale(
                self.original_image,
                (int(self.original_image.get_width() * self.scale_factor),
                 int(self.original_image.get_height() * self.scale_factor))
            )
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            pygame.time.set_timer(self.timer_event, self.growth_interval)

    def update(self, event_list):
        for event in event_list:
            if event.type == self.timer_event and self.alive:
                self.grow()
