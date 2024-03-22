import threading
import random
import time
import copy

# Constants
EMPTY = 0
BUFFER_SIZE = 5


class Monitor:
    """
    Synchronization tool for monitoring producer and consumer and ensuring they wait and signal before producing / consuming from the bounded.
    """

    buffer = []  # Shared buffer

    # Lock object for the Monitor from which synchronisation will occur
    monitor_lock = threading.Lock()

    # object with which monitor will wait and notify
    condition_vars = threading.Condition(monitor_lock)

    def __init__(self):
        self._buffer_history = []  # Maintain history of all the buffers
        self._produce_consumed = []  # Maintain history of all produced/consumed items
        self._buffer_states = []  # Maintain history of all produced/consumed items

    @property
    def buffer_list(self) -> list:
        return self._buffer_history

    @property
    def produce_consumed_list(self) -> list:
        return self._produce_consumed

    def add_buffer_list(self, buffer: list) -> None:
        buffer = ", ".join(buffer) if buffer else "Buffer is Empty"
        self._buffer_history.append(buffer)

    def add_prod_cons_list(self, item: str) -> None:
        self._produce_consumed.append(item)

    def add_buffer_state_list(self, state: str) -> None:
        self._buffer_states.append(state)

    def append(self, item_name: int) -> None:
        """
        Monitor public method for consumer to access
        """

        with self.monitor_lock:

            buffer_count = len(self.buffer)  # Number of elements in the buffer

            if buffer_count == BUFFER_SIZE:  # If the Buffer is full then wait
                print("Buffer FULL, Producer is waiting...")
                print('------------------------------------------------')
                self.condition_vars.wait()

            self.buffer.append(item_name)  # Insert new item into buffer

            self.add_buffer_list(copy.deepcopy(self.buffer))
            self.add_prod_cons_list(f"Produced {item_name}")

            self.condition_vars.notify()  # Notify the monitor that it is free

            print(f"Produced {item_name}, Buffer: {self.buffer}")
            print('------------------------------------------------')

    def take(self) -> None:
        """
        Monitor public method for consumer to access
        """
        with self.monitor_lock:

            buffer_count = len(self.buffer)  # Number of elements in the buffer

            if (buffer_count) == EMPTY:  # Ensure buffer is not empty
                print("Buffer EMPTY, Consumer is waiting...")
                print('------------------------------------------------')
                self.condition_vars.wait()

            # Remove item from buffer
            item = self.buffer.pop(0)

            # Notify monitor that it is now free
            self.condition_vars.notify()

            self.add_buffer_list(copy.deepcopy(self.buffer))
            self.add_prod_cons_list(f"Consumed {item}")

            print(f"Consumed {item}, Buffer: {self.buffer}")
            print('------------------------------------------------')

    # ! End of class ^


def producer(seconds: float, monitor: Monitor, no_of_processes: int) -> None:  # Insert into buffer
    """
    The producer inserts items into the bounded buffer and ensures synchronisation by using wait and signal methods
    of the monitor.
    """
    for count in range(no_of_processes):
        item_name: str = "P" + str(count)  # Format the item name
        monitor.append(item_name)


def consumer(seconds: float, monitor: Monitor, no_of_processes: int) -> None:
    """
    Consumer that pops items from the buffer, decrements the length (count--), and signals that monitor is free
    after deletion of item.
    """

    for _ in range(no_of_processes):
        monitor.take()


def process_as_begin(no_of_processes: int, monitor=Monitor()) -> None:  # process as begin
    """
    Begin process of producer & consumer.
    """

    thread1 = threading.Thread(
        target=producer, args=(0.5, monitor, no_of_processes,))

    thread2 = threading.Thread(target=consumer, args=(
        0.5, monitor, no_of_processes,))

    thread1.start()
    thread2.start()

    # Wait for each thread to finish executing before continuing to the rest of the program
    thread1.join()
    thread2.join()


def main() -> None:

    while True:
        no_of_processes = int(input('Enter No. of Processes: '))
        print('------------------------------------------------')

        if no_of_processes > 0:
            process_as_begin(no_of_processes)
            print("All items produced and consumed.")
            break
        else:
            print("Number of processes must be greater than 0")


if __name__ == '__main__':
    main()
