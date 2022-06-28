from src.instructions.arguments.any_of import AnyOf
from src.instructions.arguments.argument_interface import Argument
from src.instructions.arguments.cell import Cell
from src.instructions.arguments.value import Value
from src.instructions.instruction_interface import Instruction


class InstructionNot(Instruction):

    def __init__(self, arg1, cell):
        self.arg1 = arg1
        self.cell = cell
        self.amount_ancilliary = Instruction.size_of_binary_int

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()

        if string_no_spaces[0:4].lower() != "not ":
            return None

        split_instruction = string_no_spaces.split(" ")
        arg1 = AnyOf([Cell, Value]).parse(split_instruction[1])
        cell = Cell.parse(split_instruction[2])

        return InstructionNot(arg1, cell)

    def data_cells_accesed(self):
        return self.arg1.data_cells_accesed() + self.cell.data_cells_accesed()

    def amnt_ancilliary_qubits(self):
        return self.amount_ancilliary

    def to_binary(self):
        return self.arg1.to_binary() + self.cell.to_binary()

    @staticmethod
    def from_binary(binary_representation):
        any_of = AnyOf([Cell, Value], [Argument.cell_binary_mask, Argument.value_binary_mask])
        cell = any_of.from_binary(binary_representation[-Instruction.cell_size:])
        arg1 = any_of.from_binary(
            binary_representation[-2 * Instruction.cell_size:-Instruction.cell_size])
        return InstructionNot(arg1, cell)

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        int_value_cell1 = AnyOf([Cell, Value]).as_int_sql_statement(self.arg1, program)

        value_cell_2 = "case when {0} > 0 then 0 else 1 end".format(int_value_cell1)
        binary_value_cell_3 = " , ".join(
            "q{0} = {1} ".format(program.start_data + self.cell.cell * Instruction.size_of_binary_int + i,
                                 "((" + value_cell_2 + ")/{0} ) % {1}".format(2 ** i, 2)) for i in
            range(Instruction.size_of_binary_int))
        return "update " + tablename + " set " + binary_value_cell_3 + " WHERE " + \
               Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
               Instruction.get_instruction_mask(program, int_program_counter, binary_instruction)

    def update_program_counter(self):
        return True

    def __eq__(self, other):
        if not isinstance(other, InstructionNot):
            return False
        return other.arg1 == self.arg1 and other.cell == self.cell

    def __repr__(self):
        return "NOT " + str(self.arg1) + " " + str(self.cell)
