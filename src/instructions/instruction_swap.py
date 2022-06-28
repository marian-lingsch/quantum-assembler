from src.instructions.instruction_interface import Instruction


class InstructionSwap(Instruction):

    def __init__(self, data_cell1, data_cell2):
        super().__init__()
        self.data_cell1 = data_cell1
        self.data_cell2 = data_cell2

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()

        if string_no_spaces[0:4].lower() != "swap":
            return None

        split_instruction = string_no_spaces.split(" ")
        if split_instruction[1][0] != "d" or not split_instruction[1][1:].isnumeric():
            return None

        cell1 = int(split_instruction[1][1:])
        if split_instruction[2][0] != "d" or not split_instruction[2][1:].isnumeric():
            return None

        cell2 = int(split_instruction[2][1:])
        return InstructionSwap(cell1, cell2)

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        return "update " + tablename + " set " + " , ".join([
            "q{0} = q{1} , q{1} = q{0}".format(
                program.start_data + self.data_cell1 * Instruction.size_of_binary_int + t,
                program.start_data + self.data_cell2 * Instruction.size_of_binary_int + t) for t in
            range(Instruction.size_of_binary_int)]) + " WHERE " + \
               Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
               Instruction.get_instruction_mask(program, int_program_counter, binary_instruction)

    def update_program_counter(self):
        return True

    def data_cells_accesed(self):
        return [self.data_cell1, self.data_cell2]

    def amnt_ancilliary_qubits(self):
        return 0

    def to_binary(self):
        return self.int_to_binary(self.data_cell1) + self.int_to_binary(self.data_cell2)

    @staticmethod
    def from_binary(binary_representation):
        data_cell1 = Instruction.binary_to_int(binary_representation[-Instruction.size_of_binary_int:])
        data_cell2 = Instruction.binary_to_int(
            binary_representation[-2 * Instruction.size_of_binary_int:-Instruction.size_of_binary_int])
        return InstructionSwap(data_cell1, data_cell2)

    def __eq__(self, other):
        if not isinstance(other, InstructionSwap):
            return False
        return other.data_cell1 == self.data_cell1 and other.data_cell2 == self.data_cell2

    def __repr__(self):
        return "SWAP " + str(self.data_cell1) + " " + str(self.data_cell2)
