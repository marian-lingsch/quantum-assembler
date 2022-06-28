from src.instructions.arguments.any_of import AnyOf
from src.instructions.arguments.argument_interface import Argument
from src.instructions.arguments.cell import Cell
from src.instructions.arguments.value import Value
from src.instructions.instruction_interface import Instruction


class InstructionIfThenElse(Instruction):

    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()
        if string_no_spaces[0:5].lower() != "ifte ":
            return None

        split_instruction = string_no_spaces.split(" ")
        arg1 = AnyOf([Cell, Value]).parse(split_instruction[1])
        arg2 = AnyOf([Cell, Value]).parse(split_instruction[2])
        arg3 = AnyOf([Cell, Value]).parse(split_instruction[3])

        return InstructionIfThenElse(arg1, arg2, arg3)

    def data_cells_accesed(self):
        return self.arg1.data_cells_accesed() + self.arg2.data_cells_accesed() + self.arg3.data_cells_accesed()

    def amnt_ancilliary_qubits(self):
        return 0

    def to_binary(self):
        return self.arg1.to_binary() + self.arg2.to_binary() + self.arg3.to_binary()

    @staticmethod
    def from_binary(binary_representation):
        any_of = AnyOf([Cell, Value], [Argument.cell_binary_mask, Argument.value_binary_mask])
        arg3 = any_of.from_binary(binary_representation[-Instruction.cell_size:])
        arg2 = any_of.from_binary(
            binary_representation[-2 * Instruction.cell_size:-Instruction.cell_size])
        arg1 = any_of.from_binary(
            binary_representation[-3 * Instruction.cell_size:-2 * Instruction.cell_size])
        return InstructionIfThenElse(arg1, arg2, arg3)

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        int_value_cell1 = AnyOf([Cell, Value]).as_int_sql_statement(self.arg1, program)
        int_value_cell2 = AnyOf([Cell, Value]).as_int_sql_statement(self.arg2, program)
        int_value_cell3 = AnyOf([Cell, Value]).as_int_sql_statement(self.arg3, program)

        binary_value_new_pc = " , ".join(
            "q{0} = case when {1} > 0 then CAST({2} as INTEGER) else CAST({3} as INTEGER) end".format(
                i, int_value_cell1,
                "((" + int_value_cell2 + ")/{0} ) % {1}".format(2 ** i, 2),
                "((" + int_value_cell3 + ")/{0} ) % {1}".format(2 ** i, 2)) for i in
            range(Instruction.size_of_binary_int))
        return "update " + tablename + " set " + binary_value_new_pc + " WHERE " + \
               Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
               Instruction.get_instruction_mask(program, int_program_counter, binary_instruction)

    def update_program_counter(self):
        return False

    def __eq__(self, other):
        if not isinstance(other, InstructionIfThenElse):
            return False
        return other.arg1 == self.arg1 and other.arg2 == self.arg2 and other.arg3 == self.arg3

    def __repr__(self):
        return "IFTE " + str(self.arg1) + " " + str(self.arg2) + " " + str(self.arg3)
