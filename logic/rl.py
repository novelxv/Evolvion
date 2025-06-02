import random
import json

class QLearningAgent:
    def __init__(self, actions: list, learning_rate: float, discount_factor: float, epsilon: float, config: dict):
        self.actions = actions
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.q_table = {}
        self.config = config

        w, h = config["world_size"]
        self.cell_size = 50
        self.grid_cols = w // self.cell_size
        self.grid_rows = h // self.cell_size

    def get_state(self, predator, prey_list):
        col = int(predator.x // self.cell_size)
        row = int(predator.y // self.cell_size)
        col = max(0, min(col, self.grid_cols - 1))
        row = max(0, min(row, self.grid_rows - 1))

        nearest_prey = None
        min_dist = float("inf")
        for p in prey_list:
            if not p.alive:
                continue
            dx = p.x - predator.x
            dy = p.y - predator.y
            dist = (dx*dx + dy*dy) ** 0.5
            if dist < min_dist:
                min_dist = dist
                nearest_prey = p

        if nearest_prey is None:
            direction = "none"
        else:
            dx = nearest_prey.x - predator.x
            dy = nearest_prey.y - predator.y

            if abs(dx) > abs(dy):
                direction = "right" if dx > 0 else "left"
            else:
                direction = "down" if dy > 0 else "up"

        state = f"C{col}_{row}|DIR_{direction}"
        return state

    def choose_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}

        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            action_values = self.q_table[state]
            max_q = max(action_values.values())
            best_actions = [a for a, v in action_values.items() if v == max_q]
            return random.choice(best_actions)

    def update_q(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0.0 for a in self.actions}

        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state].values())
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def save_to_file(self, path):
        with open(path, 'w') as f:
            json.dump(self.q_table, f)

    def load_from_file(self, path):
        with open(path, 'r') as f:
            self.q_table = json.load(f)
