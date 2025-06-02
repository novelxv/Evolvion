import random
from typing import List
from core.agent_base import BaseAgent

class Environment:
    def __init__(self, config: dict):
        self.config = config
        self.agents: List[BaseAgent] = []
        self.prey: List[BaseAgent] = []
        self.predators: List[BaseAgent] = []

    def add_agent(self, agent: BaseAgent):
        self.agents.append(agent)
        if agent.entity_class == "prey":
            self.prey.append(agent)
        elif agent.entity_class == "predator":
            self.predators.append(agent)

    def reset_generation(self):
        for p in self.prey:
            p.alive = True

    def collisionListener(self, agent: BaseAgent) -> List[BaseAgent]:
        collisions = []
        for other in self.agents:
            if other is agent or other.entity_class == agent.entity_class:
                continue
            dx = agent.x - other.x
            dy = agent.y - other.y
            dist = (dx*dx + dy*dy) ** 0.5
            if dist < agent.radius + other.radius:
                collisions.append(other)
        return collisions

    def sightListener(self, agent: BaseAgent) -> List[BaseAgent]:
        visible = []
        for other in self.agents:
            if other is agent:
                continue
            dx = agent.x - other.x
            dy = agent.y - other.y
            dist = (dx*dx + dy*dy) ** 0.5
            if dist < agent.vision * agent.radius + other.radius:
                visible.append(other)
        return visible

    def remove_dead_agents(self):
        alive_agents = [a for a in self.agents if a.alive]
        self.agents = alive_agents
        self.prey = [p for p in self.prey if p.alive]
        self.predators = [pr for pr in self.predators if pr.alive]
