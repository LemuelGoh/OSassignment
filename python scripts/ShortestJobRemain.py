# Example usage with testing data 1
# processes = [(Process, Arrival Time, Burst Time)]
# [(1, 2, 4), (2, 10, 1), (3, 3, 2), (4, 2, 5), (5, 0, 5)]
# 
# Process ID   Finish Time  Arrival Time   Turnaround Time   Burst Time  Waiting Time
# -------------------------------------------------------------------------------------
# 5            5            0              5                 5           0
# 3            7            3              4                 2           2
# 1            11           2              9                 4           5
# 2            12           10             2                 1           1
# 4            17           2              15                5           10
#
# Total Waiting Time: 18
# Total Turnaround Time: 35
# Average Waiting Time: 3.6
# Average Turnaround Time: 7.0
#
# Gantt Chart:
# |  P5  |  P3  |  P1  |  P2  |  P4  |
# 0      5      7      11      12      17

# Example usage with testing data 2
# processes = [(Process, Arrival Time, Burst Time)]
# [(1, 0, 7), (2, 2, 4), (3, 4, 1), (4, 5, 4)]
# 
# Process ID   Finish Time  Arrival Time   Turnaround Time   Burst Time  Waiting Time
# -------------------------------------------------------------------------------------
# 1            7            0              7                 7           0
# 3            8            4              4                 1           3
# 2            12           2              10                4           6
# 4            16           5              11                4           7
#
# Total Waiting Time: 16
# Total Turnaround Time: 32
# Average Waiting Time: 4.0
# Average Turnaround Time: 8.0
#
# Gantt Chart:
# |  P1  |  P3  |  P2  |  P4  |
# 0      7      8      12      16

def get_process_input():
    print("This is from : TT2L GROUP3")
    print("Members:") 
    print("1)GOH CHUN YONG 241UC24158")
    print("2)YEE SI SHUN 241UC24157")
    print("3)CHEAH CHUN YONG 241UC2417G")
    processes = []
    num_processes = int(input("Enter the number of processes(3-10): "))

    while num_processes < 3 or num_processes > 10:
        print("Please enter a number between 3 and 10.")
        num_processes = int(input("Enter the number of processes: "))
    
    for i in range(num_processes):
        print(f"Enter details for process {i+1}:")

        # Validate arrival_time input NO ALPHABERT AND NEGATIVE INTEGER
        while True:
            try:
                arrival_time = int(input("Arrival Time: "))  # Input for Arrival Time
                if arrival_time < 0:
                    print("Arrival time cannot be negative. Please enter a valid integer.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter an integer for arrival time.")
        
        # Validate burst_time input NO ALPHABERT AND NEGATIVE INTEGER
        while True:
            try:
                burst_time = int(input("Burst Time: "))  # Input for Burst Time
                if burst_time <= 0:
                    print("Burst time must be greater than 0. Please enter a valid integer.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter an integer for burst time.")

        processes.append((i+1, arrival_time, burst_time)) # Append in Array[1, 0, 5]
    
    return processes

def sjn_scheduling(processes):
    n = len(processes)
    processes.sort(key=lambda x: (x[1], x[2]))  # Sort by arrival time, then burst time

    completion_time = [0] * n
    waiting_time = [0] * n
    turnaround_time = [0] * n
    start_time = [0] * n

    current_time = 0
    remaining_processes = processes.copy()

    while remaining_processes:
        # Filter processes that have arrived by the current time
        available_processes = [p for p in remaining_processes if p[1] <= current_time]

        if not available_processes:
            # If no processes are available, move time forward to the next arrival
            current_time = min(p[1] for p in remaining_processes)
            continue

        # Select the process with the shortest burst time
        shortest_process = min(available_processes, key=lambda x: x[2])
        process_index = processes.index(shortest_process)

        # Update start time and completion time
        start_time[process_index] = current_time
        completion_time[process_index] = current_time + shortest_process[2]
        current_time = completion_time[process_index]

        # Remove the scheduled process from the remaining array
        remaining_processes.remove(shortest_process)

    # Calculate waiting time and turnaround time
    for i in range(n):
        turnaround_time[i] = completion_time[i] - processes[i][1]
        waiting_time[i] = turnaround_time[i] - processes[i][2]

    # Combine process details and sort by start time for Gantt Chart
    result = [(processes[i][0], start_time[i], completion_time[i], processes[i][1], turnaround_time[i], processes[i][2], waiting_time[i]) for i in range(n)]
    result.sort(key=lambda x: x[1])  # Sort by start time

    # Print the results with proper alignment
    header = f"\n{'Process ID':<12} {'Finish Time':<12} {'Arrival Time':<14} {'Turnaround Time':<17} {'Burst Time':<11} {'Waiting Time':<13}"
    print(header)
    print('-' * len(header))

    for res in result:
        print(f"{res[0]:<12} {res[2]:<12} {res[3]:<14} {res[4]:<17} {res[5]:<11} {res[6]:<13}")

    # Calculate average waiting time and turnaround time
    total_waiting_time = sum(waiting_time)
    total_turnaround_time = sum(turnaround_time)
    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    # Printed TOTAL_WAITING_TIME TOTAL_TURNAROUND_TIME AVG_WAITING_TIME AVG_TURNAROUND_TIME
    print(f"\nTotal Waiting Time: {total_waiting_time}")
    print(f"Total Turnaround Time: {total_turnaround_time}")
    print(f"Average Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")

    # Print the Gantt Chart with correct alignment
    print("\nGantt Chart:")
    gantt_chart = "|"
    timeline = "0"

    for i in range(n):
        gantt_chart += f"  P{result[i][0]}  |" #result[i][0] = processes
        timeline += f"      {result[i][2]}" #result[i][2] = completion_time

    print(gantt_chart)
    print(timeline)


# Example usage
processes = get_process_input()
sjn_scheduling(processes)
input("\nPress Enter to exit...")