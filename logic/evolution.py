import random
import copy

def evolve_prey(prey_list: list, config: dict):
    survivors = [p for p in prey_list if p.alive]
    if not survivors:
        survivors = prey_list.copy()

    total_fitness = sum(p.fitness for p in survivors)
    if total_fitness == 0:
        for p in survivors:
            p.fitness = 1.0
        total_fitness = len(survivors)

    def select_parent():
        pick = random.uniform(0, total_fitness)
        current = 0.0
        for p in survivors:
            current += p.fitness
            if current >= pick:
                return p
        return survivors[-1]

    new_generation = []
    n = len(prey_list)
    for _ in range(n):
        parent1 = select_parent()
        parent2 = select_parent()
        
        child = copy.deepcopy(parent1)
        for trait in child.traits:
            child.traits[trait] = (parent1.traits[trait] + parent2.traits[trait]) / 2
        
        for trait in child.traits:
            if random.random() < config["mutation_rate"]:
                low, high = config["trait_range"][trait]
                child.traits[trait] = random.uniform(low, high)
        
        child.alive = True
        child.fitness = 0.0
        
        new_generation.append(child)

    prey_list[:] = new_generation
    
    for child in prey_list:
        child.x = random.uniform(0, config["world_size"][0])
        child.y = random.uniform(0, config["world_size"][1])
