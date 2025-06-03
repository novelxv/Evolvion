CONFIG = {
    # General simulation settings
    "num_generations": 15,
    "num_prey": 20,
    "num_predators": 5,
    "world_size": (1200, 800),
    "white": (255, 255, 255),
    "blue": (0, 100, 255),
    "red": (255, 0, 0),
    "transparent": (255, 255, 255, 0),
    "time_steps_per_generation": 200,

    # Prey trait ranges
    "trait_range": {
        "speed": (1.0, 3.0),
        "agility": (0.1, 1.0),
        "vision": (2.0, 5.0),
    },

    # Predator trait ranges
    "predator_speed": 10.0,
    "predator_vision": 20.0,

    # Genetic Algorithm settings
    "mutation_rate": 0.05,
    "crossover_rate": 0.6,

    # Reinforcement Learning settings
    "rl": {
        "learning_rate": 0.2,
        "discount_factor": 0.9,
        "epsilon": 0.4,
    },

    # Clustering settings
    "k_clusters": 3,
    "cluster_interval": 10,  # every N generations

    # Output
    "log_dir": "data/logs",
    "plot_dir": "data/plots",
}
