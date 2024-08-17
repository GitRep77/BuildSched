# fitness_function.py

from buildsched.task_data import resources, tasks

def calculate_fitness(individual):
    """
    Calculate the fitness of a schedule (individual) by evaluating
    the total idle time, dependency violations, and overall task
    scheduling efficiency. Lower fitness values are better.
    """
    total_idle_time = 0
    dependency_violations = 0
    working_hour_violations = 0

    # Track the end time of the last task for each resource to calculate idle time
    resource_end_times = {resource['id']: 0 for resource in resources}

    # Calculate fitness for each task in the schedule
    for task_schedule in individual:
        # Find the task and resource for this schedule entry
        task_id = task_schedule['task_id']
        start_time = task_schedule['start_time']
        task = next(t for t in tasks if t['id'] == task_id)
        resource = next(r for r in resources if r['id'] == task_schedule['resource'])
        
        # Calculate task end time
        end_time = start_time + task['duration']
        
        # Calculate idle time for the resource if there's a gap between consecutive tasks
        if resource_end_times[resource['id']] < start_time:
            total_idle_time += start_time - resource_end_times[resource['id']]
        
        # Update the resource's end time
        resource_end_times[resource['id']] = end_time
        
        # Check dependency violations
        for dependency in task['dependencies']:
            # Find the scheduled start time of the dependency task
            dependency_task = next(t for t in individual if t['task_id'] == dependency)
            dependency_end_time = dependency_task['start_time'] + next(t for t in tasks if t['id'] == dependency)['duration']
            
            # If the dependent task finishes after the current task's start time, it's a violation
            if dependency_end_time > start_time:
                dependency_violations += 1
        
        # Check working hour violations (e.g., tasks scheduled beyond resource working hours)
        daily_work_hours = resource['working_hours_per_day']
        task_duration = task['duration']
        
        # Calculate if the task exceeds the available working hours per day
        if task_duration > daily_work_hours:
            working_hour_violations += 1
    
    # Fitness value is the sum of idle time, dependency violations (penalized heavily), and working hour violations
    fitness = total_idle_time + (dependency_violations * 100) + (working_hour_violations * 50)
    
    return fitness
