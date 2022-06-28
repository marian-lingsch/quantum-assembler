from src.instructions.arguments.argument_interface import Argument


class Label(Argument):

    @staticmethod
    def parse(string):
        pass

    def data_cells_accesed(self):
        pass

    def to_binary(self):
        pass

    def as_int_sql_statement(self, program):
        pass

    def __eq__(self, other):
        pass

    def __repr__(self):
        pass
