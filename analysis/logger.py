import os
import json

def log_generation(env, gen: int, config: dict):
    os.makedirs(config["log_dir"], exist_ok=True)
    log_path = os.path.join(config["log_dir"], f"gen_{gen+1}.json")

    prey_traits = []
    for p in env.prey:
        prey_traits.append({
            "traits": p.traits,
            "fitness": p.fitness,
            "alive": p.alive
        })

    predator_data = []
    for predator in env.predators:
        predator_data.append({
            "total_reward": predator.total_reward
        })

    record = {
        "generation": gen + 1,
        "num_prey_alive": sum(1 for p in env.prey if p.alive),
        "prey_data": prey_traits,
        "predator_data": predator_data
    }

    with open(log_path, "w") as f:
        json.dump(record, f, indent=2)

def dummy_logger(env, gen, config):
    alive_count = sum(1 for p in env.prey if p.alive)
    avg_reward = sum(pr.total_reward for pr in env.predators) / len(env.predators)
    print(f"Gen {gen+1}: Prey alive = {alive_count}, Avg Predator Reward = {avg_reward:.2f}")
