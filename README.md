# Process Scheduling Algorithms

This project implements several process scheduling algorithms in Python. The goal is to simulate and understand the behavior of different scheduling methods in an operating system context.

## Table of Contents

1. [Introduction](#introduction)
2. [Algorithms Implemented](#algorithms-implemented)
3. [Project Structure](#project-structure)
4. [Classes and Methods](#classes-and-methods)
    - [PriorityQueue](#priorityqueue)
    - [Process](#process)
    - [Scheduler](#scheduler)

## Introduction

This project simulates various CPU scheduling algorithms, which are crucial for managing how processes are executed by the CPU. Scheduling algorithms determine the order in which processes are executed and can significantly impact the efficiency and performance of an operating system.

## Algorithms Implemented

1. **First Come First Served (FCFS)**

    - **Description**: Processes are executed in the order they arrive in the ready queue. The process that arrives first is executed first.
    - **Characteristics**: Non-preemptive, simple to implement, but can lead to the "convoy effect" where shorter processes are delayed by longer processes.

2. **Shortest Job First (SJF)**

    - **Description**: The process with the shortest burst time is executed next. If two processes have the same burst time, FCFS order is used.
    - **Characteristics**: Non-preemptive, optimal for minimizing average waiting time, but can cause starvation for longer processes.

3. **Shortest Remaining Time First (SRTF)**

    - **Description**: Similar to SJF but preemptive. The process with the shortest remaining burst time is executed next. If a new process arrives with a shorter burst time than the remaining time of the current process, the current process is preempted.
    - **Characteristics**: Preemptive, further minimizes average waiting time compared to SJF, but can also lead to starvation.

4. **Round Robin (RR)**

    - **Description**: Processes are executed in a cyclic order, each process getting a fixed time quantum (q = 5). If a process's burst time exceeds the time quantum, it is placed back in the ready queue with the remaining burst time.
    - **Characteristics**: Preemptive, fair as each process gets an equal share of CPU time, but can have higher average waiting time and overhead due to frequent context switching.

5. **Preemptive Priority Scheduling with Aging**

    - **Description**: Processes are executed based on their priority. A higher priority value means lower priority. If two processes have the same priority, FCFS order is used. Aging mechanism: the priority of a process is decremented by 1 if it remains in the ready queue for 5 time units.
    - **Characteristics**: Preemptive, reduces starvation through aging, but can be complex to implement.

6. **Non-preemptive Priority Scheduling with Aging**

    - **Description**: Similar to preemptive priority scheduling but non-preemptive. The process with the highest priority (lowest priority value) is executed next. Aging mechanism: the priority of a process is decremented by 1 if it remains in the ready queue for 5 time units.
    - **Characteristics**: Non-preemptive, simpler than the preemptive version, reduces starvation through aging, but can lead to lower responsiveness compared to preemptive scheduling.

## Project Structure

The project is structured as follows:

- **PriorityQueue**: Implementation of the priority queue with support for custom ordering using function objects.
- **Process**: A class representing a process in a scheduling algorithm.
- **Scheduler**: Class containing methods for scheduling as well as the main function.

## Classes and Methods

### PriorityQueue

A priority queue implementation that supports custom ordering. This is used to manage the processes based on their priority, arrival time, or remaining time, depending on the scheduling algorithm.

### Process

A class representing a process. The `Process` class includes attributes such as:

- Process ID
- Arrival time
- Burst time
- Priority
- Remaining time (for preemptive algorithms)
- Other relevant attributes

### Scheduler

The `Scheduler` module contains the following functions to simulate the different scheduling algorithms:

- `main()`: The main function to interactively run scheduling algorithms and display results.
- `show_menu()`: Displays the menu of available scheduling algorithms.
- `run_algorithm_FCFS(processes, time_limit)`: Runs the First Come, First Served (FCFS) scheduling algorithm.
- `run_algorithm_SJF(processes, time_limit)`: Runs the Shortest Job First (SJF) scheduling algorithm.
- `run_algorithm_SRTF(processes, time_limit)`: Runs the Shortest Remaining Time First (SRTF) scheduling algorithm.
- `run_algorithm_RR(processes, time_limit)`: Runs the Round Robin (RR) scheduling algorithm.
- `run_algorithm_PP(processes, is_preemptive, time_limit)`: Runs the preemptive or non-preemptive Priority with aging (PP) scheduling algorithm.
- `handle_arrival(processes, time, ready_queue)`: Handles the arrival of processes at a specific time.
- `handle_comeback(time, waiting_queue, ready_queue)`: Handles processes that are coming back to the ready queue after a comeback time.
- `print_gantt_chart(time, process)`: Prints the Gantt chart.
- `replace_process_SRTF(time, ready_queue, running_process)`: Replaces the currently running process in SRTF scheduling.
- `replace_process_RR(time, ready_queue, running_process)`: Replaces the currently running process in RR scheduling.
- `replace_process_PP(time, ready_queue, running_process)`: Replaces the currently running process in PP scheduling.
- `handle_priority(time, ready_queue)`: Updates priorities of processes in the ready queue based on a time-triggered condition.

