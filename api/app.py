import random
from flask import Flask, render_template, request, redirect
from api import PCBB
from api.SRTN import srtf
app = Flask(__name__)


@app.route("/")
def index(name=None):
    return render_template('index.html', name=name)


@app.route("/home", methods=["POST"])
def selectedOption():
    select = request.form['select']

    print("Requested Option is:", select)

    if select == "SRTN":
        return render_template('SRTN.html')
    elif select == "PCBB":
        return render_template('PCBB.html')
    elif select == "SSTF":
        return render_template('SSTF.html')
    elif select == "OPR":
        return render_template('OPR.html')
    else:
        return "Invalid Option"


@app.route('/SRTN', methods=['GET', 'POST'])
def SRTN():
    if request.method == 'POST':
        arrival_times = list(
            map(int, request.form.get('arrival_times').split(' ')))
        burst_times = list(
            map(int, request.form.get('burst_times').split(' ')))

        completion_time, turnaround_time, waiting_time = srtf(
            arrival_times, burst_times)

        jobs_info = []
        for i in range(len(arrival_times)):
            job_info = {
                'JobName': f'Job {i+1}',
                'Arrival Time': arrival_times[i],
                'Burst Time': burst_times[i],
                'Finish Time': completion_time[i],
                'Turnaround Time': turnaround_time[i],
                'Waiting Time': waiting_time[i]
            }
            jobs_info.append(job_info)

        return render_template('SRTN.html', jobs_info=jobs_info)

    return render_template('SRTN.html')


@app.route("/PCBB", methods=["POST"])
def app_ProducerConsumer():

    form = request.form
    no_of_processes = int(form['no_of_processes'])

    # Create a new object of the Monitor to access the history & list of states & items
    monitor = PCBB.Monitor()

    # Begin the process
    PCBB.process_as_begin(no_of_processes, monitor)

    buffer_history = monitor.buffer_history
    produced_consumed = monitor.produce_consumed_list
    buffer_state_list = monitor.buffer_state_list

    # Zip will combine all the lists into 1
    zipped_data = zip(produced_consumed, buffer_history, buffer_state_list)

    # Render the frontend using the zipped lists
    return render_template('PCBB.html', zipped_data=zipped_data)

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

# Function to simulate SSTF disk scheduling algorithm


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


def optimal_page_replacement(pages, capacity):
    page_faults = 0
    page_frames = []
    page_fault_details = []

    for page in pages:
        if page not in page_frames:
            if len(page_frames) < capacity:
                page_frames.append(page)
            else:
                future_occurrences = {}
                for i in range(len(page_frames)):
                    try:
                        future_occurrences[page_frames[i]] = pages.index(
                            page_frames[i], pages.index(page))
                    except ValueError:
                        future_occurrences[page_frames[i]] = float('inf')

                page_to_replace = max(future_occurrences,
                                      key=future_occurrences.get)
                replaced_page = page_frames[page_frames.index(page_to_replace)]
                page_frames[page_frames.index(page_to_replace)] = page
                page_fault_details.append(
                    {'page': page, 'replaced_page': replaced_page, 'page_frames': page_frames.copy()})
            page_faults += 1

    return page_faults, page_fault_details


@app.route('/OPR', methods=['GET', 'POST'])
def OPR():
    pages = list(map(int, request.form['pages'].split(',')))
    capacity = int(request.form['capacity'])
    page_faults, page_fault_details = optimal_page_replacement(
        pages, capacity)
    return render_template('OPR.html', page_faults=page_faults, page_fault_details=page_fault_details, pages=request.form['pages'], capacity=request.form['capacity'])


@app.route('/SSTF', methods=['GET', 'POST'])
def SSTF():
    initial_position = int(request.form['initial_position'])
    max_requests = int(request.form['max_requests'])
    max_position = int(request.form['max_position'])
    random_seed = int(request.form['random_seed'])
    random.seed(random_seed)
    requests = [random.randint(0, max_position)
                for _ in range(max_requests)]
    sequence, total_seek_time = sstf_disk_scheduling(
        initial_position, requests)
    return render_template('SSTF.html', sequence=sequence, total_seek_time=total_seek_time)


if __name__ == "__main__":
    app.config['DEBUG'] = True
