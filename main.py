from buildsched.task_data import tasks, resources
from buildsched.genetic_algorithm import genetic_algorithm
from buildsched.gantt_chart_visualization import plot_schedule

# Run the genetic algorithm
# Specify the actual parameters for population size, generations, mutation rate, and tournament size
best_schedule = genetic_algorithm(population_size=10, generations=50, mutation_rate=0.1, tournament_size=3)

# Plot the best schedule
plot_schedule(best_schedule)