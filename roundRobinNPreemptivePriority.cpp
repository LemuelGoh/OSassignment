#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <queue>

using namespace std;

namespace rr
{
    class Process
    {
    private:
        int AT;
        int BT;
        int oriBT;
        int Priority;
        int FinishTime;
        bool Ready = false;

    public:
        static int Quantum;
        static int totalBt;
        static int highestAt;
        Process() {};
        Process(int at, int bt, int priority)
        {
            AT = at;
            BT = bt;
            oriBT = bt;
            Priority = priority;
        }
        void setReady()
        {
            Ready = true;
        }
        bool ready() const
        {
            return Ready;
        }
        int getAT() const
        {
            return AT;
        }
        void setBT(int newBt)
        {
            BT = newBt;
        }
        int getBT() const
        {
            return BT;
        }
        int getOriBT() const
        {
            return oriBT;
        }
        void setFinishTime(int time)
        {
            FinishTime = time;
        }
        int getFinishTime() const
        {
            return FinishTime;
        }
        int getPriority()
        {
            return Priority;
        }
    };

    int Process::totalBt = 0;
    int Process::Quantum = 0;
    int Process::highestAt = -2147483647 - 1;

    void rrProcessInfoEnquiry(Process processes[], int numProcess)
    {
        int at, bt, priority, totalBt = 0;
        for (int i = 0; i < numProcess; i++)
        {
            cout << "Process " << i << ':' << endl;
            cout << "Arrival Time: ";
            cin >> at;
            if (at > processes->highestAt)
                processes->highestAt = at;

            cout << "Burst Time: ";
            cin >> bt;

            cout << "Priority: ";
            cin >> priority;
            Process Other(at, bt, priority);
            cout << endl;
            processes[i] = Other;
        }
        processes->totalBt = totalBt;
    }
}

void rrMain()
{
    // getInput
    int numProcess, quantum;
    do
    {
        cout << "How many Processes [3-10]: ";
        cin >> numProcess;
        if (numProcess < 3 || numProcess > 10)
        {
            cout << "Please Enter Valid Amount -> 3 to 10" << endl;
        }
    } while (numProcess < 3 || numProcess > 10);
    cout << "Time Quantum: ";
    cin >> quantum;
    rr::Process *processes = new rr::Process[numProcess];
    processes->Quantum = quantum; // set quantum

    rrProcessInfoEnquiry(processes, numProcess); // set bt at & totalBt
    //

    queue<int> waitingQueue;
    vector<string> ganttChart;
    vector<int> timeFrame;
    bool allPReady = false;
    int time = 0;
    // load processes with Arrivaltime = 0;
    for (int i = 0; i < numProcess; i++)
    {
        if (processes[i].getAT() == 0)
        {
            waitingQueue.push(i);
            processes[i].setReady();
        }
    }
    //---------------------------

    while (!waitingQueue.empty())
    {
        ganttChart.push_back("P" + to_string(waitingQueue.front()));
        if (processes[waitingQueue.front()].getBT() <= processes->Quantum)
        {                                                    // if bt of the process is less than quantum, do only bt amount
            time += processes[waitingQueue.front()].getBT(); // instead of blindly do quantum time amount.
            processes[waitingQueue.front()].setBT(0);
        }
        else
        {
            time += processes->Quantum;
            processes[waitingQueue.front()].setBT(processes[waitingQueue.front()].getBT() - processes->Quantum);
        }

        timeFrame.push_back(time);

        // find which process is ready after the time increased
        if (!allPReady)
        {

            for (int i = 1; i <= time; i++)
            {
                for (int y = 0; y < numProcess; y++)
                {
                    if (processes[y].getAT() == i && !processes[y].ready())
                    {
                        waitingQueue.push(y);
                        processes[y].setReady();
                    }
                }
            }

            if (time >= processes->highestAt)
            {
                allPReady = true;
            }
        }

        // pop process and find whether need push
        if (processes[waitingQueue.front()].getBT() == 0)
        {
            processes[waitingQueue.front()].setFinishTime(time);
            waitingQueue.pop();
        }
        else
        {
            waitingQueue.push(waitingQueue.front());
            waitingQueue.pop();
        }
    }

    // generate gantt chart
    for (int i = 0; i < ganttChart.size(); i++) // top part
    {
        cout << "____";
    }
    cout << endl;
    for (int i = 0; i < ganttChart.size(); i++) // display processes part
    {
        cout << ganttChart[i] << " |";
    }
    cout << endl; // time
    cout << "0  ";
    for (int i = 0; i < ganttChart.size(); i++) // display time part
    {
        if (timeFrame[i] < 10)
        {
            cout << timeFrame[i] << "   ";
        }
        else if (timeFrame[i] < 100)
        {
            cout << timeFrame[i] << "  ";
        }
        else if (timeFrame[i] < 1000)
        {
            cout << timeFrame[i] << " ";
        }
    }
    //---------------------
    cout << "\n\n";
    // display table
    cout << "   |" << "Arrival Time | Burst Time | Priority | Finish Time | Turnaround Time | Waiting Time" << endl;
    for (int i = 0; i < numProcess; i++)
    {
        cout << 'P' << i << " |  " << processes[i].getAT() << "          |   " << processes[i].getOriBT() << "        |   " << processes[i].getPriority() << "      |   " << processes[i].getFinishTime() << "         |   " << processes[i].getFinishTime() - processes[i].getAT() << "             |   " << (processes[i].getFinishTime() - processes[i].getAT()) - processes[i].getOriBT();
        cout << endl;
    }
    delete[] processes;
}
//-------------------
namespace pPriority
{
    class Process
    {
    public:
        string pid;
        int AT;
        int BT;
        int RT;
        int priority;
        int FinishTime;
        int TAT;
        int WT;

