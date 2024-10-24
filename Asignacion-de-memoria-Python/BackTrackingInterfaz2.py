import tkinter as tk
from tkinter import messagebox

class Process:
    def __init__(self, process_id, size, execution_time):
        self.process_id = process_id
        self.size = size
        self.execution_time = execution_time


class MemorySimulator:
    def __init__(self, memory_size):
        self.memory_size = memory_size
        self.processes = []
        self.combinations = []

    def add_process(self, processes):
        for process in processes:
            self.processes.append(process)

    def find_combinations(self):
        self.processes.sort(key=lambda x: x.size, reverse=True)
        current_combination = []
        self.backtracking(0, current_combination)
        return self.combinations

    def backtracking(self, process_index, current_combination):
        if process_index >= len(self.processes):
            total_size = sum([process.size for process in current_combination])
            if total_size <= self.memory_size:
                self.combinations.append(current_combination.copy())
            return

        process = self.processes[process_index]
        self.backtracking(process_index + 1, current_combination)
        current_combination.append(process)
        self.backtracking(process_index + 1, current_combination)
        current_combination.pop()

    def get_combinations_info(self):
        min_relation = float('inf')
        min_relation_index = -1
        info = []

        for i, combination in enumerate(self.combinations):
            total_size = sum([process.size for process in combination])
            total_processes = len(combination)
            marcador = 0

            if total_processes > 0:
                combination_info = f"Combination {i} (Total Size: {total_size}):\n"
                for process in combination:
                    combination_info += f"Process {process.process_id}: Size: {process.size}\n"
                individual_relations = [process.size / process.execution_time for process in combination]
                for j in range(len(individual_relations)):
                    if individual_relations[j] < 1:
                        marcador = 1

                sum_individual_relations = sum(individual_relations)

                if marcador == 1:
                    relation = total_size  / (total_processes * (sum_individual_relations / 2 ))
                else:
                    relation = total_size / (total_processes * sum_individual_relations)

                combination_info += f"Relation: {relation:.2f}\n\n"

                info.append(combination_info)

                if relation < min_relation:
                    min_relation = relation
                    min_relation_index = i

        info.append(f"Mejor combinacion de procesos: {min_relation_index}")
        return info


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Simulator")
        self.geometry("800x600")
        self.memory_size_entry = None
        self.processes_entry = None
        self.memory_simulator = None
        self.combinations_text = None

        self.create_widgets()

    def create_widgets(self):
        memory_size_label = tk.Label(self, text="Memory Size:")
        memory_size_label.pack()
        self.memory_size_entry = tk.Entry(self)
        self.memory_size_entry.pack()

        processes_label = tk.Label(
            self, text="Processes (Format: Process ID, Size, Execution Time):"
        )
        processes_label.pack()
        self.processes_entry = tk.Text(self, height=5, width=50)
        self.processes_entry.pack()

        simulate_button = tk.Button(self, text="Simulate", command=self.simulate)
        simulate_button.pack()

        self.combinations_text = tk.Text(self, height=25, width=80)
        self.combinations_text.pack()

    def simulate(self):
        memory_size = int(self.memory_size_entry.get())
        processes_str = self.processes_entry.get("1.0", "end-1c")
        processes = self.parse_processes(processes_str)

        if processes:
            self.memory_simulator = MemorySimulator(memory_size)
            self.memory_simulator.add_process(processes)
            combinations = self.memory_simulator.find_combinations()
            combinations_info = self.memory_simulator.get_combinations_info()
            self.display_combinations(combinations_info)
        else:
            messagebox.showerror("Input Error", "Invalid process format.")

    def parse_processes(self, processes_str):
        try:
            processes_data = processes_str.strip().split("\n")
            processes = []
            for process_data in processes_data:
                process_id, size, execution_time = map(int, process_data.split(","))
                process = Process(process_id, size, execution_time)
                processes.append(process)
            return processes
        except:
            return None

    def display_combinations(self, combinations_info):
        self.combinations_text.delete("1.0", "end")

        for i, combination_info in enumerate(combinations_info):
            if i % 2 == 0:
                self.combinations_text.tag_configure("odd_combination", justify="left")
                self.combinations_text.insert("end", combination_info, "odd_combination")
            else:
                self.combinations_text.tag_configure("even_combination", justify="right")
                self.combinations_text.insert("end", combination_info, "even_combination")

        self.combinations_text.insert("end", "\n")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
