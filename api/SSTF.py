# Function to calculate the distance between two disk requests
def calculate_distance(curr_position, request):
    """
    Calculates the distance between the current disk head position and a disk request.

    Parameters:
        curr_position (int): Current position of the disk head.
        request (int): Disk request for which the distance is calculated.

    Returns:
        int: Absolute distance between the current position and the request.
    """
    return abs(curr_position - request)

# Function to find the closest disk request to the current position


def find_closest_request(curr_position, requests):
    """
    Finds the closest disk request to the current position of the disk head.

    Parameters:
        curr_position (int): Current position of the disk head.
        requests (list of int): List of disk requests.

    Returns:
        int: Closest disk request to the current position.
    """
    min_distance = float('inf')  # Initialize minimum distance to infinity
    closest_request = None  # Initialize closest request to None
    for req in requests:
        # Calculate distance between current position and request
        distance = calculate_distance(curr_position, req)
        if distance < min_distance:  # If distance is less than current minimum distance
            min_distance = distance  # Update minimum distance
            closest_request = req  # Update closest request
    return closest_request


def sstf_disk_scheduling(initial_position, requests):
    """
    Performs Shortest Seek Time First (SSTF) disk scheduling.

    Parameters:
        initial_position (int): Initial position of the disk head.
        requests (list of int): List of disk requests.

    Returns:
        tuple: A tuple containing:
            - list of tuples: Sequence of disk requests accessed along with the distance moved for each access.
            - int: Total seek time required for all accesses.
    """
    sequence = []  # Initialize list to store sequence of disk requests accessed
    total_seek_time = 0  # Initialize total seek time to 0
    # Set current position of the disk head to initial position
    curr_position = initial_position
    while requests:  # While there are remaining requests
        # Find closest request to current position
        closest_request = find_closest_request(curr_position, requests)
        # Calculate distance to closest request
        distance = calculate_distance(curr_position, closest_request)
        total_seek_time += distance  # Update total seek time
        # Append closest request and distance to sequence
        sequence.append((closest_request, distance))
        curr_position = closest_request  # Move disk head to closest request
        # Remove closest request from remaining requests
        requests.remove(closest_request)
    return sequence, total_seek_time  # Return sequence and total seek time
