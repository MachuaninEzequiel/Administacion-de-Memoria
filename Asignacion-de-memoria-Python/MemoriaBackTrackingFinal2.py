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

    def print_combinations(self):
        for combination in self.combinations:
            total_size = sum([process.size for process in combination])
            total_processes = len(combination)
            if total_processes > 0:
                print("Combination (Total Size: {}):".format(total_size))
                for process in combination:
                    print("Process {}: Size: {}".format(process.process_id, process.size))
                individual_relations = [process.size / process.execution_time for process in combination]
                sum_individual_relations = sum(individual_relations)
                relation = total_size / (total_processes * sum_individual_relations)
                print("Relation: {:.2f}\n".format(relation))


# Ejemplo de uso
memory_size = 100
simulator = MemorySimulator(memory_size)

processes = [
    Process(1, 20, 5),
    Process(2, 30, 8),
    Process(3, 70, 10),
    Process(4, 32, 4),
    Process(5, 34, 6),
    Process(6, 10, 2),
    Process(7, 15, 3)
]

simulator.add_process(processes)

combinations = simulator.find_combinations()

simulator.print_combinations()
