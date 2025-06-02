import pygame
from core.agent_base import *

class Prey(BaseAgent):
    def __init__(self, x, y, config, environment):
        super().__init__(x, y, config, environment, "prey", "blue")
    
    def update(self):
        return super().update()
    
    def handle_movement(self):
        import math
        vision = self.visionDetector()
        print(vision)
        if (len(vision) == 0):
            return
        
        target = vision[-1] # the first agent to be spotted is locked as the target, hence the last element

        dx = self.x - target.x
        dy = self.y - target.y

        magnitude = math.hypot(-dx, -dy)
        if magnitude == 0:
            self.move_towards_point(0, 0)
            return 
        dx /= magnitude
        dy /= magnitude

        print(dx, dy)

        self.move_towards_point(dx, dy)