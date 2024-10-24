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

    def print_allocation(self):
        for process in self.processes:
            if process.allocated:
                print(f"Process {process.process_id}: Allocated from address {process.start_address} to {process.end_address}")
            else:
                print(f"Process {process.process_id}: Not allocated")


# Ejemplo de uso
memory_size = 250
simulator = MemorySimulator(memory_size)

processes = [
    Process(1,75,11),
    Process(2,9,23),
    Process(3,94,11),
    Process(4,77,10),
    Process(5,11,20),
    Process(6,80,26),
    Process(7,97,8),
]

simulator.add_process(processes)
simulator.allocate_processes()
simulator.print_allocation()
