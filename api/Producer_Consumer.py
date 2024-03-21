import threading
import random
import time


class Monitor:
    """
    Synchronization tool for monitoring producer and consumer and ensuring they wait and signal before producing / consuming from the bounded.
    """
    BUFFER_SIZE = 5         # Maximum Size of the bounded buffer
    buffer = []             # Shared buffer
    monitor_busy = True     # The current status of the monitor
    monitor_lock = threading.Lock()  # Lock object for the Monitor from which synchronisation will occur
    condition_vars = threading.Condition(monitor_lock)  # Condition object using which monitor will wait and be notified

    @staticmethod
    def cwait() -> None:
        """
        Monitor method to ensure that the process will wait if the Monitor is busy and currently occupied.
        """
        with Monitor.monitor_lock:
            # with keyword helps with resource management "Entry & Exit methods"
            # & for error handling
            while Monitor.monitor_busy:
                Monitor.condition_vars.wait()  # Wait until monitor is free
            Monitor.monitor_busy = True

    @staticmethod
    def csignal() -> None:
        """
        Monitor method to send a signal in the consumer and producer methods to notify that the Monitor is now free.
        """
        with Monitor.monitor_lock:
            Monitor.monitor_busy = False
            Monitor.condition_vars.notify()  # Signal that monitor is free
    # "Append" method

    @staticmethod
    def produce(item_index: str, seconds: float) -> None:  # Insert into buffer
        """
        The producer inserts items into the bounded buffer and ensures synchronisation by using wait and signal methods
        of the monitor.
        """

        item_index = "P" + item_index  # Format the item name

        buffer_count = len(Monitor.buffer)  # Number of elements in the buffer

        if buffer_count == Monitor.BUFFER_SIZE:  # If the Buffer is full then wait
            Monitor.cwait()

        time.sleep(seconds)   # Halt execution temporarily to simulate processing

        Monitor.buffer.append(item_index)  # Insert new item into buffer
        Monitor.csignal()  # Notify the monitor that it is free

        print("Slept for %.1f" % seconds)
        print(f"Produced {item_index}, Buffer: {Monitor.buffer}")
        print('------------------------------------------------')

    @staticmethod
    def consume(seconds: float) -> None:
        """
        Consumer that pops items from the buffer, decrements the length (count--), and signals that monitor is free
        after deletion of item.
        """
        time.sleep(seconds)  # Halt execution temporarily to simulate processing

        if len(Monitor.buffer) == 0:  # Ensure buffer is not empty
            Monitor.cwait()  # If buffer is empty then wait indefinitely until items are added

        # Remove item from buffer
        item = Monitor.buffer.pop(0)
        # Notify monitor that it is now free
        Monitor.csignal()

        print("Slept for %.1f" % seconds)
        print(f"Consumed {item}, Buffer: {Monitor.buffer}")
        print(f"Number of Items left in Buffer: {len(Monitor.buffer)}")
        print('------------------------------------------------')


def produce_consume(item_index: int, process_times: list) -> None:
    """
    Method that calls both producer and consumer methods.
    This method will be a thread called in "process_as_begin"
    """
    # seconds = process_times[item_index]
    seconds = random.expovariate(0.5)
    item_index = str(item_index + 1)

    monitor = Monitor()
    monitor.produce(item_index, seconds)
    monitor.consume(seconds)


def process_as_begin(number_processes: int, times: list) -> None:  # process as begin
    """
    Begin process of producer & consumer.
    """

    threads_list = []

    for num in range(number_processes):  # Iterate and create new process threads until number of processes.
        thread = threading.Thread(target=produce_consume, args=(num, times))
        # Call produce_consume() in the thread, pass current process no. & times[] for execution seconds to the method
        thread.start()
        threads_list.append(thread)  # Insert thread into the list, to join it later

    for thread in threads_list:  # Join all the threads
        thread.join()  # Wait for each thread to finish executing before continuing to the rest of the program


def main() -> None:
    process_times = []

    while True:
        number_processes = int(input('Enter Number of Processes: '))
        print('------------------------------------------------')

        # for process_no in range(number_processes):
        #     time = int(input(f"Enter time for Process {process_no + 1}: "))
        #     processtimes.insert(process_no, time)  # process_no = index

        if number_processes > 1:
            process_as_begin(number_processes, process_times)
            print("All items produced and consumed.")
            break
        else:
            print("Number of processes must be greater than 1")


if __name__ == '__main__':
    main()
