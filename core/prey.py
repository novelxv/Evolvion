import math, pygame
import random
from core.agent_base import BaseAgent

class Prey(BaseAgent):
    def __init__(self, x: float, y: float, config: dict, environment):
        super().__init__(x, y, config, environment, entity_class="prey", color_key="blue")
        self.last_random_time = pygame.time.get_ticks()
        self.random_target = (x, y)
        self.idle_until = 0
        self.fitness = 0.0

    def update(self):
        if self.alive:
            self.fitness += 1.0
        super().update()

    def handle_movement(self):
        visible_predators = [
            agent for agent in self.visionDetector()
            if agent.entity_class == "predator" and agent.alive
        ]
        now = pygame.time.get_ticks()
        epsilon = 5

        if visible_predators:
            # --- ESCAPE MODE ---
            # Run directly away from the closest predator
            closest_pred = min(
                visible_predators,
                key=lambda p: math.hypot(self.x - p.x, self.y - p.y)
            )
            dx = self.x - closest_pred.x
            dy = self.y - closest_pred.y
            distance = math.hypot(dx, dy)
            if distance > 0:
                dx /= distance
                dy /= distance
                self.move_towards_point(dx, dy)
            else:
                # If predator lands on top, freeze until update() handles death
                self.vel_x = 0
                self.vel_y = 0
            return

        # --- WANDER MODE ---
        tx, ty = self.random_target
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)

        if dist < epsilon:
            # Arrived: pick a new random spot and idle briefly
            self.random_target = self.random_pos()
            self.idle_until = now + 2000  # idle 2 seconds
            self.vel_x = 0
            self.vel_y = 0
            return

        if pygame.time.get_ticks() < self.idle_until:
            # still idling
            self.vel_x = 0
            self.vel_y = 0
            return

        # move smoothly toward the random_target
        dx /= dist
        dy /= dist
        self.move_towards_point(dx, dy)

    def reproduce(self):
        child = Prey(self.x, self.y, self.config, self.environment)
        child.traits = self.traits.copy()
        return child
