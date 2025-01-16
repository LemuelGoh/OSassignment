#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

class Process {
public:
    string pid;
    int AT;   // Arrival Time
    int BT;   // Burst Time
    int RT;   // Remaining Time (same as BT for non-preemptive)
    int priority;
    int FinishTime;
    int TAT;  // Turnaround Time
    int WT;   // Waiting Time

    Process(string id, int at, int bt, int pr)
        : pid(id), AT(at), BT(bt), RT(bt), priority(pr),
          FinishTime(0), TAT(0), WT(0) {}
};

class Scheduler {
private:
    vector<Process> processes;

    // We will store the schedule in a small Gantt-Chart-like structure:
    // Each entry holds the process ID, the time it started, and the time it ended.
    vector< pair<string, pair<int,int>> > gantt; 
    //           PID         start,  finish

public:
    void addProcess(const string &id, int AT, int BT, int priority) {
        processes.emplace_back(id, AT, BT, priority);
    }

    // Non-Preemptive Priority Scheduling
    void nonPreemptivePriorityScheduling() {
        // 1. Sort processes by arrival time
        sort(processes.begin(), processes.end(),
             [](const Process &a, const Process &b) {
                 return a.AT < b.AT;
             });

        int time = 0;
        int completed = 0;
        int n = processes.size();

        // 2. While not all processes are completed
        while (completed < n) {
            int idx = -1;          // Index of selected process
            int bestPriority = 1e9; // "Largest" possible priority for comparison

            // 3. Find the highest-priority process that has arrived
            for (int i = 0; i < n; i++) {
                if (processes[i].RT > 0 && processes[i].AT <= time) {
                    // If this process has a *lower* priority number => higher priority
                    if (processes[i].priority < bestPriority) {
                        bestPriority = processes[i].priority;
                        idx = i;
                    }
                    // Tie-breaker: If priority is the same, pick the one with earlier arrival
                    else if (processes[i].priority == bestPriority) {
                        if (processes[i].AT < processes[idx].AT) {
                            idx = i;
                        }
                    }
                }
            }

            // 4. If no process is ready yet, just move the time forward
            if (idx == -1) {
                time++;
            }
            else {
                // Record the start time
                int startTime = time;

                // "Run" the process to completion
                time += processes[idx].BT;
                processes[idx].RT = 0;  // Mark as completed
                processes[idx].FinishTime = time;
                completed++;

                // Save this segment to our Gantt structure
                gantt.push_back({ processes[idx].pid, {startTime, time} });
            }
        }

        // 5. Compute Turnaround Time and Waiting Time
        for (auto &p : processes) {
            p.TAT = p.FinishTime - p.AT;
            p.WT  = p.TAT - p.BT;
        }
    }

    // Print a simple Gantt chart before printing the table
    void printGanttChart() {
        cout << "\n===== Gantt Chart =====\n";

        // First line: process labels
        for (auto &entry : gantt) {
            cout << "|" << entry.first << "";
        }
        cout << "|\n";

        // Second line: time markers
        // The first time always starts at 0 or the earliest start in the Gantt
        // so we’ll print each segment's start time and the final end time
        cout << gantt.front().second.first << " "; 
        for (auto &entry : gantt) {
            cout << entry.second.second << " ";
        }
        cout << "\n=======================\n\n";
    }

    // Print results in a table
    void printResults() {
        cout << "PID\tArrival\tBurst\tPriority\tCompletion\tTurnaround\tWaiting\n";
        double total_TAT = 0;
        double total_WT = 0;

        for (auto &p : processes) {
            total_TAT += p.TAT;
            total_WT  += p.WT;

            cout << p.pid << "\t"
                 << p.AT << "\t"
                 << p.BT << "\t"
                 << p.priority << "\t\t"
                 << p.FinishTime << "\t\t"
                 << p.TAT << "\t\t"
                 << p.WT << "\n";
        }

        cout << "\nAverage Turnaround Time: " << (total_TAT / processes.size()) << "\n";
        cout << "Average Waiting Time   : " << (total_WT / processes.size()) << "\n";
    }
};

int main() {
    Scheduler scheduler;
    int n;
    do {
    cout << "Enter the number of processes [3-10]: ";
    cin >> n;
    }while(n < 3 || n > 10);

    for (int i = 0; i < n; i++) {
        cout << "\nEnter details for Process " << i + 1 << ":\n";
        string pid = "P" + to_string(i + 1);
        int AT, BT, priority;
        cout << "Arrival Time: ";
        cin >> AT;
        cout << "Burst Time: ";
        cin >> BT;
        cout << "Priority (lower = higher priority): ";
        cin >> priority;
        scheduler.addProcess(pid, AT, BT, priority);
    }

    scheduler.nonPreemptivePriorityScheduling();

    // Print Gantt chart BEFORE final table
    scheduler.printGanttChart();

    // Now print the table of results
    scheduler.printResults();

    return 0;
}