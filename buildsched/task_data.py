import random

# Task and resource data structures as defined earlier
tasks = [
    {'id': 'T1', 'description': 'Site Preparation', 'duration': 40, 'dependencies': [], 'resource': 'M1'},
    {'id': 'T2', 'description': 'Foundation Laying', 'duration': 60, 'dependencies': ['T1'], 'resource': 'M2'},
    {'id': 'T3', 'description': 'Steel Frame Erection', 'duration': 100, 'dependencies': ['T2'], 'resource': 'M3'},
    {'id': 'T4', 'description': 'Electrical Wiring', 'duration': 50, 'dependencies': ['T3'], 'resource': 'W1'},
    {'id': 'T5', 'description': 'Plumbing Installation', 'duration': 40, 'dependencies': ['T3'], 'resource': 'W2'},
    {'id': 'T6', 'description': 'Interior Walls', 'duration': 80, 'dependencies': ['T4', 'T5'], 'resource': 'W3'},
    {'id': 'T7', 'description': 'Roofing Installation', 'duration': 60, 'dependencies': ['T6'], 'resource': 'W4'},
    {'id': 'T8', 'description': 'Window Installation', 'duration': 30, 'dependencies': ['T6'], 'resource': 'W5'},
    {'id': 'T9', 'description': 'Final Inspections', 'duration': 20, 'dependencies': ['T7', 'T8'], 'resource': 'W6'}
]

resources = [
    {'id': 'W1', 'type': 'worker', 'skillset': 'Electrician', 'working_hours_per_day': 8},
    {'id': 'W2', 'type': 'worker', 'skillset': 'Plumber', 'working_hours_per_day': 8},
    {'id': 'W3', 'type': 'worker', 'skillset': 'Carpenter', 'working_hours_per_day': 8},
    {'id': 'W4', 'type': 'worker', 'skillset': 'Roofer', 'working_hours_per_day': 8},
    {'id': 'W5', 'type': 'worker', 'skillset': 'Glazier', 'working_hours_per_day': 8},
    {'id': 'M1', 'type': 'machine', 'skillset': 'Excavator', 'working_hours_per_day': 10},
    {'id': 'M2', 'type': 'machine', 'skillset': 'Concrete Mixer', 'working_hours_per_day': 10},
    {'id': 'M3', 'type': 'machine', 'skillset': 'Crane', 'working_hours_per_day': 10},
    {'id': 'W6', 'type': 'worker', 'skillset': 'Inspector', 'working_hours_per_day': 6}
]

def create_individual():
    """
    Creates a random individual (schedule) where tasks are assigned randomly
    """
    individual = []
    for task in tasks:
        # Assign start time randomly between 0 and 100 hours
        start_time = random.randint(0, 100)
        individual.append({'task_id': task['id'], 'start_time': start_time, 'resource': task['resource']})
    return individual

def create_population(population_size=10):
    """
    Create a population of random schedules
    """
    population = []
    for _ in range(population_size):
        individual = create_individual()
        population.append(individual)
    return population

def calculate_fitness(individual):
    """
    Calculates the fitness of an individual (schedule).
    Lower fitness values are better.
    """
    total_idle_time = 0
    dependency_violations = 0
    
    # Store the last end time of each resource to calculate idle time
    resource_end_times = {resource['id']: 0 for resource in resources}
    
    for task_schedule in individual:
        # Find the task and resource for this schedule entry
        task = next(t for t in tasks if t['id'] == task_schedule['task_id'])
        resource = next(r for r in resources if r['id'] == task_schedule['resource'])
        
        # Calculate task start and end times
        start_time = task_schedule['start_time']
        end_time = start_time + task['duration']
        
        # Calculate idle time (gaps between consecutive tasks on the same resource)
        if resource_end_times[resource['id']] < start_time:
            total_idle_time += start_time - resource_end_times[resource['id']]
        
        # Update the end time for the current resource
        resource_end_times[resource['id']] = end_time
        
        # Check dependency violations
        for dependency in task['dependencies']:
            # Find the scheduled start time of the dependency task
            dependency_task = next(t for t in individual if t['task_id'] == dependency)
            dependency_task_end_time = dependency_task['start_time'] + next(t for t in tasks if t['id'] == dependency)['duration']
            
            if dependency_task_end_time > start_time:
                dependency_violations += 1
    
    # Fitness is based on idle time and number of dependency violations
    fitness = total_idle_time + (dependency_violations * 100)  # Penalty for violations
    return fitness

# Example Usage
population = create_population(population_size=10)
for idx, individual in enumerate(population):
    fitness = calculate_fitness(individual)
    print(f"Individual {idx + 1} - Fitness: {fitness}")
