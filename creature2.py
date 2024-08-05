import pygame
import random
import logging

logger = logging.getLogger()

# These variables are genetic traits that must be passed in from the parents:
#   speed,
#   stomach_size,
#   starvation_time_limit,
#   food_reduction_interval

# ***** Notes ******
#
# Presently, a creature is allow to feast when near a tree..up to a full stomach
#

class Creature2(pygame.sprite.Sprite):
    MATING_TIMEOUT = 25000 # Minimum interval between matings
    unique_id_counter = 100  # Class variable to keep track of unique IDs

    def __init__(self, image, initial_scale, parent1, parent2, position, speed, stomach_size, starvation_time_limit, food_reduction_interval):
        super().__init__()
        self.alive = True
        self.born_time = pygame.time.get_ticks()
        self.last_mating_time = None
        self.image = image
        self.unique_id = Creature2.unique_id_counter  # Assign unique ID from the counter
        Creature2.unique_id_counter += 1  # Increment the counter for the next creature
        self.parent1 = parent1
        self.parent2 = parent2
        self.trees_eaten_from = []
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
        self.stomach_size = stomach_size
        self.starvation_time_limit = starvation_time_limit  # Time limit before starvation in milliseconds, can represent fat/energy stores
        self.food_reduction_interval = food_reduction_interval  # Time interval to reduce food in stomach by 1 in milliseconds

        self.food_in_stomach = random.randint(1, self.stomach_size)
        self.is_hungry = self.determine_hunger(self.food_in_stomach, self.stomach_size)
        self.is_full = self.determine_full(self.food_in_stomach, self.stomach_size)
        self.last_eat_time = None  # Timer starts only when food_in_stomach == 0
        self.last_food_reduction_time = pygame.time.get_ticks()  # Initialize the last food reduction time




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
    def eat(self, tree):
        if (self.food_in_stomach < self.stomach_size):
            self.food_in_stomach += 1
            self.is_hungry = self.determine_hunger(self.food_in_stomach, self.stomach_size)
            self.is_full = self.determine_full(self.food_in_stomach, self.stomach_size)
            self.last_eat_time = None  # Reset starvation timer when the creature eats
            self.trees_eaten_from.append(tree.unique_id) # Save a list of trees creature has eaten from
            logger.info(f"Creature ID:{self.unique_id} has eaten.")
            logger.info(str(self))

    def check_starvation(self):
        current_time = pygame.time.get_ticks()
        if self.food_in_stomach == 0:
            if self.last_eat_time is None:
                self.last_eat_time = current_time  # Start the timer when food_in_stomach reaches 0
            elif current_time - self.last_eat_time > self.starvation_time_limit:
                self.alive = False
                logger.info(f"Creature ID:{self.unique_id} has starved.")
        else:
            self.last_eat_time = None  # Reset the timer if food_in_stomach is not 0

    def reduce_food_in_stomach(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_food_reduction_time >= self.food_reduction_interval:
            if self.food_in_stomach > 0:
                self.food_in_stomach -= 1
                self.is_hungry = self.determine_hunger(self.food_in_stomach, self.stomach_size)
                self.is_full = self.determine_full(self.food_in_stomach, self.stomach_size)
                logger.info(f"Creature ID:{self.unique_id} lost 1 food. Current food: {self.food_in_stomach}")
                if self.food_in_stomach == 0:
                    self.last_eat_time = current_time  # Start starvation timer
            self.last_food_reduction_time = current_time  # Reset the food reduction timer

    def found_tree(self, tree):
        if self.is_hungry:
            logger.info(f"Creature ID:{self.unique_id} found a tree and is hungry.")
            self.eat(tree)
            tree.change_color((21, 155, 21)) # to indicate visually a proximity event

    def found_creature(self, found_creature, creatures, creature_surf, screen_width, screen_height):
        current_time = pygame.time.get_ticks()

        # Reset mating times of creatures if it has been long enough
        if self.last_mating_time is not None:
            if (self.last_mating_time - current_time) > self.MATING_TIMEOUT:
                self.last_mating_time = None
        if found_creature.last_mating_time is not None:
            if (found_creature.last_mating_time - current_time) > found_creature.MATING_TIMEOUT:
                found_creature.last_mating_time = None

        if ((self.last_mating_time is None) and (found_creature.last_mating_time is None)):
            self.last_mating_time = current_time 
            found_creature.last_mating_time = current_time 
            logger.info(f"Creature {self.unique_id} is near creature {found_creature.unique_id} and will mate.")
            new_creature = self.mate(self, found_creature, creature_surf, screen_width, screen_height)
            creatures.add(new_creature) # Add creature to the array of creatures
            logger.info(f"New creature (ID:{new_creature.unique_id}) born from mating:")
            logger.info(new_creature)
            logger.info(self)
            logger.info(found_creature)


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
        self.check_starvation()
        self.reduce_food_in_stomach()

    def __str__(self):
        return (f"Creature ID:{self.unique_id}, Parents: {self.parent1:03},{self.parent2:03} (Position: {self.position}, Speed: {self.speed:.2f}, "
                f"Stomach Size: {self.stomach_size}, Food in Stomach: {self.food_in_stomach}, "
                f"Is Hungry: {self.is_hungry}, Is Full: {self.is_full})"
                f"Trees eaten from: {self.trees_eaten_from})")
    
    @staticmethod
    def mate(parent1, parent2, image, screen_width, screen_height):
        # Fix this to later spawn near parent
        new_position = ( 
            random.randint(0, screen_width),
            random.randint(0, screen_height)
        )
        new_speed = parent1.speed
        new_stomach_size = parent2.stomach_size
        new_starvation_time_limit = parent1.starvation_time_limit
        new_food_reduction_interval = parent2.food_reduction_interval
        # These variables are genetic traits that must be passed in from the parents:
        #   speed,
        #   stomach_size,
        #   starvation_time_limit,
        #   food_reduction_interval
        new_creature = Creature2(
            image=image,
            initial_scale=0.5,
            parent1=parent1.unique_id,
            parent2=parent2.unique_id,
            position=new_position,
            speed=new_speed,
            stomach_size=new_stomach_size,
            starvation_time_limit=new_starvation_time_limit,
            food_reduction_interval=new_food_reduction_interval
        )
        return new_creature
