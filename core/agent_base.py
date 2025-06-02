import pygame
import random
from core.environment import Environment
import sys

class BaseAgent:
    def __init__(self, x, y, config, environment: Environment, entity_class):
        self.x = x
        self.y = y
        self.radius = 25
        self.config = config
        self.environment = environment
        self.entity_class = entity_class
        self.vision = random.uniform(*config["trait_range"]["vision"])
        self.speed = 5 # set to 0 by default, 5 for debugging
        self.vel_x = 0
        self.vel_y = 0
    
    def update(self):
        # Update position based on velocity
        self.x += self.vel_x
        self.y += self.vel_y

        # Keep agent (circle) on screen
        if self.x < self.radius:
            self.x = self.radius
        elif self.x > self.config["world_size"][0] - self.radius:
            self.x = self.config["world_size"][0] - self.radius

        if self.y < self.radius:
            self.y = self.radius
        elif self.y > self.config["world_size"][1] - self.radius:
            self.y = self.config["world_size"][1] - self.radius

        self.collisionDetector()
        self.visionDetector()

    def handle_input(self, keys):
        # Reset velocity
        self.vel_x = 0
        self.vel_y = 0
        
        # Still using key for movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel_y = self.speed

    def handle_movement(self):
        vision = self.visionDetector()
        if (len(vision) == 0):
            return
        
        target = vision[0]
        self.move_towards_point(target.x, target.y)

    def move_towards_point(self, target_x, target_y):
        import math

        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance

            self.x += dx * self.speed
            self.y += dy * self.speed

    def collisionDetector(self):
        # returns an array of collided agents, other than the same tag
        return self.environment.collisionListener(self)

    def visionDetector(self):
        # returns an array of agents in vision radius
        return self.environment.sightListener(self)
    
    def draw(self, surface):
        vision_radius = int(self.vision)
        temp_surf = pygame.Surface((vision_radius * 2, vision_radius * 2), pygame.SRCALPHA)

        # Draw the vision circle on the temp surface
        pygame.draw.circle(temp_surf, self.config["blue"], (int(self.x), int(self.y)), vision_radius * self.radius)

        # Blit temp surface onto main screen
        surface.blit(temp_surf, (int(self.x - vision_radius), int(self.y - vision_radius)))

        # Draw the actual agent
        pygame.draw.circle(surface, self.config["blue"], (int(self.x), int(self.y)), self.radius)
