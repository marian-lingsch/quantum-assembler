from src.instructions.arguments.any_of import AnyOf
from src.instructions.arguments.argument_interface import Argument
from src.instructions.arguments.cell import Cell
from src.instructions.arguments.value import Value
from src.instructions.instruction_interface import Instruction


class InstructionSqrt(Instruction):

    def __init__(self, arg1, cell):
        self.arg1 = arg1
        self.cell = cell
        self.amount_ancilliary = Instruction.size_of_binary_int

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()

        if string_no_spaces[0:5].lower() != "sqrt ":
            return None

        split_instruction = string_no_spaces.split(" ")

        arg1 = AnyOf([Cell, Value]).parse(split_instruction[1])
        cell = Cell.parse(split_instruction[2])

        return InstructionSqrt(arg1, cell)

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
        return InstructionSqrt(arg1, cell)

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        any_of = AnyOf([Cell, Value])
        int_value_cell1 = any_of.as_int_sql_statement(self.arg1, program)

        int_value_cell_3 = " sqrt(" + int_value_cell1 + ") "
        binary_value_cell_3 = " , ".join(
            "q{0} = CAST({1} as INTEGER)".format(
                program.start_data + self.cell.cell * Instruction.size_of_binary_int + i,
                "((" + int_value_cell_3 + ")/{0} ) % {1}".format(2 ** i, 2)) for i in
            range(Instruction.size_of_binary_int))

        # Update the result
        update_statement = "update " + tablename + " set " + binary_value_cell_3 + " WHERE " + \
                           Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
                           Instruction.get_instruction_mask(program, int_program_counter,
                                                            binary_instruction) + ";"

        return update_statement

    def update_program_counter(self):
        return True

    def __eq__(self, other):
        if not isinstance(other, InstructionSqrt):
            return False
        return other.arg1 == self.arg1 and other.cell == self.cell

    def __repr__(self):
        return "SQRT " + str(self.arg1) + " " + str(self.cell)
