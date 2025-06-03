import pygame
import sys
from logic.simulation import run_simulation
from config import CONFIG
from analysis.logger import log_generation, dummy_logger
from analysis.visualization import plot_reward_curve, plot_trait_distribution
from ui.pygame_view import render

def main():
    pygame.init()
    screen = pygame.display.set_mode(CONFIG["world_size"])
    pygame.display.set_caption("Evolvion - Full Simulation")
    clock = pygame.time.Clock()

    reward_history = []

    def custom_logger(env, gen, config):
        log_generation(env, gen, config)
        avg_reward = sum(pr.total_reward for pr in env.predators) / len(env.predators)
        reward_history.append(avg_reward)
        prey_data = [{"traits": p.traits} for p in env.prey]
        plot_trait_distribution(prey_data, gen, config)

    run_simulation(CONFIG, logger_func=custom_logger, visualization_func=render)
    run_simulation(CONFIG, dummy_logger, lambda *args: None)

    plot_reward_curve(reward_history, CONFIG)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
