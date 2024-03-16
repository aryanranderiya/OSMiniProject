from flask import Flask, render_template, request, redirect
from api import SRTN


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
    else:
        return "Invalid Option"


@app.route("/SRTNaddProcess", methods=["POST"])
def app_SRTN():

    form = request.form
    processes = SRTN.addProcess(form)
    gantt_chart = SRTN.generateGanttChart()
    print("------------------------------------", gantt_chart)
    return render_template('SRTN.html', processes=processes)
