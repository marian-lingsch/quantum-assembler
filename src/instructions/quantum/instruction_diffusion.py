from src.instructions.instruction_interface import Instruction


class InstructionDiffusion(Instruction):

    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()

        if string_no_spaces.lower() != "diffusion":
            return None

        return InstructionDiffusion()

    def data_cells_accesed(self):
        return []

    def amnt_ancilliary_qubits(self):
        return 0

    def to_binary(self):
        return []

    @staticmethod
    def from_binary(binary_representation):
        return InstructionDiffusion()

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        query = "update {0} set revalue = -revalue + (Select 2.0*avg(revalue) FROM {0}), imvalue = -imvalue + (Select 2.0*avg(imvalue) FROM {0}) where ".format(
            tablename) + Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
                Instruction.get_instruction_mask(program, int_program_counter, binary_instruction)
        return query

    def update_program_counter(self):
        return True

    def __eq__(self, other):
        if not isinstance(other, InstructionDiffusion):
            return False
        return True

    def __repr__(self):
        return "DIFFUSION"
