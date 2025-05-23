CONFIG = {
    # General simulation settings
    "num_generations": 50,
    "num_prey": 20,
    "num_predators": 5,
    "world_size": (800, 600),
    "time_steps_per_generation": 300,

    # Prey trait ranges
    "trait_range": {
        "speed": (1.0, 3.0),
        "agility": (0.1, 1.0),
        "vision": (2.0, 5.0),
    },

    # Genetic Algorithm settings
    "mutation_rate": 0.1,
    "crossover_rate": 0.7,

    # Reinforcement Learning settings
    "rl": {
        "learning_rate": 0.1,
        "discount_factor": 0.9,
        "epsilon": 0.1,
    },

    # Clustering settings
    "k_clusters": 3,
    "cluster_interval": 10,  # every N generations

    # Output
    "log_dir": "data/logs",
    "plot_dir": "data/plots",
}
