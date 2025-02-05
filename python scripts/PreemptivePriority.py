from typing import List, Tuple

class Process:
    def __init__(self, id: str, arrival_time: int, burst_time: int, priority: int):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority  
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.start_time = None

    def __lt__(self, other):
        if self.priority == other.priority: #mannnnn
            return self.arrival_time < other.arrival_time
        return self.priority < other.priority

class PriorityScheduler:
    def __init__(self):
        self.processes: List[Process] = []
        self.gantt_chart: List[Tuple[str, int, int]] = []

    def add_process(self, process: Process):
        self.processes.append(process)

    def schedule(self):
        current_time = min(p.arrival_time for p in self.processes)
        remaining_processes = len(self.processes)
        ready_queue = []
        completed_processes = []
        last_process = None

        while remaining_processes > 0:
           
            for process in self.processes:
                #print(process.priority)
                if (process.arrival_time <= current_time and process.remaining_time > 0 and process not in completed_processes and process not in [p for p in ready_queue]):
                    ready_queue.append(process)
            
            if not ready_queue:
                current_time += 1
                continue

            
            ready_queue.sort(key=lambda x: (x.priority, x.arrival_time))
            current_process = ready_queue[0]

            
            if last_process != current_process:
                if self.gantt_chart:
                    if self.gantt_chart[-1][0] != current_process.id:
                        self.gantt_chart.append((current_process.id, current_time, None))
                else:
                    self.gantt_chart.append((current_process.id, current_time, None))

            # we compare time by time
            current_process.remaining_time -= 1
            current_time += 1
            last_process = current_process

            if current_process.remaining_time == 0:
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                completed_processes.append(current_process)
                ready_queue.remove(current_process)
                remaining_processes -= 1
                
                
                if self.gantt_chart[-1][2] is None:
                    self.gantt_chart[-1] = (self.gantt_chart[-1][0], self.gantt_chart[-1][1], current_time)

    def display_gantt_chart(self):
        print("\nGantt Chart:")
        print("-" * ((len(self.gantt_chart) * 9))+"-")
        
        for process in self.gantt_chart:
            print(f"|{process[0]:^8}", end="")
        print("|")
        
        print("-" * ((len(self.gantt_chart) * 9))+"-")
        for process in self.gantt_chart:
            print(f"{process[1]:<8}", end=" ")
        print(self.gantt_chart[-1][2])

    def display_process_table(self):
        print("\nProcess Table:")
        print("-" * 80)
        print(f"{'Process':^8} | {'Priority':^8} | {'Arrival':^8} | {'Burst':^8} | "
              f"{'Finish':^10} | {'Turnaround':^10} | {'Waiting':^8}")
        print("-" * 80)
        
        for process in sorted(self.processes, key=lambda x: x.id):
            print(f"{process.id:^8} | {process.priority:^8} | {process.arrival_time:^8} | "
                  f"{process.burst_time:^8} | {process.completion_time:^10} | "
                  f"{process.turnaround_time:^10} | {process.waiting_time:^8}")
        
        avg_turnaround = sum(p.turnaround_time for p in self.processes) / len(self.processes)
        avg_waiting = sum(p.waiting_time for p in self.processes) / len(self.processes)
        print("-" * 80)
        print(f"Average Turnaround Time: {avg_turnaround:.2f}")
        print(f"Average Waiting Time: {avg_waiting:.2f}")

def main():
    print("This is from : TT2L GROUP3")
    print("Members:") 
    print("1)GOH CHUN YONG 241UC24158")
    print("2)YEE SI SHUN 241UC24157")
    print("3)CHEAH CHUN YONG 241UC2417G")
    scheduler = PriorityScheduler()
    
    while True:
        try:
            n_processes = int(input("Enter number of processes between 3 to 10 (P1,P2,P3...): "))
            if 3 <= n_processes <= 10:
                break
            print("Please enter a number between 3 and 10")
        except ValueError:
            print("Please enter a valid number")

    print("\nEnter priority for each process:")
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

    scheduler.schedule()
    scheduler.display_gantt_chart()
    scheduler.display_process_table()

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")