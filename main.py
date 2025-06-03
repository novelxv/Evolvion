import pygame
import sys
from logic.simulation import run_simulation
from config import CONFIG
from analysis.logger import log_generation, dummy_logger
from ui.pygame_view import render

def main():
    pygame.init()
    screen = pygame.display.set_mode(CONFIG["world_size"])
    pygame.display.set_caption("Evolvion - Full Simulation")
    clock = pygame.time.Clock()

    # run_simulation(CONFIG, logger_func=log_generation, visualization_func=render)
    run_simulation(CONFIG, dummy_logger, lambda *args: None)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
