import pygame
from core.agent_base import *

class Predator(BaseAgent):
    def __init__(self, x, y, config, environment):
        super().__init__(x, y, config, environment, "predator", "red")
    
    def update(self):
        return super().update()
    
    def handle_movement(self):
        import math
        vision = self.visionDetector()
        if (len(vision) == 0):
            return
        
        target = vision[-1] # the first agent to be spotted is locked as the target, hence the last element

        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance

        self.move_towards_point(dx, dy)