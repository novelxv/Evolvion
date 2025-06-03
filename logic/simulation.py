from core.environment import Environment
from core.prey import Prey
from core.predator import Predator
from logic.evolution import evolve_prey
from analysis.clustering import cluster_prey_traits
from analysis.visualization import plot_cluster_centroids
import random

def run_simulation(config: dict, logger_func, visualization_func):
    env = Environment(config)

    center_x, center_y = config["world_size"][0] / 2, config["world_size"][1] / 2
    for _ in range(config["num_prey"]):
        x = random.uniform(center_x - 100, center_x + 100)
        y = random.uniform(center_y - 100, center_y + 100)
        p = Prey(x, y, config, env)
        p.traits = {
            "speed": random.uniform(*config["trait_range"]["speed"]),
            "agility": random.uniform(*config["trait_range"]["agility"]),
            "vision": random.uniform(*config["trait_range"]["vision"])
        }
        env.add_agent(p)

    for _ in range(config["num_predators"]):
        x = center_x
        y = center_y
        pr = Predator(x, y, config, env)
        env.add_agent(pr)

    for gen in range(config["num_generations"]):
        print(f"=== Generation {gen+1} ===")
        env.reset_generation()

        for predator in env.predators:
            predator.last_state = predator.rl_agent.get_state(predator, env.prey)
            predator.last_action = random.choice(predator.rl_agent.actions)

        for predator in env.predators:
            predator.total_reward = 0.0

        for step in range(config["time_steps_per_generation"]):
            for predator in env.predators:
                predator.handle_movement()
            for predator in env.predators:
                predator.update()
            for predator in env.predators:
                predator.learn()

            for prey in env.prey:
                if prey.alive:
                    prey.handle_movement()
                    prey.update()

            env.remove_dead_agents()

            visualization_func(env, gen, step)

        evolve_prey(env.prey, config)

        env.agents.clear()
        for p in env.prey:
            env.agents.append(p)
        for pr in env.predators:
            env.agents.append(pr)

        logger_func(env, gen, config)

        labels, centroids = cluster_prey_traits(env.prey, config["k_clusters"])
        plot_cluster_centroids(centroids, gen, config)

        # for p in env.prey:
        #     p.x = random.uniform(0, config["world_size"][0])
        #     p.y = random.uniform(0, config["world_size"][1])

    print("Simulation completed.")


def debug_simulation(config: dict):
    import pygame
    # Initialize pygameMore actions
    pygame.init()

    # Set up the display
    try:
        screen = pygame.display.set_mode((config["world_size"][0], config["world_size"][1]))
        pygame.display.set_caption("Evolvion")
        clock = pygame.time.Clock()
        env = Environment(config)

        agent1 = Prey(config["world_size"][0] // 2 - 300, config["world_size"][0] // 2 - 50, config, env)
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
        # agent2.handle_input(keys)
        agent1.handle_movement()
        agent2.update()
        agent2.handle_movement()
        agent1.update()

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