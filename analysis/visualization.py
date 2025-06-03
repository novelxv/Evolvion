import matplotlib.pyplot as plt
import os

def plot_reward_curve(reward_history, config):
    os.makedirs(config["plot_dir"], exist_ok=True)
    plt.figure()
    plt.plot(range(1, len(reward_history) + 1), reward_history, marker="o")
    plt.title("Average Predator Reward per Generation")
    plt.xlabel("Generation")
    plt.ylabel("Average Reward")
    plt.savefig(os.path.join(config["plot_dir"], "predator_reward_curve.png"))
    plt.close()

def plot_trait_distribution(prey_data, gen: int, config: dict):
    speeds = [p["traits"]["speed"] for p in prey_data]
    agilities = [p["traits"]["agility"] for p in prey_data]
    visions = [p["traits"]["vision"] for p in prey_data]

    os.makedirs(config["plot_dir"], exist_ok=True)
    plt.figure()
    plt.hist(speeds, bins=10, color="blue", alpha=0.7)
    plt.title(f"Generation {gen+1} – Speed Distribution")
    plt.xlabel("Speed")
    plt.ylabel("Count")
    plt.savefig(os.path.join(config["plot_dir"], f"speed_dist_gen{gen+1}.png"))
    plt.close()

    plt.figure()
    plt.hist(agilities, bins=10, color="green", alpha=0.7)
    plt.title(f"Generation {gen+1} – Agility Distribution")
    plt.xlabel("Agility")
    plt.ylabel("Count")
    plt.savefig(os.path.join(config["plot_dir"], f"agility_dist_gen{gen+1}.png"))
    plt.close()

    plt.figure()
    plt.hist(visions, bins=10, color="orange", alpha=0.7)
    plt.title(f"Generation {gen+1} – Vision Distribution")
    plt.xlabel("Vision")
    plt.ylabel("Count")
    plt.savefig(os.path.join(config["plot_dir"], f"vision_dist_gen{gen+1}.png"))
    plt.close()

def plot_cluster_centroids(centroids, gen: int, config: dict):
    if centroids is None:
        return

    os.makedirs(config["plot_dir"], exist_ok=True)
    import numpy as np
    speeds = centroids[:, 0]
    agilities = centroids[:, 1]
    visions = centroids[:, 2]

    plt.figure()
    plt.scatter(speeds, agilities, c="red", marker="x")
    for i, (s, a) in enumerate(zip(speeds, agilities)):
        plt.text(s, a, f"C{i}")
    plt.title(f"Generation {gen+1} – Cluster Centroids (Speed vs Agility)")
    plt.xlabel("Speed")
    plt.ylabel("Agility")
    plt.savefig(os.path.join(config["plot_dir"], f"centroids_gen{gen+1}.png"))
    plt.close()
