import math

from src import utils


class Program:

    def __init__(self, instructions):
        self.instructions = instructions
        self.data_cell_size = 8
        self.instructions_to_id = self.assign_id_to_instruction()
        self.id_to_instruction = {v: k for k, v in self.instructions_to_id.items()}
        self.size_of_instruction_ids = math.floor(math.log(max(self.id_to_instruction.keys()) + 1, 2)) + 1
        self.data_size = self.get_data_size()
        self.instruction_size = self.get_instruction_size()
        self.anciliary_qubits = self.get_ancilliary_qubits()
        self.program_counter_size = math.ceil(math.log(len(instructions), 2)) + 4
        self.program_size = len(self.instructions) * self.instruction_size
        self.start_data = self.program_counter_size + self.program_size + self.anciliary_qubits
        self.amnt_qubits = self.program_counter_size + self.program_size + \
                           self.data_size + self.anciliary_qubits

    def get_ancilliary_qubits(self):
        return max([ins.amnt_ancilliary_qubits() for ins in self.instructions])

    def get_data_size(self):
        return max([max(ins.data_cells_accesed() + [0]) + 1 for ins in self.instructions]) * self.data_cell_size

    def get_instruction_size(self):
        return max([len(ins.to_binary()) + self.size_of_instruction_ids for ins in self.instructions])

    def assign_id_to_instruction(self):
        instructions_to_id = {}
        counter = 0
        for ins in self.instructions:
            if ins.__class__ not in instructions_to_id.keys():
                instructions_to_id[ins.__class__] = counter
                counter += 1
        return instructions_to_id

    def program_counter_to_binary(self, pc):
        result = utils.int_to_binary(pc)
        result_correct_size = [0] * self.program_counter_size
        # TODO check if result has the correct size
        for i, value in enumerate(result):
            result_correct_size[i] = value
        return result

    def binary_program_counter_to_int(self, pc):
        return utils.binary_to_int(pc)

    def binary_to_int(self, binary_value):
        return utils.binary_to_int(binary_value)

    def int_to_binary(self, int_value):
        return utils.int_to_binary(int_value)

    def as_binary(self):
        binary_representations = []
        for ins in self.instructions:
            binary_ins = ins.to_binary()
            binary_id = self.int_to_binary(self.instructions_to_id[ins.__class__])
            binary_id = binary_id + [0] * max(self.size_of_instruction_ids - len(binary_id), 0)
            binary_representations += binary_id + [0] * (
                    self.instruction_size - len(binary_ins) - len(binary_id)) + binary_ins
        return binary_representations

    def __eq__(self, other):
        if not isinstance(other, Program):
            return False
        return other.instructions == self.instructions

# TODO
## Vergleich von Sieb des erathostenes klasisch und quantum
## Latex Listings vorbereiten
