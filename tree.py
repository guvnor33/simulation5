import pygame
import random

class Tree:
    MAX_GROWTHS = 10
    tree_timer_counter = 0  # for the timer

    def __init__(self, image, initial_scale, position, growth_rate, growth_interval):

        self.original_image = image
        self.scale_factor = initial_scale
        self.position = position
        self.growth_rate = growth_rate
        self.growth_count = 0
        self.max_growth_count = 8
        self.growth_interval = growth_interval
        self.tree_age = 0
        self.alive = True
        self.times_grown = 0

        self.scaled_image = pygame.transform.scale(
            self.original_image, 
            (int(self.original_image.get_width() * self.scale_factor), 
             int(self.original_image.get_height() * self.scale_factor))
        )
        self.rect = self.scaled_image.get_rect()
        self.rect.midbottom = self.position
        
        self.timer_event = pygame.USEREVENT + Tree.tree_timer_counter
        pygame.time.set_timer(self.timer_event, self.growth_interval)
             
        Tree.tree_timer_counter += 1

    def grow(self):
        self.times_grown += 1

        if self.times_grown >= self.MAX_GROWTHS:  # too many growths means the tree will die
            self.alive = False
        if self.growth_count < self.max_growth_count:
            self.growth_count += 1
            self.scale_factor += self.growth_rate
            self.scaled_image = pygame.transform.scale(
                self.original_image, 
                (int(self.original_image.get_width() * self.scale_factor), 
                 int(self.original_image.get_height() * self.scale_factor))
            )
            self.rect = self.scaled_image.get_rect()
            self.rect.midbottom = self.position
            pygame.time.set_timer(self.timer_event, self.growth_interval)

    def draw(self, surface):
        surface.blit(self.scaled_image, self.rect.topleft)
