import random
import json

class QLearningAgent:
    def __init__(self, actions: list, learning_rate: float, discount_factor: float, epsilon: float):
        self.actions = actions
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.q_table = {}

    def get_state(self, predator, prey_list):
        return "default"

    def choose_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}

        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            action_values = self.q_table[state]
            max_q = max(action_values.values())
            best_actions = [act for act, val in action_values.items() if val == max_q]
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
