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

    def add_process(self, process):
        self.processes.append(process)

    def allocate_process(self, process):
        start_address = self.find_free_block(process.size)
        if start_address is not None:
            end_address = start_address + process.size - 1
            process.allocated = True
            process.start_address = start_address
            process.end_address = end_address
            self.update_memory(start_address, end_address)
            return True
        else:
            return False

    def find_free_block(self, size):
        start_address = None
        count = 0
        for i in range(self.memory_size):
            if self.memory[i] is None:
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
            self.memory[i] = True

    def get_allocation(self):
        allocation = []
        for process in self.processes:
            if process.allocated:
                allocation.append(f"Process {process.process_id}: Allocated from address {process.start_address} to {process.end_address}")
        return allocation


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Simulator")
        self.geometry("600x400")
        self.memory_size_entry = None
        self.processes_entry = None
        self.memory_simulator = None
        self.memory_canvas = None

        self.create_widgets()

    def create_widgets(self):
        memory_size_label = tk.Label(self, text="Memory Size:")
        memory_size_label.pack()
        self.memory_size_entry = tk.Entry(self)
        self.memory_size_entry.pack()

        processes_label = tk.Label(self, text="Processes (Format: Process ID, Size, Execution Time):")
        processes_label.pack()
        self.processes_entry = tk.Text(self, height=5, width=50)
        self.processes_entry.pack()

        simulate_button = tk.Button(self, text="Simulate", command=self.simulate)
        simulate_button.pack()

        self.memory_canvas = tk.Canvas(self, height=200, width=400, bg="white")
        self.memory_canvas.pack()

    def simulate(self):
        memory_size = int(self.memory_size_entry.get())
        processes_str = self.processes_entry.get("1.0", "end-1c")
        processes = self.parse_processes(processes_str)

        if processes:
            self.memory_simulator = MemorySimulator(memory_size)
            allocation = []
            for process in processes:
                allocated = self.memory_simulator.allocate_process(process)
                if allocated:
                    allocation.append(f"Process {process.process_id}: Allocated from address {process.start_address} to {process.end_address}")
            self.update_memory_visualization()
            if allocation:
                messagebox.showinfo("Memory Allocation", "\n".join(allocation))
            else:
                messagebox.showinfo("Memory Allocation", "No processes allocated.")
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

    def update_memory_visualization(self):
        self.memory_canvas.delete("all")
        memory_size = self.memory_simulator.memory_size
        memory = self.memory_simulator.memory

        rect_width = self.memory_canvas.winfo_width() / memory_size
        rect_height = self.memory_canvas.winfo_height()

        for i in range(memory_size):
            if memory[i]:
                color = "green"
            else:
                color = "red"

            x1 = i * rect_width
            y1 = 0
            x2 = (i + 1) * rect_width
            y2 = rect_height

            self.memory_canvas.create_rectangle(x1, y1, x2, y2, fill=color)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
