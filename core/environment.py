

class Environment:
    def __init__(self):
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def collisionListener(self, agent):
        collisions = []
        for other in self.agents:
            if other is agent or other.entity_class == agent.entity_class:
                continue
            dx = agent.x - other.x
            dy = agent.y - other.y
            dist = (dx**2 + dy**2)**0.5
            if dist < agent.radius + other.radius:
                collisions.append(other)
        # if len(collisions) != 0:
        #     print(collisions)
        return collisions
    
    def sightListener(self, agent):
        visions = []
        for other in self.agents:
            if other is agent:
                continue
            dx = agent.x - other.x
            dy = agent.y - other.y
            dist = (dx**2 + dy**2)**0.5
            if dist < agent.vision * agent.radius + other.radius:
                visions.append(other)
        # if visions:
        #     print(f"{agent} sees {[str(v) for v in visions]}")
        return visions
