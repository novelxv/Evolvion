import pygame
import random
from typing import List

class BaseAgent:
    def __init__(self, x: float, y: float, config: dict, environment, entity_class: str, color_key: str):
        self.x = x
        self.y = y
        self.config = config
        self.environment = environment
        self.entity_class = entity_class
        self.color_key = color_key

        self.radius = 6
        self.vision = random.uniform(*config["trait_range"]["vision"])
        self.speed = random.uniform(*config["trait_range"]["speed"])

        self.alive = True
        self.total_reward = 0.0
        self.fitness = 0.0

        self.vel_x = 0.0
        self.vel_y = 0.0

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        w, h = self.config["world_size"]
        if self.x < self.radius:
            self.x = self.radius
        elif self.x > w - self.radius:
            self.x = w - self.radius

        if self.y < self.radius:
            self.y = self.radius
        elif self.y > h - self.radius:
            self.y = h - self.radius

        self.collisionDetector()
        self.visionDetector()

    def handle_input(self, keys):
        self.vel_x = 0.0
        self.vel_y = 0.0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel_y = self.speed

    def handle_movement(self):
        raise NotImplementedError("handle_movement() harus diimplementasikan di subclass")
    
    def random_pos(self):
        import random

        range_ = self.vision * self.radius
        world_width, world_height = self.config["world_size"]

        new_x = random.uniform(self.x - range_, self.x + range_ * 2)
        new_y = random.uniform(self.y - range_ * 2, self.y + range_ * 2)

        new_x = max(self.radius, min(new_x, world_width - self.radius))
        new_y = max(self.radius, min(new_y, world_height - self.radius))

        return new_x, new_y

    def move_towards_point(self, dx: float, dy: float):
        self.vel_x = dx * self.speed
        self.vel_y = dy * self.speed

    def collisionDetector(self) -> List["BaseAgent"]:
        return self.environment.collisionListener(self)

    def visionDetector(self) -> List["BaseAgent"]:
        return self.environment.sightListener(self)

    def draw(self, surface):
        vision_radius_px = int(self.vision * self.radius)
        temp_surf = pygame.Surface((vision_radius_px * 2, vision_radius_px * 2), pygame.SRCALPHA)

        semi_transparent = (*self.config[self.color_key], 50)  # (R, G, B, alpha)
        pygame.draw.circle(temp_surf, semi_transparent, (vision_radius_px, vision_radius_px), vision_radius_px)

        surface.blit(temp_surf, (int(self.x - vision_radius_px), int(self.y - vision_radius_px)))

        pygame.draw.circle(surface, self.config[self.color_key], (int(self.x), int(self.y)), self.radius)
