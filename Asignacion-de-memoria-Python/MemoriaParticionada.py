class Process:
    def __init__(self, process_id, size):
        self.process_id = process_id
        self.size = size
        self.allocated = False
        self.partition_id = None


class Partition:
    def __init__(self, partition_id, size):
        self.partition_id = partition_id
        self.size = size
        self.allocated = False
        self.process_id = None


class MemorySimulator:
    def __init__(self, partitions):
        self.partitions = partitions
        self.processes = []

    def add_process(self, process_id, size):
        process = Process(process_id, size)
        self.processes.append(process)

    def allocate_processes(self):
        for process in self.processes:
            for partition in self.partitions:
                if not partition.allocated and partition.size >= process.size:
                    partition.allocated = True
                    partition.process_id = process.process_id
                    process.allocated = True
                    process.partition_id = partition.partition_id
                    break

    def print_allocation(self):
        for partition in self.partitions:
            if partition.allocated:
                print(f"Partition {partition.partition_id}: Process {partition.process_id}")
            else:
                print(f"Partition {partition.partition_id}: Free")

# Ejemplo de uso
partitions = [Partition(1, 100), Partition(2, 200), Partition(3, 150)]
simulator = MemorySimulator(partitions)

simulator.add_process(1, 120)
simulator.add_process(2, 180)
simulator.add_process(3, 90)
simulator.add_process(4, 80)
simulator.add_process(5, 150)

simulator.allocate_processes()
simulator.print_allocation()





