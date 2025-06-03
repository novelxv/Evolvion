import math, pygame
from core.agent_base import BaseAgent
from logic.rl import QLearningAgent

class Predator(BaseAgent):
    def __init__(self, x: float, y: float, config: dict, environment):
        super().__init__(x, y, config, environment, entity_class="predator", color_key="red")
        self.last_random_time = pygame.time.get_ticks()
        self.random_target = (x, y)
        self.idle_until = 0
        actions = ["up", "down", "left", "right", "stay"]
        rl_cfg = config["rl"]
        self.rl_agent = QLearningAgent(actions,
                                       rl_cfg["learning_rate"],
                                       rl_cfg["discount_factor"],
                                       rl_cfg["epsilon"],
                                       config)
        self.total_reward = 0.0
        self.last_state = None
        self.last_action = None
        self.speed = config.get("predator_speed", 4.0)
        self.vision = config.get("predator_vision", 20.0)

    def decide_action(self):
        state = self.rl_agent.get_state(self, self.environment.prey)
        action = self.rl_agent.choose_action(state)
        self.last_state = state
        self.last_action = action
        return action

    def execute_action(self, action):
        if action == "up":
            dx, dy = 0, -1
        elif action == "down":
            dx, dy = 0, 1
        elif action == "left":
            dx, dy = -1, 0
        elif action == "right":
            dx, dy = 1, 0
        else:
            dx, dy = 0, 0
        self.move_towards_point(dx, dy)

    def handle_movement(self):
        state = self.rl_agent.get_state(self, self.environment.prey)
        visible = [ag for ag in self.visionDetector()
                       if ag.entity_class == "prey" and ag.alive]
        epsilon = 5
        now = pygame.time.get_ticks()

        if state in self.rl_agent.q_table:
            action = self.decide_action()
            self.execute_action(action)
            return

        if not visible:
            target_x, target_y = self.random_target

            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.hypot(dx, dy)

            if distance < epsilon:
                self.x = target_x
                self.y = target_y
                self.random_target = self.random_pos()
                self.idle_until = now + 3000

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
        dx = target.x - self.x
        dy = target.y - self.y
        if min_dist > 0:
            dx /= min_dist
            dy /= min_dist
        self.move_towards_point(dx, dy)

    def learn(self):
        reward = 0.0
        collided = self.collisionDetector()
        if collided:
            print(f"Predator at ({self.x:.1f},{self.y:.1f}) collided with {[ (p.x,p.y) for p in collided ]}")
            for p in collided:
                if p.entity_class == "prey" and p.alive:
                    p.alive = False
                    reward += 2.0

        reward -= 0.001

        next_state = self.rl_agent.get_state(self, self.environment.prey)

        if self.last_state is not None and self.last_action is not None:
            self.rl_agent.update_q(self.last_state, self.last_action, reward, next_state)

        self.total_reward += reward

        self.last_state = next_state
