import copy

from PriorityQueue import *
from Process import *
from collections import deque

# Global variable to track the line number for Gantt chart output
line = 0

# Sample processes for scheduling algorithms
processes = [Process(1, 0, 10, 2, 3),
             Process(2, 1, 8, 4, 2),
             Process(3, 3, 14, 6, 3),
             Process(4, 4, 7, 8, 1),
             Process(5, 6, 5, 3, 0),
             Process(6, 7, 4, 6, 1),
             Process(7, 8, 6, 9, 2)]


def main():
    """
    The main function to interactively run scheduling algorithms and display results.
    """

    while True:
        show_menu()
        print("\n")
        option = input("Enter a number for one of the algorithms\n")
        global line
        line = 0

        # copy make a deep copy of all processes in the array to prevent
        # issues relating to the continuity of the menu

        processes_copy = copy.deepcopy(processes)

        print("Gantt Chart :\n\n")

        if option == "1":
            run_algorithm_FCFS(processes_copy, 200)

        elif option == "2":
            run_algorithm_SJF(processes_copy, 200)

        elif option == "3":
            run_algorithm_RR(processes_copy, 200)

        elif option == "4":
            run_algorithm_SRTF(processes_copy, 200)

        elif option == "5":
            run_algorithm_PP(processes_copy, True, 200)

        elif option == "6":
            run_algorithm_PP(processes_copy, False, 200)

        elif option == "7":
            print("Exiting program...")
            exit(0)
        else:
            print("invalid option!")

        print("\n")
        Process.print_calculations_time(processes_copy)


def show_menu():
    """
    Displays the menu of available scheduling algorithms.
    """

    print("________________________________________________________\n"
          ":::::::::::::::Scheduling Algorithms:::::::::::::::\n"
          "---------------------------------------------------------\n\n" +
          "1) First Come First Serve\n" +
          "2) Shortest Job First\n" +
          "3) Round Robin\n" +
          "4) Shortest Remaining Time First\n" +
          "5) Preemptive priority scheduling with aging\n" +
          "6) Non-preemptive priority scheduling with aging\n"
          "7) Exit")


def run_algorithm_FCFS(processes, time_limit):
    """
    Runs the First Come, First Served (FCFS) scheduling algorithm.

    Parameters:
        - processes (list): List of processes to be scheduled.
        - time_limit (int): The time limit for the simulation.
    """

    # set up the ready queue and the waiting queue for algorithm
    # simulation
    ready_queue = deque()
    waiting_queue = deque()

    # run the first process at time 0
    running_process = processes[0]
    running_process.has_executed = True
    running_process.start_time = 0

    # loop that simulates the algorithm from 1 to 200s
    for time in range(1, time_limit):

        # handle the debut of new processes
        handle_arrival(processes, time, ready_queue)
        # handle the return of processes from the waiting queue
        handle_comeback(time, waiting_queue, ready_queue)
        running_process.decrease_remaining()

        # a process has finished its job
        if running_process.remaining_time == 0:
            running_process.finish_time = time
            running_process.cpu_turn_time = time
            print_gantt_chart(time, running_process)

            # the process has finished, it goes to the waiting queue
            waiting_queue.append(running_process)

            # fetch the next process from the ready queue
            running_process = ready_queue.popleft()

            # update the waiting time by (currentTime - last time the process entered the ready queue)
            running_process.waiting_time = running_process.waiting_time + (time - running_process.ready_queue_time)
            running_process.has_executed = True

            # update the last time the process has entered the CPU
            running_process.start_time = time

    # update the CPU exit time of the last process to 200 (the loop does not handle that case)
    running_process.cpu_turn_time = time_limit
    print_gantt_chart(time_limit, running_process)


