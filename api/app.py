import random
from flask import Flask, render_template, request, redirect

# Importing functions from the API modules
from api import PCBB
from api.SRTN import srtf
from api.OPR import optimal_page_replacement
from api.SSTF import *

app = Flask(__name__)

# Route for the homepage


@app.route("/")
def index(name=None):
    return render_template('index.html', name=name)

# Route for handling the option selected from the homepage


@app.route("/home", methods=["POST"])
def selectedOption():
    select = request.form['select']

    print("Requested Option is:", select)

    # Based on the selected option, redirect to the corresponding route
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

# Route for handling Shortest Remaining Time Next (SRTN) algorithm


@app.route('/SRTN', methods=['GET', 'POST'])
def SRTN():
    # Get arrival times and burst times from the form
    arrival_times = list(
        map(int, request.form.get('arrival_times').split(' ')))
    burst_times = list(
        map(int, request.form.get('burst_times').split(' ')))

    # Calculate completion time, turnaround time, and waiting time using SRTN algorithm
    completion_time, turnaround_time, waiting_time = srtf(
        arrival_times, burst_times)

    # Prepare job information for rendering in the template
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

    # Render the SRTN template with job information
    return render_template('SRTN.html', jobs_info=jobs_info)


# Route for handling Producer-Consumer Buffer Bound (PCBB) algorithm
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

    # Render the PCBB template with zipped data
    return render_template('PCBB.html', zipped_data=zipped_data)

# Route for handling Optimal Page Replacement (OPR) algorithm


@app.route('/OPR', methods=['GET', 'POST'])
def OPR():

    # Extracting page references and capacity from the form submitted by the user
    # List of page references converted to integers
    pages = list(map(int, request.form['pages'].split(',')))
    capacity = int(request.form['capacity'])  # Capacity of page frames

    # Performing Optimal Page Replacement (OPR) algorithm
    # This function returns the number of page faults and details of each page fault
    page_faults, page_fault_details = optimal_page_replacement(pages, capacity)

    # Rendering the OPR template with the results and form inputs
    # The page_faults, page_fault_details, pages, and capacity are passed to the template for displaying on the frontend
    return render_template('OPR.html', page_faults=page_faults, page_fault_details=page_fault_details, pages=request.form['pages'], capacity=request.form['capacity'])


# Route for handling Shortest Seek Time First (SSTF) algorithm
@app.route('/SSTF', methods=['POST'])
def SSTF():
    # Extracting input values from the form
    # Initial position of the disk head
    initial_position = int(request.form['initial_position'])
    # Total number of disk requests to be generated
    max_requests = int(request.form['max_requests'])
    # Maximum position of the disk
    max_position = int(request.form['max_position'])
    # Seed for random number generation
    random_seed = int(request.form['random_seed'])

    # Setting the random seed to ensure reproducibility
    random.seed(random_seed)

    # Generating random disk requests within the specified range
    requests = [random.randint(0, max_position) for _ in range(max_requests)]

    # Performing Shortest Seek Time First (SSTF) disk scheduling
    sequence, total_seek_time = sstf_disk_scheduling(
        initial_position, requests)

    # Rendering the SSTF template with the resulting sequence and total seek time
    return render_template('SSTF.html', sequence=sequence, total_seek_time=total_seek_time)


# Run the Flask app
if __name__ == "__main__":
    app.config['DEBUG'] = True
