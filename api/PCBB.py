import threading
import copy
import time
import random

# Constants
EMPTY = 0
BUFFER_SIZE = 5


class Monitor:
    """
    Synchronization tool for monitoring producer and consumer and ensuring they wait and signal before producing / consuming from the bounded.
    """

    buffer = []  # Shared buffer

    # Lock object for the Monitor that provides exclusive access to a shared resource in a multithreaded application
    # Can also be known as a mutex
    # Forces threads to access the shared resource 1 at a time instead of all at once
    monitor_lock = threading.Lock()

    # Condition object with which monitor will sychronise threades based on 'monitor_lock'
    # A condition variable allows one or more threads to wait until they are notified by another thread.
    condition_vars = threading.Condition(monitor_lock)

    def __init__(self):
        self._buffer_history = []  # Maintain history of all the buffers
        self._produce_consumed = []  # Maintain history of all produced/consumed items
        self._buffer_states = []  # Maintain history of all produced/consumed items

    # Properties to display on the Frontend

    @property
    def buffer_history(self) -> list:
        return self._buffer_history

    @property
    def produce_consumed_list(self) -> list:
        return self._produce_consumed

    @property
    def buffer_state_list(self) -> list:
        return self._buffer_states

    def add_buffer_history(self) -> None:
        """
        Append the buffers to a history list to keep track of all the buffers to display to the user
        """

        # Create a copy of the buffer, adding the buffer directly will simply pass the reference
        buffer = copy.deepcopy(self.buffer)

        if not buffer:
            # If buffer is empty then append EMPTY to history
            self.add_buffer_state_list("Consumer waiting..")
            self._buffer_history.append("EMPTY")

        elif len(buffer) is BUFFER_SIZE:
            # If buffer is full then append FULL along with the buffer to history
            self.add_buffer_state_list("Producer waiting...")
            buffer = "FULL — " + ", ".join(buffer)
            self._buffer_history.append(buffer)

        else:
            # Buffer is normal
            self.add_buffer_state_list("-")
            self._buffer_history.append(", ".join(buffer))

    def add_prod_cons_list(self, item: str) -> None:
        """
        Setter method to append to "_produce_consumed" list to keep track of all items produced and consumed
        """
        self._produce_consumed.append(item)

    def add_buffer_state_list(self, state: str) -> None:
        """
        Setter method to append to "_buffer_states" list to keep track of the current state of the buffer.
        Values can be 'Producer waiting...' or 'Consumer waiting...'
        """
        self._buffer_states.append(state)

    def produce(self, item_name: int) -> None:
        """
        Monitor public method for consumer to access & 'append'
        """

        # With is used for exceptional handling
        with self.monitor_lock:

            # time.sleep(random.uniform(0, 2))  # Simulate some running time

            buffer_count = len(self.buffer)  # Number of elements in the buffer

            if buffer_count is BUFFER_SIZE:  # If the Buffer is full then wait
                print("Buffer FULL, Producer is waiting for Consumer...")
                print('------------------------------------------------')
                self.condition_vars.wait()

            # Insert new item into buffer
            self.buffer.append(item_name)

            # Notify monitor that it is now free
            self.condition_vars.notify()  # Notify the monitor that it is free

            # Keep track of consumed items
            self.add_prod_cons_list(f"Produced {item_name}")

            # Keep track of the buffer
            self.add_buffer_history()

            print(f"Produced {item_name}, Buffer: {self.buffer}")
            print('------------------------------------------------')

    def consume(self) -> None:
        """
        Monitor public method for consumer to access
        """
        with self.monitor_lock:

            # time.sleep(random.uniform(0, 1))  # Simulate some running time

            if not self.buffer:  # Ensure buffer is not empty
                print("Buffer EMPTY, Consumer is waiting for Producer ...")
                print('------------------------------------------------')
                self.condition_vars.wait()

            # Remove item from buffer
            item_name = self.buffer.pop(0)

            # Notify monitor that it is now free
            self.condition_vars.notify()

            # Keep track of consumed items
            self.add_prod_cons_list(f"Consumed {item_name}")

            # Keep track of the buffer
            self.add_buffer_history()

            print(f"Consumed {item_name}, Buffer: {self.buffer}")
            print('------------------------------------------------')

    # ! End of class ^


def producer(monitor: Monitor, no_of_processes: int) -> None:  # Insert into buffer
    """
    The producer inserts items into the bounded buffer and ensures synchronisation by using wait and signal methods
    of the monitor.
    """

    for count in range(no_of_processes):
        item_name: str = "P" + str(count)  # Format the item name
        monitor.produce(item_name)  # Call the Monitors produce method


def consumer(monitor: Monitor, no_of_processes: int) -> None:
    """
    Consumer that pops items from the buffer, decrements the length (count--), and signals that monitor is free
    after deletion of item.
    """

    for _ in range(no_of_processes):
        monitor.consume()  # Call the Monitors consume method


def process_as_begin(no_of_processes: int, monitor=Monitor()) -> None:  # process as begin
    """
    Begin process of producer & consumer.
    """
    print('------------------------------------------------')

    # Create Producer Thread
    thread1 = threading.Thread(
        target=producer, args=(monitor, no_of_processes,))

    # Create Consumer Thread
    thread2 = threading.Thread(
        target=consumer, args=(monitor, no_of_processes,))

    # Start both producer & consumer threads
    thread1.start()
    thread2.start()

    # Wait for each thread to finish executing before continuing to the rest of the program
    thread1.join()
    thread2.join()

    print("All items produced and consumed.")


def main() -> None:
    """
    Main method of the application. Will only be called if manually run using 'python PCBB.py'. 
    Won't be executed using flask.
    Takes user input and passes to "processs_as_begin" to create threads for producer & consumer
    """

    while True:
        no_of_processes = int(input('Enter No. of Processes: '))

        if no_of_processes > 0:
            process_as_begin(no_of_processes)
            break

        print("Number of processes must be greater than 0")


if __name__ == '__main__':
    main()
