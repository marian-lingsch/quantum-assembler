from src.instructions.instruction_interface import Instruction


class InstructionSkip(Instruction):

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()
        if string_no_spaces[0:4].lower() != "skip":
            return None

        return InstructionSkip()

    def data_cells_accesed(self):
        return []

    def amnt_ancilliary_qubits(self):
        return 0

    def to_binary(self):
        return []

    @staticmethod
    def from_binary(binary_representation):
        return InstructionSkip()

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        return ""

    def update_program_counter(self):
        return True

    def __eq__(self, other):
        return isinstance(other, InstructionSkip)

    def __repr__(self):
        return "SKIP"
