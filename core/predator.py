import math
from core.agent_base import BaseAgent
from logic.rl import QLearningAgent

class Predator(BaseAgent):
    def __init__(self, x: float, y: float, config: dict, environment):
        super().__init__(x, y, config, environment, entity_class="predator", color_key="red")
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
        if state in self.rl_agent.q_table:
            action = self.decide_action()
            self.execute_action(action)
        else:
            visible = [ag for ag in self.visionDetector()
                       if ag.entity_class == "prey" and ag.alive]
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
            for p in collided:
                if p.entity_class == "prey" and p.alive:
                    p.alive = False
                    reward += 1.0

        reward -= 0.01

        next_state = self.rl_agent.get_state(self, self.environment.prey)

        if self.last_state is not None and self.last_action is not None:
            self.rl_agent.update_q(self.last_state, self.last_action, reward, next_state)

        self.total_reward += reward

        self.last_state = next_state
