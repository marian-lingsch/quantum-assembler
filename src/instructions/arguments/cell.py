from src.instructions.arguments.argument_interface import Argument
from src.instructions.instruction_interface import Instruction


class Cell(Argument):

    def __init__(self, cell):
        self.cell = cell

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()
        if string_no_spaces[0] != "d" or not string_no_spaces[1:].isnumeric():
            return None

        return Cell(int(string_no_spaces[1:]))

    def data_cells_accesed(self):
        return [self.cell]

    def to_binary(self):
        return Argument.cell_binary_mask + Instruction.int_to_binary(self.cell)

    @staticmethod
    def from_binary(arg):
        return Cell(Instruction.binary_to_int(arg))

    def as_int_sql_statement(self, program):
        return Instruction.statement_to_binary(self.cell, program)

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.cell == other.cell

    def __repr__(self):
        return "d" + str(self.cell)
