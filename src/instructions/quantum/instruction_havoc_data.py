from src.instructions.instruction_interface import Instruction
from src.instructions.quantum.instruction_havoc_data_bit import InstructionHavocDataBit


class InstructionHavocData(Instruction):

    def __init__(self, cell, lower_range, upper_range):
        super().__init__()
        self.cell = cell
        self.lower_range = lower_range
        self.upper_range = upper_range

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()
        if string_no_spaces[0:6].lower() != "havoc ":
            return None

        split_instruction = string_no_spaces.split(" ")

        if not (split_instruction[2].isnumeric() and split_instruction[3].isnumeric()):
            return None

        lower_range = int(split_instruction[2])
        upper_range = int(split_instruction[3])
        if split_instruction[1][0] != "d" or not split_instruction[1][1:].isnumeric():
            return None

        data_cell_position = int(split_instruction[1][1:])
        return InstructionHavocData(data_cell_position, lower_range, upper_range)

    def data_cells_accesed(self):
        return [self.cell]

    def amnt_ancilliary_qubits(self):
        return 0

    def to_binary(self):
        return self.int_to_binary(self.upper_range) + self.int_to_binary(self.lower_range) + self.int_to_binary(
            self.cell)

    @staticmethod
    def from_binary(binary_representation):
        cell = Instruction.binary_to_int(binary_representation[-Instruction.size_of_binary_int:])
        lower_range = Instruction.binary_to_int(
            binary_representation[-2 * Instruction.size_of_binary_int:-Instruction.size_of_binary_int])
        upper_range = Instruction.binary_to_int(
            binary_representation[-3 * Instruction.size_of_binary_int:-2 * Instruction.size_of_binary_int])
        return InstructionHavocData(cell, lower_range, upper_range)

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        query = ""
        for i in range(self.lower_range, self.upper_range):
            bit = self.cell * Instruction.size_of_binary_int + i
            query += InstructionHavocDataBit(bit).update_db_sql_statement(tablename, binary_program_counter,
                                                                          int_program_counter, binary_instruction,
                                                                          program) + ";"
        return query

    def update_program_counter(self):
        return True

    def __eq__(self, other):
        if not isinstance(other, InstructionHavocData):
            return False
        return other.cell == self.cell and other.lower_range == self.lower_range and other.upper_range == self.upper_range

    def __repr__(self):
        return "HAVOC " + "d" + str(self.cell) + " " + str(self.lower_range) + " " + str(self.upper_range)
