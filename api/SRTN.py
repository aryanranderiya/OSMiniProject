process_dict = {}


def addProcess(form):

    process_dict[form['process_name']] = {
        'process_arrival': form['process_arrival'],
        'process_burst': form['process_burst']
    }

    return process_dict


def generateGanttChart():

    sorted_arrival = sorted(
        process_dict, key=lambda k: process_dict[k]['process_arrival'])

    sorted_burst = sorted(
        process_dict, key=lambda k: process_dict[k]['process_burst'])

    print("Sorted by Arrival", sorted_arrival)
    print("Sorted by Burst", sorted_burst)
    
    return process_dict


if __name__ == "__main__":
    ...
