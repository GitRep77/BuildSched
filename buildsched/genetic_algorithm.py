import random
from buildsched.fitness_function import calculate_fitness
from buildsched.task_data import create_population

def tournament_selection(population, tournament_size=3):
    """
    Selects the best individual from a random tournament of the population.
    """
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda ind: calculate_fitness(ind))
    return tournament[0]

def crossover(parent1, parent2):
    """
    Performs single-point crossover between two parents to create offspring.
    """
    crossover_point = random.randint(1, len(parent1) - 1)
    
    # Create offspring by combining parts of parents
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    
    return offspring1, offspring2

def mutate(individual, mutation_rate=0.1):
    """
    Performs swap mutation on the individual with a certain probability.
    """
    for task_schedule in individual:
        if random.random() < mutation_rate:
            # Randomly pick two tasks and swap their start times
            task1, task2 = random.sample(individual, 2)
            task1['start_time'], task2['start_time'] = task2['start_time'], task1['start_time']
    return individual

def genetic_algorithm(population_size=10, generations=50, mutation_rate=0.1, tournament_size=3):
    """
    Runs the genetic algorithm with selection, crossover, and mutation.
    """
    # Create initial population
    population = create_population(population_size)
    
    for generation in range(generations):
        new_population = []
        
        # Generate new offspring
        while len(new_population) < population_size:
            # Selection
            parent1 = tournament_selection(population, tournament_size)
            parent2 = tournament_selection(population, tournament_size)
            
            # Crossover
            offspring1, offspring2 = crossover(parent1, parent2)
            
            # Mutation
            offspring1 = mutate(offspring1, mutation_rate)
            offspring2 = mutate(offspring2, mutation_rate)
            
            # Add offspring to the new population
            new_population.append(offspring1)
            if len(new_population) < population_size:
                new_population.append(offspring2)
        
        # Evaluate the new population
        population = sorted(new_population, key=lambda ind: calculate_fitness(ind))[:population_size]
        
        # Best individual in this generation
        best_individual = population[0]
        best_fitness = calculate_fitness(best_individual)
        
        # Output for every generation
        print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")
    
    return best_individual

# Run the genetic algorithm
best_schedule = genetic_algorithm(population_size=10, generations=50, mutation_rate=0.1, tournament_size=3)

# Final result
print("\nBest Schedule Found:")
for task in best_schedule:
    print(task)
