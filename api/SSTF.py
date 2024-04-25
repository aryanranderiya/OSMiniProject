
# Function to calculate the distance between two disk requests
def calculate_distance(curr_position, request):
    return abs(curr_position - request)

# Function to find the closest disk request to the current position


def find_closest_request(curr_position, requests):
    min_distance = float('inf')
    closest_request = None
    for req in requests:
        distance = calculate_distance(curr_position, req)
        if distance < min_distance:
            min_distance = distance
            closest_request = req
    return closest_request


def sstf_disk_scheduling(initial_position, requests):
    sequence = []
    total_seek_time = 0
    curr_position = initial_position
    while requests:
        closest_request = find_closest_request(curr_position, requests)
        distance = calculate_distance(curr_position, closest_request)
        total_seek_time += distance
        sequence.append((closest_request, distance))
        curr_position = closest_request
        requests.remove(closest_request)
    return sequence, total_seek_time
