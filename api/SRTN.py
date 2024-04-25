def srtf(arrival_times, burst_times):
    n = len(arrival_times)
    remaining_time = [0] * n
    for i in range(n):
        remaining_time[i] = burst_times[i]

    total_completed = 0
    current_time = 0
    min_burst = float('inf')
    shortest = 0
    finished = [False] * n
    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n

    while total_completed != n:
        for j in range(n):
            if arrival_times[j] <= current_time and remaining_time[j] < min_burst and remaining_time[j] > 0:
                min_burst = remaining_time[j]
                shortest = j

        if min_burst == float('inf'):
            current_time += 1
            continue

        remaining_time[shortest] -= 1
        min_burst = remaining_time[shortest]
        if min_burst == 0:
            min_burst = float('inf')

        if remaining_time[shortest] == 0:
            total_completed += 1
            completion_time[shortest] = current_time + 1
            finished[shortest] = True

            turnaround_time[shortest] = completion_time[shortest] - \
                arrival_times[shortest]
            waiting_time[shortest] = turnaround_time[shortest] - \
                burst_times[shortest]

        current_time += 1

    return completion_time, turnaround_time, waiting_time