def run_algorithm_SJF(processes, time_limit):
    """
    Runs the Shortest Job First (SJF) scheduling algorithm.

    Parameters:
        - processes (list): List of processes to be scheduled.
        - time_limit (int): The time limit for the simulation.
    """

    # set up the ready queue and the waiting queue for algorithm
    # simulation
    ready_queue = PriorityQueue(lambda item: item.burst_time)  # order by burst time (shortest job first)
    waiting_queue = deque()

    # run the first process at time 0
    running_process = processes[0]
    running_process.has_executed = True
    running_process.start_time = 0

    # loop that simulates the algorithm from 1 to 200s
    for time in range(1, time_limit):

        # handle the debut of new processes
        handle_arrival(processes, time, ready_queue)

        # handle the return of processes from the waiting queue
        handle_comeback(time, waiting_queue, ready_queue)
        running_process.decrease_remaining()

        # a process has finished its job
        if running_process.remaining_time == 0:
            running_process.finish_time = time
            running_process.cpu_turn_time = time
            print_gantt_chart(time, running_process)

            # the process has finished, it goes to the waiting queue
            waiting_queue.append(running_process)

            # reset the remaining time of the process
            running_process.remainingTime = running_process.burst_time

            # fetch the next process from the ready queue
            running_process = ready_queue.pop()

            # update the waiting time by (currentTime - last time the process entered the ready queue)
            running_process.waiting_time = running_process.waiting_time + (time - running_process.ready_queue_time)

            running_process.has_executed = True
            running_process.start_time = time

    # update the CPU exit time of the last process to 200 (the loop does not handle that case)
    running_process.cpu_turn_time = time_limit
    print_gantt_chart(time_limit, running_process)


def run_algorithm_SRTF(processes, time_limit):
    """
        Runs the Shortest Remaining Time First (SRTF) scheduling algorithm.

        Parameters:
            - processes (list): List of processes to be scheduled.
            - time_limit (int): The time limit for the simulation.
    """

    # Set up the ready queue as a priority queue with a custom ordering
    # based on the remaining time, and then on ready queue time
    # so the peek is always the process having the least remaining time
    # and the one that arrived first to the ready queue.

    ready_queue = PriorityQueue(lambda item: item.remaining_time, lambda item: item.ready_queue_time)
    waiting_queue = deque()

    # run the first process at time 0
    running_process = processes[0]
    running_process.has_executed = True
    running_process.start_time = 0

    # loop that simulates the algorithm from 1 to 200s
    for time in range(1, time_limit):

        handle_arrival(processes, time, ready_queue)
        handle_comeback(time, waiting_queue, ready_queue)
        running_process.decrease_remaining()

        # a process has finished its job
        if running_process.remaining_time == 0:
            running_process.finish_time = time
            running_process.cpu_turn_time = time
            print_gantt_chart(time, running_process)
            waiting_queue.append(running_process)

            running_process = ready_queue.pop()
            running_process.waiting_time = running_process.waiting_time + (time - running_process.ready_queue_time)
            running_process.has_executed = True
            running_process.start_time = time

        # if the process has just started, then check if the other processes in the
        # ready queue have a lower remaining time, so they can interrupt the flow of the program
        else:
            running_process = replace_process_SRTF(time, ready_queue, running_process)

    # update the CPU exit time of the last process to 200 (the loop does not handle that case)
    running_process.cpu_turn_time = time_limit
    print_gantt_chart(time_limit, running_process)


def run_algorithm_RR(processes, time_limit):
    """
        Runs the Round Robin (RR) scheduling algorithm.

        Parameters:
            - processes (list): List of processes to be scheduled.
            - time_limit (int): The time limit for the simulation.
        """

    ready_queue = deque()
    waiting_queue = deque()

    # run the first process at time 0
    running_process = processes[0]
    running_process.has_executed = True
    running_process.start_time = 0

    # loop that simulates the algorithm from 1 to 200s
    for time in range(1, time_limit):

        flag = True
        handle_arrival(processes, time, ready_queue)
        handle_comeback(time, waiting_queue, ready_queue)
        running_process.decrease_remaining()

        if running_process.remaining_time == 0:
            flag = False
            running_process.finish_time = time
            running_process.cpu_turn_time = time
            print_gantt_chart(time, running_process)
            waiting_queue.append(running_process)

            running_process = ready_queue.popleft()
            running_process.waiting_time = running_process.waiting_time + (time - running_process.ready_queue_time)
            running_process.has_executed = True
            running_process.start_time = time

        # if the process has just started, then check if the other processes in the
        # ready queue have a lower remaining time, so they can interrupt the flow of the program
        if flag:
            running_process = replace_process_RR(time, ready_queue, running_process)

    running_process.cpu_turn_time = time_limit
    print_gantt_chart(time_limit, running_process)


