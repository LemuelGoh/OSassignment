from typing import List, Tuple
import heapq

class Process:
    def __init__(self, id: str, arrival_time: int, burst_time: int, priority: int):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority  # Lower number means higher priority
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.start_time = None

    def __lt__(self, other):
        # For priority queue comparison
        return self.priority < other.priority

class PriorityScheduler:
    def __init__(self):
        self.processes: List[Process] = []
        self.gantt_chart: List[Tuple[str, int, int]] = []  # (process_id, start_time, end_time)

    def add_process(self, process: Process):
        self.processes.append(process)

    def schedule(self):
        current_time = min(p.arrival_time for p in self.processes)
        remaining_processes = len(self.processes)
        ready_queue = []
        process_map = {p.id: p for p in self.processes}
        last_process_id = None

        while remaining_processes > 0:
            # Add newly arrived processes to ready queue
            for process in self.processes:
                if (process.arrival_time <= current_time and 
                    process.remaining_time > 0 and 
                    process.id not in [p[1].id for p in ready_queue]):
                    # Add to ready queue with priority as key
                    heapq.heappush(ready_queue, (process.priority, process))

            if not ready_queue:
                current_time += 1
                continue

            # Get highest priority process
            _, current_process = heapq.heappop(ready_queue)

            # If this is a new process starting or a different process from last time
            if last_process_id != current_process.id:
                if last_process_id is not None:
                    # End the last process's time slot
                    self.gantt_chart.append((last_process_id, 
                                           self.gantt_chart[-1][2] if self.gantt_chart else current_time-1,
                                           current_time))
                # Start new process time slot
                if current_process.start_time is None:
                    current_process.start_time = current_time

            # Execute for 1 time unit
            current_process.remaining_time -= 1
            current_time += 1
            last_process_id = current_process.id

            # If process is complete
            if current_process.remaining_time == 0:
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                remaining_processes -= 1
                # Add final gantt chart entry
                self.gantt_chart.append((current_process.id, 
                                       self.gantt_chart[-1][2] if self.gantt_chart else current_time-1,
                                       current_time))
                last_process_id = None
            else:
                # Process still has remaining time, check if it should continue
                heapq.heappush(ready_queue, (current_process.priority, current_process))

        # Clean up and merge consecutive slots of the same process
        self.merge_gantt_chart()

    def merge_gantt_chart(self):
        if not self.gantt_chart:
            return
            
        merged = []
        current = list(self.gantt_chart[0])
        
        for entry in self.gantt_chart[1:]:
            if entry[0] == current[0]:  # Same process
                current[2] = entry[2]  # Extend end time
            else:
                merged.append(tuple(current))
                current = list(entry)
        merged.append(tuple(current))
        
        self.gantt_chart = merged

    def display_gantt_chart(self):
        print("\nGantt Chart:")
        print("-" * (len(self.gantt_chart) * 10))
        
        # Process names
        for process in self.gantt_chart:
            print(f"|{process[0]:^8}", end="")
        print("|")
        
        # Timeline
        print("-" * (len(self.gantt_chart) * 10))
        for process in self.gantt_chart:
            print(f"{process[1]:<8}", end=" ")
        print(self.gantt_chart[-1][2])

    def display_process_table(self):
        print("\nProcess Table:")
        print("-" * 80)
        print(f"{'Process':^8} | {'Priority':^8} | {'Arrival':^8} | {'Burst':^8} | "
              f"{'Finish Time':^10} | {'Turnaround':^10} | {'Waiting':^8}")
        print("-" * 80)
        
        for process in sorted(self.processes, key=lambda x: x.id):
            print(f"{process.id:^8} | {process.priority:^8} | {process.arrival_time:^8} | "
                  f"{process.burst_time:^8} | {process.completion_time:^10} | "
                  f"{process.turnaround_time:^10} | {process.waiting_time:^8}")
        
        # Calculate and display averages
        avg_turnaround = sum(p.turnaround_time for p in self.processes) / len(self.processes)
        avg_waiting = sum(p.waiting_time for p in self.processes) / len(self.processes)
        print("-" * 80)
        print(f"Average Turnaround Time: {avg_turnaround:.2f}")
        print(f"Average Waiting Time: {avg_waiting:.2f}")

def main():
    scheduler = PriorityScheduler()
    
    # Get number of processes
    while True:
        try:
            n_processes = int(input("Enter number of processes (3-10): "))
            if 3 <= n_processes <= 10:
                break
            print("Please enter a number between 3 and 10")
        except ValueError:
            print("Please enter a valid number")
    
    # Get process details
    print("\nEnter details for each process:")
    print("Note: Lower priority number means higher priority")
    for i in range(n_processes):
        print(f"\nProcess P{i}:")
        while True:
            try:
                arrival_time = int(input(f"Enter arrival time for P{i}: "))
                burst_time = int(input(f"Enter burst time for P{i}: "))
                priority = int(input(f"Enter priority for P{i}: "))
                if arrival_time >= 0 and burst_time > 0:
                    break
                print("Times must be non-negative and burst time must be positive")
            except ValueError:
                print("Please enter valid numbers")
                
        scheduler.add_process(Process(f"P{i}", arrival_time, burst_time, priority))
    
    # Run the scheduler
    scheduler.schedule()
    
    # Display results
    scheduler.display_gantt_chart()
    scheduler.display_process_table()

if __name__ == "__main__":
    main()