from core.environment import Environment
from core.prey import Prey
from core.predator import Predator
from logic.evolution import evolve_prey
from analysis.clustering import cluster_prey_traits
from analysis.visualization import plot_cluster_centroids
import random
import time

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
        x = random.uniform(center_x - 200, center_x + 200)
        y = random.uniform(center_y - 200, center_y + 200)
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
            should_continue = visualization_func(env, gen, step)
            
            while should_continue is False:
                time.sleep(0.1) 
                should_continue = visualization_func(env, gen, step)
            
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

        evolve_prey(env.prey, config)

        new_prey_list = []
        for _ in range(config["num_prey"]):
            if len(env.prey) > config["num_prey"]:
                new_prey_list = env.prey[:config["num_prey"]]
            else:
                new_prey_list = env.prey.copy()
                while len(new_prey_list) < config["num_prey"]:
                    x = random.uniform(0, config["world_size"][0])
                    y = random.uniform(0, config["world_size"][1])
                    p = Prey(x, y, config, env)
                    p.traits = {
                        "speed": random.uniform(*config["trait_range"]["speed"]),
                        "agility": random.uniform(*config["trait_range"]["agility"]),
                        "vision": random.uniform(*config["trait_range"]["vision"])
                    }
                    new_prey_list.append(p)
            for child in new_prey_list:
                child.alive = True
                child.fitness = 0.0
        env.prey = new_prey_list

        env.agents = []
        for p in env.prey:
            env.agents.append(p)
        for pr in env.predators:
            env.agents.append(pr)

        logger_func(env, gen, config)

        labels, centroids = cluster_prey_traits(env.prey, config["k_clusters"])
        plot_cluster_centroids(centroids, gen, config)

    print("Simulation completed.")


def debug_simulation(config: dict):
    import pygame
    # Initialize pygame
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