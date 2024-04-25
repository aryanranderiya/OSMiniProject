def srtf(arrival_times, burst_times):
    n = len(arrival_times)  # Number of processes
    # Initialize lists to store remaining burst time, completion time, turnaround time, and waiting time for each process
    remaining_time = burst_times.copy()
    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n

    total_completed = 0  # Initialize counter for total completed processes
    current_time = 0  # Initialize current time
    while total_completed < n:
        min_burst = float('inf')  # Initialize minimum burst time to infinity
        shortest = None  # Initialize index of process with shortest remaining burst time

        # Find the process with the shortest remaining burst time among arrived and unfinished processes
        for i in range(n):
            if arrival_times[i] <= current_time and remaining_time[i] < min_burst and remaining_time[i] > 0:
                min_burst = remaining_time[i]
                shortest = i

        if shortest is None:  # No process is ready, move to the next arrival time
            current_time = min(arrival_times)
            continue

        # Decrement remaining time of the shortest process by 1
        remaining_time[shortest] -= 1

        # If the remaining time of the shortest process becomes 0, update completion time, turnaround time, and waiting time
        if remaining_time[shortest] == 0:
            total_completed += 1
            completion_time[shortest] = current_time + 1
            turnaround_time[shortest] = completion_time[shortest] - \
                arrival_times[shortest]
            waiting_time[shortest] = turnaround_time[shortest] - \
                burst_times[shortest]

        current_time += 1  # Move to the next time unit

    return completion_time, turnaround_time, waiting_time