def run_algorithm_PP(processes, is_preemptive, time_limit):
    """
        Runs the preemptive (or non) Priority with aging (PP) scheduling algorithm.

        Parameters:
            - processes (list): List of processes to be scheduled.
            - is_preemptive (bool) : indicates whether the algorithm is preemptive or non-preemptive
            - time_limit (int): The time limit for the simulation.
        """

    # Set up the ready queue as a priority queue with a custom ordering
    # based on the priority data field, and then on ready queue time
    # so the peek is always the process having the least priority
    # and the one that arrived first to the ready queue.

    ready_queue = PriorityQueue(lambda item: item.priority, lambda item: item.ready_queue_time)
    waiting_queue = deque()

    # run the first process at time 0
    running_process = processes[0]
    running_process.has_executed = True
    running_process.start_time = 0

    # loop that simulates the algorithm from 1 to 200s
    for time in range(1, time_limit):

        handle_priority(time, ready_queue)
        handle_arrival(processes, time, ready_queue)
        handle_comeback(time, waiting_queue, ready_queue)

        # handling the decrease of the priority for processes
        # every 5 seconds
        running_process.decrease_remaining()

        # a process has finished its job
        if running_process.remaining_time == 0:
            running_process.finish_time = time
            running_process.cpu_turn_time = time
            print_gantt_chart(time, running_process)
            waiting_queue.append(running_process)

            running_process.remainingTime = running_process.burst_time

            running_process = ready_queue.pop()
            running_process.waiting_time = running_process.waiting_time + (time - running_process.ready_queue_time)
            running_process.has_executed = True
            running_process.start_time = time

        # interrupt the flow of the running process if PP
        elif is_preemptive:
            temp = replace_process_PP(time, ready_queue, running_process)
            if temp is not None:
                print_gantt_chart(time, running_process)
                running_process = temp

    running_process.cpu_turn_time = time_limit
    print_gantt_chart(time_limit, running_process)


def handle_arrival(processes, time, ready_queue):
    """
    Handle the arrival of processes at a specific time.

    Parameters:
       - processes (list): List of process objects representing all processes.
       - time (int): The current time at which arrival is being handled.
       - ready_queue (list): A queue to store processes that have arrived and are ready for execution.
    """

    # Iterate through each process in the processes list.
    # Check if the arrival time of the process matches the current time.
    # If a matching process is found, update its ready_queue_time attribute to the current time.
    # Append the process to the ready_queue to indicate it is ready for execution.
    # Break the loop after the first matching process is handled.

    for process in processes:
        if process.arrival_time == time:
            process.ready_queue_time = time
            ready_queue.append(process)
            break


def handle_comeback(time, waiting_queue, ready_queue):
    """
    Handle processes that are coming back to the ready queue after a comeback time.

    Parameters:
        - time (int): The current time at which comebacks are being handled.
        - waiting_queue (deque): A queue containing processes that are waiting to come back.
        - ready_queue (list): A queue to store processes that have come back and are ready for execution.
    """

    # Iterate through each process in the 'waiting_queue'.
    # Check if the finish time plus comeback time of the process matches the current time.
    # If a matching process is found:
    # Reset its 'remaining_time' to the original 'burst_time'.
    # Update 'ready_queue_time' to the current time.
    # Append the process to the 'ready_queue'.
    # Add the process to the 'removed' list for later removal from 'waiting_queue'.
    # Remove the processes in the 'removed' list from the 'waiting_queue'.

    removed = []
    for process in waiting_queue:

        if process.finish_time + process.come_back == time:
            process.remaining_time = process.burst_time
            removed.append(process)
            process.ready_queue_time = time
            ready_queue.append(process)

    for process in removed:
        waiting_queue.remove(process)


