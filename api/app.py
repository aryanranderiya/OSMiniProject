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
            map(int, request.form.get('arrival_times').split(',')))
        burst_times = list(
            map(int, request.form.get('burst_times').split(',')))

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

        return render_template('SRTNresult.html', jobs_info=jobs_info)

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


if __name__ == "__main__":
    app.config['DEBUG'] = True
