import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from buildsched.task_data import tasks, resources
from buildsched.genetic_algorithm import genetic_algorithm

def plot_schedule(schedule):
    """
    Plots a Gantt chart of the given schedule using matplotlib.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define a color map for different workers/machines
    colors = {
        'W1': 'blue', 'W2': 'green', 'W3': 'orange', 'W4': 'red', 'W5': 'purple', 'W6': 'brown',
        'M1': 'cyan', 'M2': 'magenta', 'M3': 'yellow'
    }
    
    # Create patches for the legend
    legend_patches = [mpatches.Patch(color=color, label=worker_id) for worker_id, color in colors.items()]
    
    for idx, task_schedule in enumerate(schedule):
        task = next(t for t in tasks if t['id'] == task_schedule['task_id'])
        start_time = task_schedule['start_time']
        end_time = start_time + task['duration']
        resource = task_schedule['resource']
        
        # Fallback color for undefined resources
        color = colors.get(resource, 'gray')  # Use gray if resource is not in the color map
        
        # Plot the task as a bar in the Gantt chart
        ax.barh(idx, end_time - start_time, left=start_time, color=color, edgecolor='black')
        
        # Annotate with task duration
        ax.text(start_time + (end_time - start_time) / 2, idx, f'{task["duration"]}h', 
                ha='center', va='center', color='black', fontsize=10)
    
    # Add labels and legend
    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Tasks")
    ax.set_title("Gantt Chart of Optimized Task Schedule")
    ax.set_yticks(range(len(schedule)))  # Ensure the y-axis ticks match the number of tasks
    ax.set_yticklabels([task['id'] for task in tasks])  # Label y-axis with task IDs
    
    ax.legend(handles=legend_patches, title="Workers/Machines")
    
    # Display the plot
    plt.tight_layout()
    plt.show()

# Run the genetic algorithm and get the best schedule
best_schedule = genetic_algorithm(population_size=10, generations=50, mutation_rate=0.1, tournament_size=3)

# Plot the best schedule
plot_schedule(best_schedule)
