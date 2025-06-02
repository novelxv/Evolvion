import pygame
import sys
from core.agent_base import BaseAgent
from core.predator import Predator
from core.prey import Prey
from core.environment import Environment

def run_simulation(config):
    # Initialize pygame
    pygame.init()

    # Set up the display
    try:
        screen = pygame.display.set_mode((config["world_size"][0], config["world_size"][1]))
        pygame.display.set_caption("Evolvion")
        clock = pygame.time.Clock()
        env = Environment()

        agent1 = Prey(config["world_size"][0] // 2 - 100, config["world_size"][0] // 2 - 50, config, env)
        agent2 = Predator(config["world_size"][0] // 2, config["world_size"][0] // 2, config, env)

        env.add_agent(agent1)
        env.add_agent(agent2)
    except ValueError:
        print("The configuration is invalid")

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get current key states
        keys = pygame.key.get_pressed()
        
        # Update game objects
        # agent2.handle_input(keys)
        agent1.handle_movement()
        agent2.handle_movement()
        agent1.update()
        agent2.update()
        
        # Draw everything
        screen.fill(config["white"])
        agent2.draw(screen)
        agent1.draw(screen)
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate (60 FPS)
        clock.tick(60)

    # Quit
    pygame.quit()
    sys.exit()