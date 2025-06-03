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
        # See which prey are in vision
        visible_prey = [
            agent for agent in self.visionDetector()
            if agent.entity_class == "prey" and agent.alive
        ]

        if visible_prey:
            # --- CHASE MODE ---
            # Find the closest prey
            target = min(
                visible_prey,
                key=lambda p: math.hypot(self.x - p.x, self.y - p.y)
            )
            dx = target.x - self.x
            dy = target.y - self.y
            distance = math.hypot(dx, dy)
            if distance > 0:
                dx /= distance
                dy /= distance
                self.move_towards_point(dx, dy)
                return
            else:
                # If on top of prey, stop moving (capture occurs in learn())
                self.vel_x = 0
                self.vel_y = 0
                return

        # If no visible prey → WANDER MODE
        epsilon = 5
        tx, ty = self.random_target
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)

        if dist < epsilon:
            self.random_target = self.random_pos()
            self.idle_until = pygame.time.get_ticks() + 2000  # idle for 2 seconds
            self.vel_x = 0
            self.vel_y = 0
            return

        if pygame.time.get_ticks() < self.idle_until:
            self.vel_x = 0
            self.vel_y = 0
            return

        dx /= dist
        dy /= dist
        self.move_towards_point(dx, dy)

    def learn(self):
        reward = 0.0
        collided = self.collisionDetector()
        if collided:
            print(f"Predator at ({self.x:.1f},{self.y:.1f}) collided with {[ (p.x,p.y) for p in collided ]}")
            for p in collided:
                if p.entity_class == "prey" and p.alive:
                    p.alive = False
                    reward += 5.0

        reward -= 0.001

        next_state = self.rl_agent.get_state(self, self.environment.prey)

        if self.last_state is not None and self.last_action is not None:
            self.rl_agent.update_q(self.last_state, self.last_action, reward, next_state)

        self.total_reward += reward

        self.last_state = next_state
