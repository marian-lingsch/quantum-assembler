from src.instructions.instruction_interface import Instruction


class InstructionStop(Instruction):

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()
        if string_no_spaces[0:4].lower() != "stop":
            return None

        return InstructionStop()

    def data_cells_accesed(self):
        return []

    def amnt_ancilliary_qubits(self):
        return 0

    def to_binary(self):
        return []

    @staticmethod
    def from_binary(binary_representation):
        return InstructionStop()

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        return ""

    def update_program_counter(self):
        return False

    def __eq__(self, other):
        return isinstance(other, InstructionStop)

    def __repr__(self):
        return "STOP"
