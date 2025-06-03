import math
import random
from core.agent_base import BaseAgent

class Prey(BaseAgent):
    def __init__(self, x: float, y: float, config: dict, environment):
        super().__init__(x, y, config, environment, entity_class="prey", color_key="blue")
        self.fitness = 0.0

    def update(self):
        if self.alive:
            self.fitness += 1.0
        super().update()

    def handle_movement(self):
        visible = [agent for agent in self.visionDetector() if agent.entity_class == "predator" and agent.alive]
        if not visible:
            self.vel_x = 0
            self.vel_y = 0
            return

        target = visible[0]
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
