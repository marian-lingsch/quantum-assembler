from src.instructions.arguments.argument_interface import Argument
from src.instructions.instruction_interface import Instruction


class Value(Argument):

    def __init__(self, value):
        self.value = value

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()
        if not string_no_spaces.isnumeric():
            return None

        return Value(int(string_no_spaces))

    def data_cells_accesed(self):
        return []

    def to_binary(self):
        return Argument.value_binary_mask + Instruction.int_to_binary(self.value)

    @staticmethod
    def from_binary(arg):
        return Value(Instruction.binary_to_int(arg))

    def as_int_sql_statement(self, program):
        return str(self.value)

    def __eq__(self, other):
        if not isinstance(other, Value):
            return False
        return self.value == other.value

    def __repr__(self):
        return str(self.value)
