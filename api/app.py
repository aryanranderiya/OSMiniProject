from flask import Flask, render_template, request, redirect
from api import SRTN, PCBB
import time

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


@app.route("/addProcessSRTN", methods=["POST"])
def app_SRTN():
    processes = SRTN.addProcess(request.form)
    # gantt_chart = SRTN.generateGanttChart()
    # print("------------------------------------", gantt_chart)
    return render_template('SRTN.html', processes=processes)


@app.route("/addProcessPCBB", methods=["POST"])
def app_ProducerConsumer():
    form = request.form
    no_of_processes = int(form['no_of_processes'])

    monitor = PCBB.Monitor()

    PCBB.process_as_begin(no_of_processes, monitor)

    buffer_history = monitor.buffer_history
    produced_consumed = monitor.produce_consumed_list
    buffer_state_list = monitor.buffer_state_list

    zipped_data = zip(produced_consumed, buffer_history, buffer_state_list)

    return render_template('PCBB.html', zipped_data=zipped_data)


if __name__ == "__main__":
    app.config['DEBUG'] = True
