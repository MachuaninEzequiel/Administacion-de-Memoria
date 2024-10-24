class Process:
    def __init__(self, process_id, size):
        self.process_id = process_id
        self.size = size
        self.allocated = False
        self.start_address = None
        self.end_address = None


class MemorySimulator:
    def __init__(self, memory_size):
        self.memory_size = memory_size
        self.memory = [None] * memory_size
        self.processes = []
        self.allocations = []

    def add_process(self, process_id, size):
        process = Process(process_id, size)
        self.processes.append(process)

    def allocate_processes(self):
        self.processes.sort(key=lambda x: x.size, reverse=True)  # Ordenar procesos de mayor a menor tamaño
        self.backtracking(0)
        return self.allocations

    def backtracking(self, process_index):
        if process_index >= len(self.processes):
            allocation = []
            for process in self.processes:
                if process.allocated:
                    allocation.append((process.process_id, process.start_address, process.end_address))
            self.allocations.append(allocation)
            return

        process = self.processes[process_index]
        for i in range(self.memory_size - process.size + 1):
            if self.is_valid_position(i, process.size):
                self.assign_process(i, process.size, process)
                self.backtracking(process_index + 1)
                self.unassign_process(i, process.size, process)

    def is_valid_position(self, start_address, size):
        for i in range(start_address, start_address + size):
            if self.memory[i] is not None:
                return False
        return True

    def assign_process(self, start_address, size, process):
        process.allocated = True
        process.start_address = start_address
        process.end_address = start_address + size - 1
        for i in range(start_address, start_address + size):
            self.memory[i] = process

    def unassign_process(self, start_address, size, process):
        process.allocated = False
        process.start_address = None
        process.end_address = None
        for i in range(start_address, start_address + size):
            self.memory[i] = None


# Ejemplo de uso
memory_size = 100
simulator = MemorySimulator(memory_size)

simulator.add_process(1, 20)


allocations = simulator.allocate_processes()

for allocation in allocations:
    print("Allocation:")
    for process_id, start_address, end_address in allocation:
        print(f"Process {process_id}: Allocated from address {start_address} to {end_address}")
    print()
