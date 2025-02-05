from typing import List, Tuple

class Process:
    def __init__(self, id: str, arrival_time: int, burst_time: int):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

class RoundRobinScheduler:
    def __init__(self, quantum: int):
        self.quantum = quantum
        self.processes: List[Process] = []
        self.gantt_chart: List[Tuple[str, int, int]] = []  # (process_id, start_time, end_time)

    def add_process(self, process: Process):
        self.processes.append(process)

    def schedule(self):
        current_time = min(p.arrival_time for p in self.processes)
        remaining_processes = len(self.processes)
        
        # sort wit da arrival time
        self.processes.sort(key=lambda x: x.arrival_time)
        
        ready_queue = []
        process_index = 0
        
        while remaining_processes > 0:
            # add the arrived process to ready queue
            while process_index < len(self.processes) and self.processes[process_index].arrival_time <= current_time:
                ready_queue.append(self.processes[process_index])
                process_index += 1
            
            if not ready_queue:
                current_time += 1
                continue
            
            # from heap get the next process to run
            current_process = ready_queue.pop(0)
            # check this process to fit quantum or nah
            execution_time = min(self.quantum, current_process.remaining_time)
            # for gantt chart
            self.gantt_chart.append((current_process.id, current_time, current_time + execution_time))
            # for process timing
            current_time += execution_time
            current_process.remaining_time -= execution_time
            # if process is complete
            if current_process.remaining_time == 0:
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                remaining_processes -= 1
            else:
                # check for any new arrivals first then
                # back to ready queue if not complete
                while process_index < len(self.processes) and self.processes[process_index].arrival_time <= current_time:
                    ready_queue.append(self.processes[process_index])
                    process_index += 1
                ready_queue.append(current_process)

    def display_gantt_chart(self):
        print("\nGantt Chart:")
        print("-" * (len(self.gantt_chart) * 9)+"-")
        
       
        for process in self.gantt_chart:
            print(f"|{process[0]:^8}", end="")
        print("|")
        
        
        print("-" * (len(self.gantt_chart) * 9)+"-")
        for process in self.gantt_chart:
            print(f"{process[1]:<8}", end=" ")
        print(self.gantt_chart[-1][2])
        
    def display_process_table(self):
        print("\nProcess Table:")
        print("-" * 70)
        print(f"{'Process':^8} | {'Arrival':^8} | {'Burst':^8} | {'Finish':^10} | {'Turnaround':^10} | {'Waiting':^8}")
        print("-" * 70)
        sorted_processes = sorted(self.processes, key=lambda x: int(x.id[1:]))
        for process in self.processes:
            print(f"{process.id:^8} | {process.arrival_time:^8} | {process.burst_time:^8} | "
                  f"{process.completion_time:^10} | {process.turnaround_time:^10} | {process.waiting_time:^8}")
        
        # calculation
        avg_turnaround = sum(p.turnaround_time for p in self.processes) / len(self.processes)
        avg_waiting = sum(p.waiting_time for p in self.processes) / len(self.processes)
        print("-" * 70)
        print(f"Average Turnaround Time: {avg_turnaround:.2f}")
        print(f"Average Waiting Time: {avg_waiting:.2f}")

def main():
    print("This is from : TT2L GROUP3")
    print("Members:") 
    print("1)GOH CHUN YONG 241UC24158")
    print("2)YEE SI SHUN 241UC24157")
    print("3)CHEAH CHUN YONG 241UC2417G")
    quantum = 3
    scheduler = RoundRobinScheduler(quantum)
    
    
    while True:
        try:
            n_processes = int(input("Enter number of processes (3-10): "))
            if 3 <= n_processes <= 10:
                break
            print("Please enter a number between 3 and 10")
        except ValueError: #build in function hehe
            print("Please enter a valid number")
    
    # Get process details
    print("\nEnter details for each process:")
    for i in range(n_processes):
        print(f"\nProcess P{i}:")
        while True:
            try:
                arrival_time = int(input(f"Enter arrival time for P{i}: "))
                burst_time = int(input(f"Enter burst time for P{i}: "))
                if arrival_time >= 0 and burst_time > 0:
                    break
                print("Times must be non-negative and burst time must be positive")
            except ValueError:
                print("Please enter valid numbers")
                
        scheduler.add_process(Process(f"P{i}", arrival_time, burst_time))
    
    scheduler.schedule()
    
    scheduler.display_gantt_chart()
    scheduler.display_process_table()

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")