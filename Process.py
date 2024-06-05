class Process:
    """
     A class representing a process in a scheduling algorithm.

    Attributes:
        - number (int): A unique identifier for the process.
        - arrival_time (int): The time at which the process arrives in the ready queue.
        - burst_time (int): The total CPU burst time required for the process to complete.
        - come_back (int): The time the process takes to come back to the ready queue after completion.
        - priority (int): The priority level of the process.
        - remaining_time (int): The remaining CPU burst time for the process.
        - finish_time (int): The time at which the process finishes execution.
        - waiting_time (int): The total time the process spends waiting in the ready queue.
        - ready_queue_time (int): The time at which the process is added to the ready queue.
        - has_executed (bool): Indicates whether the process has been executed.
        - start_time (int): The time at which the process starts execution.
        - cpu_turn_time (int): The time that that process exits the CPU. At the end of the loop, it
            would indicate the time at which it exits the CPU.

    Methods:
        - __init__: Initializes a Process instance with specified attributes (Class constructor).
        - decrease_remaining: Decreases the remaining CPU burst time for the process by one.
        - decrease_priority: Decreases the priority level of the process by one.
        - __str__: Returns a string representation of the process.
        - print_calculations_time: Static method to print average waiting time and average turnaround time for a list of processes.
    """

    finish_time = 0
    waiting_time = 0
    ready_queue_time = 0
    has_executed = False
    start_time = 0
    cpu_turn_time = 0

    def __init__(self, number, arrival_time, burst_time, come_back, priority):
        self.number = number
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.come_back = come_back
        self.priority = priority
        self.remaining_time = burst_time

    def decrease_remaining(self):
        """
        Decreases the remaining CPU burst time for the process.
        """
        if self.remaining_time <= 0:
            self.remaining_time = 0
        else:
            self.remaining_time = self.remaining_time - 1

    def decrease_priority(self):
        """
        Decreases the priority level of the process.
        """
        if self.priority <= 0:
            self.priority = 0
        else:
            self.priority = self.priority - 1

    def __str__(self):
        """
        Returns a string representation of the process.
        """
        return "P" + str(self.number)

    @staticmethod
    def print_calculations_time(processes):
        """
        Static method to print average waiting
        time and average turnaround time for a list of processes.

        Parameters:
        - processes (list): A list of Process instances.
        """

        # Shorthand for a loop that creates a list containing all processes that are executed
        # then computing the number of such processes in the list
        number_executed = len([process for process in processes if process.has_executed])

        # compute the sum of the waiting time of all processes that are executed at least once
        sum_waiting_time = sum(process.waiting_time for process in processes if process.has_executed)

        # # compute the sum of the turnaround time of all processes that are executed at least once
        sum_turnaroud_time = sum([(process.cpu_turn_time - process.arrival_time) for process in processes if process.has_executed])

        # print the average waiting time and turnaround time
        print("Average waiting time is: " + str(sum_waiting_time/number_executed))
        print("Average turnaround time is: " + str(sum_turnaroud_time/number_executed))
