process_dict = {}


def addProcess(form):

    process_dict[form['process_name']] = {
        'process_arrival': form['process_arrival'],
        'process_burst': form['process_burst']
    }

    return process_dict


if __name__ == "__main__":
    ...
