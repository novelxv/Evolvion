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
        visible = [agent for agent in self.visionDetector() if agent.entity_class == "predator" and agent.alive]
        now = pygame.time.get_ticks()
        epsilon = 5

        # if now < self.idle_until and not visible:
        #     return

        if not visible:
            target_x, target_y = self.random_target

            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.hypot(dx, dy)


            if distance < epsilon:
                self.x, self.y = target_x, target_y
                self.random_target = self.random_pos()
                self.idle_until = now + 3000
                return

            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.hypot(dx, dy)

            if distance == 0:
                return

            dx /= distance
            dy /= distance

            self.move_towards_point(dx, dy)
            return

        target = visible[-1]
        min_dist = math.hypot(self.x - target.x, self.y - target.y)
        for p in visible[1:]:
            d = math.hypot(self.x - p.x, self.y - p.y)
            if d < min_dist:
                min_dist = d
                target = p

        dx = self.x - target.x
        dy = self.y - target.y
        if min_dist > 0:
            dx /= min_dist
            dy /= min_dist
        self.move_towards_point(dx, dy)

    def reproduce(self):
        child = Prey(self.x, self.y, self.config, self.environment)
        child.traits = self.traits.copy()
        return child
