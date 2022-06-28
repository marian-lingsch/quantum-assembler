from src.instructions.arguments.cell import Cell
from src.instructions.arguments.value import Value
from src.instructions.instruction_interface import Instruction


class InstructionSetData(Instruction):

    def __init__(self, data_cell, value):
        super().__init__()
        self.data_cell = data_cell
        self.value = value

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()
        if string_no_spaces[0:4].lower() != "set ":
            return None

        split_instruction = string_no_spaces.split(" ")

        cell = Cell.parse(split_instruction[1])
        if cell is None:
            return None

        value = Value.parse(split_instruction[2])
        if value is None:
            return None

        return InstructionSetData(cell.cell, value.value)

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        binary_value = Instruction.int_to_binary(self.value)
        return "update " + tablename + " set " + " , ".join([
            "q{0} = {1}".format(program.start_data + self.data_cell * Instruction.size_of_binary_int + t, v) for t, v in
            enumerate(binary_value)]) + " WHERE " + \
               Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
               Instruction.get_instruction_mask(program, int_program_counter, binary_instruction)

    def update_program_counter(self):
        return True

    def data_cells_accesed(self):
        return [self.data_cell]

    def amnt_ancilliary_qubits(self):
        return 0

    def to_binary(self):
        return self.int_to_binary(self.data_cell) + self.int_to_binary(self.value)

    @staticmethod
    def from_binary(binary_representation):
        value = Instruction.binary_to_int(binary_representation[-Instruction.size_of_binary_int:])
        data_cell = Instruction.binary_to_int(
            binary_representation[-2 * Instruction.size_of_binary_int:-Instruction.size_of_binary_int])
        return InstructionSetData(data_cell, value)

    def __eq__(self, other):
        if not isinstance(other, InstructionSetData):
            return False
        return other.data_cell == self.data_cell and other.value == self.value

    def __repr__(self):
        return "SET d" + str(self.data_cell) + " " + str(self.value)
