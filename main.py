import pygame
import sys
from logic.simulation import run_simulation, debug_simulation
from config import CONFIG
from analysis.logger import log_generation, dummy_logger
from analysis.visualization import plot_reward_curve, plot_trait_distribution
from ui.pygame_view import render

def main():
    pygame.init()
    
    # Get screen info for optimal sizing
    info = pygame.display.Info()
    max_width = info.current_w - 100
    max_height = info.current_h - 100
    
    # Use larger size but within screen bounds
    width = min(CONFIG["world_size"][0], max_width)
    height = min(CONFIG["world_size"][1], max_height)
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("🧬 EVOLVION - Advanced Evolution Simulator")
    
    # Set window icon
    icon = pygame.Surface((32, 32))
    icon.fill((100, 150, 255))
    pygame.display.set_icon(icon)
    
    clock = pygame.time.Clock()
    reward_history = []

    def custom_logger(env, gen, config):
        log_generation(env, gen, config)
        avg_reward = sum(pr.total_reward for pr in env.predators) / len(env.predators)
        reward_history.append(avg_reward)
        prey_data = [{"traits": p.traits} for p in env.prey]
        plot_trait_distribution(prey_data, gen, config)

    try:
        run_simulation(CONFIG, logger_func=custom_logger, visualization_func=render)
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
    
    plot_reward_curve(reward_history, CONFIG)

    # Show completion message
    font = pygame.font.Font(None, 48)
    text = font.render("Simulation Complete! Press any key to exit.", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width//2, height//2))
    
    screen.fill((25, 25, 35))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    # Wait for key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT, pygame.KEYDOWN]:
                waiting = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
