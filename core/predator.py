import pygame
from agent_base import *

class Predator(BaseAgent):
    def __init__(self, x, y, config, environment):
        super().__init__(x, y, config, environment)
    
    def onCollide(self, entity_tag):
        super().onCollide(entity_tag)

    def onSight(self, entity_class):
        super().onSight(entity_class)
        # TODO: targetting algorithm