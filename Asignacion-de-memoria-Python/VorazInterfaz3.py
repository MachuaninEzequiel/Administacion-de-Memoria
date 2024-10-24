import tkinter as tk
from tkinter import messagebox

class Process:
    def __init__(self, process_id, size, execution_time):
        self.process_id = process_id
        self.size = size
        self.execution_time = execution_time
        self.allocated = False
        self.start_address = None
        self.end_address = None


class MemorySimulator:
    def __init__(self, memory_size):
        self.memory_size = memory_size
        self.memory = [None] * memory_size
        self.processes = []

    def add_process(self, processes):
        for process in processes:
            self.processes.append(process)

    def allocate_processes(self):
        self.processes.sort(key=lambda x: x.size / x.execution_time, reverse=True)
        for process in self.processes:
            if process.size / process.execution_time < 0.2:
                continue

            start_address = self.find_free_block(process.size)
            if start_address is not None:
                end_address = start_address + process.size - 1
                process.allocated = True
                process.start_address = start_address
                process.end_address = end_address
                self.update_memory(start_address, end_address)

    def find_free_block(self, size):
        start_address = None
        count = 0
        for i in range(1, self.memory_size + 1):
            if self.memory[i - 1] is None:
                if start_address is None:
                    start_address = i
                count += 1
                if count == size:
                    return start_address
            else:
                start_address = None
                count = 0
        return None

    def update_memory(self, start_address, end_address):
        for i in range(start_address, end_address + 1):
            self.memory[i - 1] = True

    def get_allocation(self):
        allocation = []
        for process in self.processes:
            if process.allocated:
                allocation.append(f"Process {process.process_id}: Allocated from address {process.start_address} to {process.end_address}")
            else:
                allocation.append(f"Process {process.process_id}: Not allocated")
        return allocation


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Simulator")
        self.geometry("600x400")
        self.memory_size_entry = None
        self.processes_entry = None
        self.memory_simulator = None
        self.allocation_text = None

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

        self.allocation_text = tk.Text(self, height=10, width=50)
        self.allocation_text.pack()

    def simulate(self):
        memory_size = int(self.memory_size_entry.get())
        processes_str = self.processes_entry.get("1.0", "end-1c")
        processes = self.parse_processes(processes_str)

        if processes:
            self.memory_simulator = MemorySimulator(memory_size)
            self.memory_simulator.add_process(processes)
            self.memory_simulator.allocate_processes()
            allocation = self.memory_simulator.get_allocation()
            self.display_allocation(allocation)
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

    def display_allocation(self, allocation):
        self.allocation_text.delete("1.0", "end")
        self.allocation_text.insert("1.0", "\n".join(allocation))


if __name__ == "__main__":
    app = Application()
    app.mainloop()
