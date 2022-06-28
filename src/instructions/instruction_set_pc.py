from src.instructions.instruction_interface import Instruction


class InstructionSetProgramCounter(Instruction):

    def __init__(self, cell):
        self.cell = cell

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()
        if string_no_spaces[0:6].lower() != "setpc ":
            return None

        split_instruction = string_no_spaces.split(" ")

        if split_instruction[1][0] != "d" or not split_instruction[1][1:].isnumeric():
            return None

        data_cell_position = int(split_instruction[1][1:])
        return InstructionSetProgramCounter(data_cell_position)

    def data_cells_accesed(self):
        return [self.cell]

    def amnt_ancilliary_qubits(self):
        return 0

    def to_binary(self):
        return self.int_to_binary(self.cell)

    @staticmethod
    def from_binary(binary_representation):
        cell = Instruction.binary_to_int(binary_representation[-Instruction.size_of_binary_int:])
        return InstructionSetProgramCounter(cell)

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        return "update " + tablename + " set " + " , ".join([
            "q{0} = q{1}".format(t, program.start_data + self.cell * Instruction.size_of_binary_int + t) for t in
            range(Instruction.size_of_binary_int)]) + " WHERE " + \
               Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
               Instruction.get_instruction_mask(program, int_program_counter, binary_instruction)

    def update_program_counter(self):
        return False

    def __eq__(self, other):
        if not isinstance(other, InstructionSetProgramCounter):
            return False
        return other.cell == self.cell

    def __repr__(self):
        return "SETPC d" + str(self.cell)
