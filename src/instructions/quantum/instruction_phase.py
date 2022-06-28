from src.instructions.instruction_interface import Instruction


class InstructionPhase(Instruction):

    def __init__(self, re, im):
        super().__init__()
        self.re = re
        self.im = im
        assert abs((self.re) ** 2 + (self.im ** 2) - 1) < 1e-9

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()
        if string_no_spaces[0:6].lower() != "phase ":
            return None

        split_instruction = string_no_spaces.split(" ")

        try:
            re = float(split_instruction[1])
            im = float(split_instruction[2])
        except:
            return None

        return InstructionPhase(re, im)

    def data_cells_accesed(self):
        return []

    def amnt_ancilliary_qubits(self):
        return 0

    def to_binary(self):
        return self.float_to_binary(self.re) + self.float_to_binary(self.im)

    @staticmethod
    def from_binary(binary_representation):
        im = Instruction.binary_to_float(binary_representation[-Instruction.size_of_binary_float:])
        re = Instruction.binary_to_float(
            binary_representation[-2 * Instruction.size_of_binary_float:-Instruction.size_of_binary_float])
        return InstructionPhase(re, im)

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        query = "update {0} set revalue = {1}*revalue - {2}*imvalue, imvalue = {1}*imvalue + {2}*revalue where ".format(
            tablename, self.re, self.im) + Instruction.get_program_counter_mask(program,
                                                                                binary_program_counter) + " and " + \
                Instruction.get_instruction_mask(program, int_program_counter, binary_instruction)
        return query

    def update_program_counter(self):
        return True

    def __eq__(self, other):
        if not isinstance(other, InstructionPhase):
            return False
        return True

    def __repr__(self):
        return "PHASE " + str(self.re) + " " + str(self.im)
