import threading
import random
import time
import copy


class Monitor:
    """
    Synchronization tool for monitoring producer and consumer and ensuring they wait and signal before producing / consuming from the bounded.
    """

    BUFFER_SIZE = 5  # Maximum Size of the bounded buffer
    buffer = []  # Shared buffer
    monitor_busy = True  # The current status of the monitor

    # Lock object for the Monitor from which synchronisation will occur
    monitor_lock = threading.Lock()

    # object with which monitor will wait and notify
    condition_vars = threading.Condition(monitor_lock)

    def __init__(self):
        self.buffer_list = []  # Maintain history of all the buffers
        self.produce_consumed_list = []  # Maintain history of all produced/consumed items

    def add_buffer_list(self, buffer: list) -> None:
        self.buffer_list.append(buffer)

    def get_buffer(self) -> list:
        return self.buffer_list

    def add_prod_cons_list(self, obj: str) -> None:
        self.produce_consumed_list.append(obj)

    def get_produced_consumed(self) -> list:
        return self.produce_consumed_list

    def wait(self) -> None:
        """
        Monitor method to ensure that the process will wait if the Monitor is busy and currently occupied.
        """
        with self.monitor_lock:
            # with keyword helps with resource management "Entry & Exit methods"
            # & for error handling
            while self.monitor_busy:
                self.condition_vars.wait()  # Wait until monitor is free
            self.monitor_busy = True

    def signal(self) -> None:
        """
        Monitor method to send a signal in the consumer and producer methods to notify that the Monitor is now free.
        """
        with self.monitor_lock:
            self.monitor_busy = False
            self.condition_vars.notify()  # Signal that monitor is free
    # "Append" method

    def produce(self, item_index: str, seconds: float) -> None:  # Insert into buffer
        """
        The producer inserts items into the bounded buffer and ensures synchronisation by using wait and signal methods
        of the monitor.
        """

        item_index = "P" + item_index  # Format the item name

        buffer_count = len(self.buffer)  # Number of elements in the buffer

        if buffer_count == self.BUFFER_SIZE:  # If the Buffer is full then wait
            self.wait()

        # Halt execution temporarily to simulate processing
        time.sleep(seconds)

        self.buffer.append(item_index)  # Insert new item into buffer

        self.add_buffer_list(copy.deepcopy(self.buffer))
        self.add_prod_cons_list(f"Produced {item_index}")

        self.signal()  # Notify the monitor that it is free

        # print(f"Produced {item_index}, Buffer: {self.buffer}")
        # print('------------------------------------------------')

    def consume(self, seconds: float) -> None:
        """
        Consumer that pops items from the buffer, decrements the length (count--), and signals that monitor is free
        after deletion of item.
        """

        # Halt execution temporarily to simulate processing
        time.sleep(seconds)

        if len(self.buffer) == 0:  # Ensure buffer is not empty
            self.wait()  # If buffer is empty then wait indefinitely until items are added

        # Remove item from buffer
        item = self.buffer.pop(0)

        # Notify monitor that it is now free
        self.signal()

        self.add_buffer_list(copy.deepcopy(self.buffer))
        self.add_prod_cons_list(f"Consumed {item}")
        # self.add_prod_cons_list(
        #     f"Number of Items left in Buffer: {len(self.buffer)}")

        # print(f"Consumed {item}, Buffer: {self.buffer}")
        # print(f"Number of Items left in Buffer: {len(self.buffer)}")
        # print('------------------------------------------------')


def produce_consume(item_index: int, process_times: list, monitor: Monitor) -> None:
    """
    Method that calls both producer and consumer methods.
    This method will be a thread called in "process_as_begin"
    """
    # seconds = process_times[item_index]
    # seconds = random.expovariate(0.5)
    seconds = random.uniform(0.1, 3)

    # seconds = 1
    item_index = str(item_index + 1)

    monitor.produce(item_index, seconds)
    monitor.consume(seconds)  # monitor = self


def process_as_begin(number_processes: int, times: list, monitor: Monitor) -> None:  # process as begin
    """
    Begin process of producer & consumer.
    """

    threads_list = []

    # Iterate and create new process threads until number of processes.
    for num in range(number_processes):
        thread = threading.Thread(
            target=produce_consume, args=(num, times, monitor))
        # Call produce_consume() in the thread, pass current process no. & times[] for execution seconds to the method
        thread.start()
        # Insert thread into the list, to join it later
        threads_list.append(thread)

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
