import pygame
import random
import copy
import logging

MAX_TREES = 300

logger = logging.getLogger()

# These variables are genetic traits that must be passed in from the parents:
#   
#   add genetic variables
#   possibly growth_rate and growth_interval
#   

class Tree2(pygame.sprite.Sprite):
    MAX_GROWTHS = 8
    unique_id_counter = 600  # Class variable to keep track of unique IDs

    def __init__(self, images, initial_scale, parent, carrier, position, growth_rate, growth_interval):
        super().__init__()
        self.images = images
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.original_image = self.image.copy()
        self.scale_factor = initial_scale
        self.image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * self.scale_factor),
             int(self.image.get_height() * self.scale_factor))
        )
        self.scale_factor = initial_scale
        self.image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * self.scale_factor),
             int(self.original_image.get_height() * self.scale_factor))
        )
        self.unique_id = Tree2.unique_id_counter  # Assign unique ID from the counter
        Tree2.unique_id_counter += 1  # Increment the counter for the next creature
        self.parent = parent # Parent is the parent tree (where the seed came from)
        self.carrier = carrier # Carrier is defined when a creature deposits a previously eaten seed back into the environement
        self.position = pygame.math.Vector2(position)
        self.rect = self.image.get_rect(midbottom=position)
        self.growth_rate = growth_rate
        self.growth_count = 0
        self.max_growth_count = self.MAX_GROWTHS
        self.growth_interval = growth_interval
        self.alive = True
        self.times_grown = 0
        self.timer_event = pygame.USEREVENT + random.randint(1, 1000)
        pygame.time.set_timer(self.timer_event, self.growth_interval)
        # Set the self_spawn time for a new tree,
        # "self spawn" indicates that the new tree spawns from a seed that dropped from the tree itself
        self.next_self_spawn_time = pygame.time.get_ticks() + random.randint(30000, 55000)

        self.position = pygame.math.Vector2(position)
        self.growth_rate = growth_rate
        self.growth_interval = growth_interval
        self.last_growth_time = pygame.time.get_ticks()
        self.growth_stage = 0
        


    def grow(self):
        current_time = pygame.time.get_ticks()
        self.times_grown += 1
        if self.times_grown > self.MAX_GROWTHS:
            self.alive = False  
        if current_time - self.last_growth_time >= self.growth_interval:
            self.growth_stage += 1
            if self.growth_stage < len(self.images):
                self.current_image_index = self.growth_stage
                self.image = self.images[self.current_image_index]
                self.original_image = self.image.copy()
                self.scale_factor += self.growth_rate
                self.image = pygame.transform.scale(
                    self.image,
                    (int(self.image.get_width() * self.scale_factor),
                     int(self.image.get_height() * self.scale_factor))
                )
                self.rect = self.image.get_rect(midbottom=self.position)
            self.last_growth_time = current_time

    def grow_old(self):
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

    def spawn_new_tree(self,trees):
        # This code assumes a tree spawned from a tree-dropped seed
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_self_spawn_time:
            # Here, the tree spawns a new tree at a random nearby position
            #new_tree_position = (self.position.x + random.randint(-50, 50), self.position.y + random.randint(-50, 50))
            new_tree_position = (
                self.position.x + random.randint(-50, 50), 
                self.position.y + random.randint(-50, 50)
            )
            new_tree = Tree2(
                images=self.images,
                initial_scale=0.5,
                parent=self.unique_id,
                carrier=0,
                position=new_tree_position,
                growth_rate=random.uniform(0.08, 0.15),
                growth_interval=random.randint(4000, 8000)
            )
            trees.add(new_tree)
            logger.debug(f"New tree spawned at {new_tree_position}")
            self.next_self_spawn_time = current_time + random.randint(30000, 55000)  # Reset spawn timer

    def update(self, event_list,trees):
        if self.alive:
            for event in event_list:
                if event.type == self.timer_event:
                    self.grow()
        if len(trees) < MAX_TREES:
            self.spawn_new_tree(trees)  

    def change_color(self, color):
        current_size = self.image.get_size()  # Get the current size of the tree image
        self.image = self.original_image.copy()  # Make a copy of the original image
        self.image.fill(color, special_flags=pygame.BLEND_RGB_MULT)  # Apply the color
        self.image = pygame.transform.scale(self.image, current_size)  # Resize to the current size

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return (f"Tree ID:{self.unique_id}, Parent:{self.parent:03}, Carrier:{self.carrier:03} Tree(Position: {self.rect.midbottom}, "
                f"Scale: {self.scale_factor:.2f}, "
                f"Growths: {self.times_grown}, "
                f"Alive: {self.alive})")
