from src.instructions.arguments.argument_interface import Argument


class AnyOf:

    def __init__(self, types, binary_masks=None):
        self.types = types
        self.binary_masks = binary_masks

    def parse(self, string):

        for t in self.types:
            result = t.parse(string)
            if result is not None:
                return result

        return None

    def from_binary(self, arg):
        if self.binary_masks is None:
            return None

        for i, e in enumerate(self.types):
            if self.binary_masks[i] == list(arg[0:Argument.mask_length]):
                return e.from_binary(arg[Argument.mask_length:])

    def as_int_sql_statement(self, arg, program):
        for e in self.types:
            if isinstance(arg, e):
                return arg.as_int_sql_statement(program)
