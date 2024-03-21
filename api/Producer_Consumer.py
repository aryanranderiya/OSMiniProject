import threading
import random
import time


class Monitor:

    BUFFER_SIZE = 5  # Size of the bounded buffer
    buffer = []  # Shared buffer

    monitor_busy = True
    monitor_lock = threading.Lock()
    condition_vars = threading.Condition(monitor_lock)

    def cwait():
        with Monitor.monitor_lock:
            # with keyword helps with resource management "Entry & Exit methods"
            # & for error handling
            while Monitor.monitor_busy:
                Monitor.condition_vars.wait()  # Wait until monitor is free
            Monitor.monitor_busy = True

    def csignal():

        with Monitor.monitor_lock:
            Monitor.monitor_busy = False
            Monitor.condition_vars.notify()  # Signal that monitor is free

    # "Append" method
    def produce(item_index):  # Insert into buffer

        item_index = "P" + item_index

        # time.sleep(random.uniform(0.2, 5))
        time.sleep(random.expovariate(0.5))

        buffer_count = len(Monitor.buffer)

        if (buffer_count == Monitor.BUFFER_SIZE):
            Monitor.cwait()

        Monitor.buffer.append(item_index)  # Insert new item into buffer
        Monitor.csignal()

        print(f"Produced {item_index}, Buffer: {Monitor.buffer}")
        print('------------------------------------------------')

    def consume():

        # time.sleep(random.uniform(0.2, 5))
        time.sleep(random.expovariate(0.5))

        if (len(Monitor.buffer) == 0):  # buffer_count
            Monitor.cwait()

        # Remove item from buffer, Decrement count
        item = Monitor.buffer.pop(0)
        Monitor.csignal()

        print(f"Consumed {item},", end='')
        print(f" Buffer: {Monitor.buffer}")
        print(f"Number of Items left in Buffer: {len(Monitor.buffer)}")
        print('------------------------------------------------')


def call_producer_consumer(item_index, processtimes):
    # processtimes[index]
    item_index = str(item_index + 1)
    Monitor.produce(item_index)
    Monitor.consume()


def process_as_begin(number_processes, processtimes):  # process as begin

    threads_list = []
    for number in range(number_processes):

        thread = threading.Thread(
            target=call_producer_consumer, args=(number, processtimes))

        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()


def main():
    processtimes = []

    while True:
        number_processes = int(input('Enter Number of Processes: '))

        # for process_no in range(number_processes):
        # time = int(input(f"Enter time for Process {process_no + 1}: "))
        # processtimes.insert(process_no, time)  # process_no = index

        if (number_processes > 1):
            process_as_begin(number_processes, processtimes)
            print("All items produced and consumed.")
            break
        else:
            print("Number of processes must be greater than 1")


main()
