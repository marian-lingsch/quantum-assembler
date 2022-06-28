import numpy as np

from src.instructions.instruction_interface import Instruction


class InstructionHavocDataBit(Instruction):

    def __init__(self, data_bit):
        super().__init__()
        self.data_bit = data_bit

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()
        if string_no_spaces[0:7].lower() != "havocb ":
            return None

        split_instruction = string_no_spaces.split(" ")

        if not split_instruction[1].isnumeric():
            return None

        data_bit = int(split_instruction[1])

        return InstructionHavocDataBit(data_bit)

    def data_cells_accesed(self):
        return [self.data_bit // Instruction.size_of_binary_int]

    def amnt_ancilliary_qubits(self):
        return 0

    def to_binary(self):
        return self.int_to_binary(self.data_bit)

    @staticmethod
    def from_binary(binary_representation):
        data_bit = Instruction.binary_to_int(binary_representation[-Instruction.size_of_binary_int:])
        return InstructionHavocDataBit(data_bit)

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        query0 = "Select " + ", ".join(
            ["q" + str(_t) if _t != program.start_data + self.data_bit else "0 as q" + str(_t) for _t in
             range(program.amnt_qubits)]) + ", revalue*{0} as revalue, imvalue*{0}  as imvalue".format(
            np.sqrt(0.5)) + " FROM " + tablename + " WHERE " + \
                 Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
                 Instruction.get_instruction_mask(program, int_program_counter, binary_instruction)

        query1 = "Select " + ", ".join(
            ["q" + str(_t) if _t != program.start_data + self.data_bit else "1 as q" + str(_t) for _t in
             range(
                 program.amnt_qubits)]) + ", revalue*{0}*(1 - {1}) - revalue*{0}*{1} as revalue, imvalue*{0}*(1 - {1}) - imvalue*{0}*{1}  as imvalue".format(
            np.sqrt(0.5), "q" + str(program.start_data + self.data_bit)) + " FROM " + tablename + " WHERE " + \
                 Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
                 Instruction.get_instruction_mask(program, int_program_counter, binary_instruction)

        new_values = "Select " + ", ".join(["q" + str(t) for t in range(program.amnt_qubits)]) + \
                     ", sum(revalue) as revalue, sum(imvalue) as imvalue FROM (" + query0 + " union all " + query1 + ") GROUP BY " + ", ".join(
            ["q" + str(_t) for _t in range(program.amnt_qubits)])

        update_query = "replace into quantumstate (" + ", ".join(
            ["q" + str(_t) for _t in range(
                program.amnt_qubits)]) + ", revalue, imvalue) " + new_values

        return update_query

    def update_program_counter(self):
        return True

    def __eq__(self, other):
        if not isinstance(other, InstructionHavocDataBit):
            return False
        return other.data_bit == self.data_bit

    def __repr__(self):
        return "HavocB " + str(self.data_bit)