        Process(string id, int at, int bt, int pr)
        {
            pid = id;
            AT = at;
            BT = bt;
            RT = bt;
            priority = pr;
            FinishTime = 0;
            TAT = 0;
            WT = 0;
        }
    };

    class Scheduler
    {
    private:
        vector<Process> processes;
        vector<string> GCprocesses;
        vector<int> GCtimestamps; // Store timestamps for Gantt Chart

        Process *selectProcess(int current_time)
        {
            Process *selected = nullptr;
            for (auto &process : processes)
            {
                if (process.AT <= current_time && process.RT > 0)
                {
                    if (!selected || process.priority < selected->priority ||
                        (process.priority == selected->priority && process.AT < selected->AT))
                    {
                        selected = &process;
                    }
                }
            }
            return selected;
        }

    public:
        void addProcess(string id, int AT, int BT, int priority)
        {
            processes.emplace_back(id, AT, BT, priority);
        }

        void preemptivePriorityScheduling()
        {
            int time = 0;
            int completed = 0;
            int n = processes.size();

            while (completed != n)
            {
                Process *current_process = selectProcess(time);

                if (!current_process)
                {
                    GCprocesses.push_back("Idle");
                    GCtimestamps.push_back(time);
                    time++;
                    continue;
                }

                GCprocesses.push_back(current_process->pid);
                GCtimestamps.push_back(time);
                current_process->RT--;
                time++;

                if (current_process->RT == 0)
                {
                    completed++;
                    current_process->FinishTime = time;
                }
            }
            GCtimestamps.push_back(time); // Mark the final time

            for (auto &process : processes)
            {
                process.TAT = process.FinishTime - process.AT;
                process.WT = process.TAT - process.BT;
            }
        }

        void printResults()
        {
            // Print Gantt Chart
            cout << "\nGantt Chart:\n";
            for (const auto &step : GCprocesses)
            {
                cout << "| " << step << " ";
            }
            cout << "|\n";
            for (const auto &timestamp : GCtimestamps)
            {
                if (timestamp < 10)
                {
                    cout << timestamp << "    ";
                }
                else
                    cout << timestamp << "   ";
            }
            cout << "\n";

            // Print process details
            cout << "\nProcess detail:\n";
            cout << left << setw(8) << "PID" << setw(8) << "Arrival" << setw(8) << "Burst"
                 << setw(12) << "Priority" << setw(12) << "Completion" << setw(12) << "Turnaround"
                 << setw(8) << "Waiting" << "\n";
            double total_TAT = 0;
            double total_WT = 0;

            for (const auto &process : processes)
            {
                total_TAT += process.TAT;
                total_WT += process.WT;
                cout << left << setw(8) << process.pid << setw(8) << process.AT
                     << setw(8) << process.BT << setw(12) << process.priority
                     << setw(12) << process.FinishTime << setw(12) << process.TAT
                     << setw(8) << process.WT << "\n";
            }

            cout << "\nAverage Turnaround Time: " << total_TAT / processes.size() << "\n";
            cout << "Average Waiting Time: " << total_WT / processes.size() << "\n";
        }
    };
}
void pPriorityMain()
{
    pPriority::Scheduler scheduler;
    int n;
    do
    {
        cout << "Enter the number of processes [3-10]: ";
        cin >> n;
        if (n < 3 || n > 10)
        {
            cout << "Please Enter Valid Amount -> 3 to 10" << endl;
        }
    } while (n < 3 || n > 10);

        for (int i = 0; i < n; i++)
    {
        cout << "\nEnter details for Process " << i + 1 << ":\n";
        string pid = "P" + to_string(i + 1);
        int AT, BT, priority;
        cout << "Arrival Time: ";
        cin >> AT;
        cout << "Burst Time: ";
        cin >> BT;
        cout << "Priority (lower number means higher priority): ";
        cin >> priority;
        scheduler.addProcess(pid, AT, BT, priority);
    }

    scheduler.preemptivePriorityScheduling();
    scheduler.printResults();
}
//--------------------------
int main()
{
    int choose;
    do {
        cout << "Choose a scheduling algorithm" <<endl;
        cout << "Enter 1 for Round Robin Scheduling" << endl;
        cout << "Enter 2 for Preemptive Priority" << endl;
    } while (choose < 1 || choose > 2);
    switch (choose)
    {
    case 1:
        rrMain();
        break;
    case 2:
        pPriorityMain();
        break;
    }
    system("pause");
}