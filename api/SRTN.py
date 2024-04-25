def srtf(arrival_times, burst_times):
    """
    Performs Shortest Remaining Time First (SRTF) scheduling algorithm.

    Parameters:
        arrival_times (list of int): List of arrival times for each process.
        burst_times (list of int): List of burst times for each process.

    Returns:
        tuple: A tuple containing:
            - list of int: Completion time for each process.
            - list of int: Turnaround time for each process.
            - list of int: Waiting time for each process.
    """
    n = len(arrival_times)  # Number of processes
    # Initialize list to store remaining burst time for each process
    remaining_time = [0] * n
    for i in range(n):
        # Set remaining time to initial burst time
        remaining_time[i] = burst_times[i]

    total_completed = 0  # Initialize counter for total completed processes
    current_time = 0  # Initialize current time
    min_burst = float('inf')  # Initialize minimum burst time to infinity
    shortest = 0  # Initialize index of process with shortest remaining burst time
    # Initialize list to track completion status of each process
    finished = [False] * n
    # Initialize list to store completion time for each process
    completion_time = [0] * n
    # Initialize list to store turnaround time for each process
    turnaround_time = [0] * n
    # Initialize list to store waiting time for each process
    waiting_time = [0] * n

    # Loop until all processes are completed
    while total_completed != n:
        # Find process with shortest remaining burst time among arrived processes
        for j in range(n):
            if arrival_times[j] <= current_time and remaining_time[j] < min_burst and remaining_time[j] > 0:
                min_burst = remaining_time[j]
                shortest = j

        # If no process is ready, move to next time unit
        if min_burst == float('inf'):
            current_time += 1
            continue

        # Decrement remaining time of shortest process by 1
        remaining_time[shortest] -= 1
        # Update min_burst after decrement
        min_burst = remaining_time[shortest]

        # If process is completed, update completion time and process status
        if remaining_time[shortest] == 0:
            total_completed += 1
            completion_time[shortest] = current_time + 1
            finished[shortest] = True

            # Calculate turnaround time and waiting time for completed process
            turnaround_time[shortest] = completion_time[shortest] - \
                arrival_times[shortest]
            waiting_time[shortest] = turnaround_time[shortest] - \
                burst_times[shortest]

        current_time += 1  # Move to next time unit

    # Return completion time, turnaround time, and waiting time
    return completion_time, turnaround_time, waiting_time
