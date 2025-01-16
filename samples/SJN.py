def sjf_non_preemptive():
    n = int(input("Enter number of processes: "))
    processes = []

    # Automatically name processes as P1, P2, ..., Pn
    for i in range(n):
        name = f"P{i + 1}"  # Automatically assign process names
        arrival = int(input(f"Arrival time of {name}: "))
        burst = int(input(f"Burst time of {name}: "))
        processes.append((name, arrival, burst))

    # Sort by arrival time first, then by burst time
    processes.sort(key=lambda x: (x[1], x[2]))

    current_time = 0
    gantt_chart = []
    waiting_time = {}
    turnaround_time = {}

    while processes:
        available = [p for p in processes if p[1] <= current_time]
        if available:
            # Pick shortest job
            job = min(available, key=lambda x: x[2])
            processes.remove(job)
            name, arrival, burst = job

            gantt_chart.append((current_time, name))
            
            # Update waiting and turnaround times
            waiting_time[name] = current_time - arrival
            current_time += burst
            turnaround_time[name] = current_time - arrival
        else:
            current_time += 1

    gantt_chart.append((current_time, ""))  # Add the final time

    # Output Gantt Chart
    print("\nGantt Chart:")
    chart_line = "|"
    time_line = ""

    for i in range(len(gantt_chart) - 1):
        start_time, name = gantt_chart[i]
        end_time, _ = gantt_chart[i + 1]
        process_width = end_time - start_time

        # Center process names in allocated space
        chart_line += f" {name} ".center(process_width + 2, " ") + "|"
        time_line += f"{start_time}".ljust(len(chart_line) - len(time_line))

    # Add the final time marker
    time_line += f"{gantt_chart[-1][0]}"
    print(chart_line)
    print(time_line)

    #sort 
    sorted_processes = sorted(waiting_time.keys())
    # Output Waiting and Turnaround Times
    print("\nProcess\tWaiting\tTurnaround")
 
    for name in sorted_processes:
        
        print(f"{name}\t{waiting_time[name]}\t{turnaround_time[name]}")

    avg_waiting = sum(waiting_time.values()) / n
    avg_turnaround = sum(turnaround_time.values()) / n
    print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")

# Run the program
sjf_non_preemptive()