def print_gantt_chart(time, process):
    global line
    line = line + 1
    print("%-3s ||%-2s|| %-3s\t  " % (process.start_time, process, time), end="")
    if line % 5 == 0:
        print("\n")


def replace_process_SRTF(time, ready_queue, running_process):
    """
    Replace the currently running process in Shortest Remaining Time First (SRTF) scheduling.

    Parameters: - time (int): The current time at which process replacement is being considered. - ready_queue (
    PriorityQueue): A priority queue containing processes with custom ordering based on remaining time. -
    running_process (Process): The process currently running.

    Returns:
       - Process: The updated running process after potential replacement.
    """

    if ready_queue.peek().remaining_time < running_process.remaining_time:
        print_gantt_chart(time, running_process)

        # Update ready_queue_time and cpu_turn_time for the currently running process
        running_process.ready_queue_time = time
        running_process.cpu_turn_time = time

        # Swap the currently running process with the one at the front of the ready queue
        temp = running_process
        running_process = ready_queue.pop()
        running_process.waiting_time = running_process.waiting_time + (time - running_process.ready_queue_time)
        ready_queue.append(temp)

        # Update start time and mark the newly running process as executed
        running_process.start_time = time
        running_process.has_executed = True

    return running_process


def replace_process_RR(time, ready_queue, running_process):
    """
    Replace the currently running process in Round Robin (RR) scheduling.

    Parameters:
        - time (int): The current time at which process replacement is being considered.
        - ready_queue (deque): A queue containing processes scheduled for execution in a round-robin manner.
        - running_process (Process): The process currently running.

    Returns:
        - Process: The updated running process after potential replacement.
    """

    if (time - running_process.start_time) % 5 == 0:

        print_gantt_chart(time, running_process)

        # Update ready_queue_time and cpu_turn_time for the currently running process
        running_process.ready_queue_time = time
        running_process.cpu_turn_time = time

        # Swap the currently running process with the one at the front of the ready queue
        temp = running_process
        running_process = ready_queue.popleft()
        running_process.waiting_time = running_process.waiting_time + (time - running_process.ready_queue_time)
        ready_queue.append(temp)

        # Update start time and mark the newly running process as executed
        running_process.start_time = time
        running_process.has_executed = True

    return running_process


def replace_process_PP(time, ready_queue, running_process):
    """
    Replace the currently running process in Preemptive Priority (PP) scheduling.

    Parameters:
        - time (int): The current time at which process replacement is being considered.
        - ready_queue (PriorityQueue): A priority queue containing processes scheduled based on priority.
        - running_process (Process): The process currently running.
    Returns:
        - Process: The updated running process after potential replacement.
    """

    temp = None
    if ready_queue.peek().priority < running_process.priority:
        running_process.ready_queue_time = time
        running_process.cpu_turn_time = time
        temp = running_process
        running_process = ready_queue.pop()
        running_process.waiting_time = running_process.waiting_time + (time - running_process.ready_queue_time)
        ready_queue.append(temp)
        running_process.start_time = time
        running_process.has_executed = True
        temp = running_process

    return temp


def handle_priority(time, ready_queue):
    """
    Update priorities of processes in the ready queue based on a time-triggered condition.

    Parameters:
    - time (int): The current time at which priority updates are being considered.
    - ready_queue (PriorityQueue): A priority queue containing processes scheduled based on priority.
    """

    # Create a copy of the processes in the ready queue.
    # Iterate through the copied processes and check if the process has spent 5 seconds in the ready queue
    # If yes, decrease the priority of the process.
    # Heapify the ready queue using the updated priorities

    list_copy = ready_queue.copy_heap_to_list()
    for process in list_copy:
        if (time - process.ready_queue_time) % 5 == 0:
            process.decrease_priority()
    ready_queue.heapify(list_copy)


main()
