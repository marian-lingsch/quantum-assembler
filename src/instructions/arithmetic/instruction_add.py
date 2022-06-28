from src.instructions.arguments.any_of import AnyOf
from src.instructions.arguments.argument_interface import Argument
from src.instructions.arguments.cell import Cell
from src.instructions.arguments.value import Value
from src.instructions.instruction_interface import Instruction


class InstructionAdd(Instruction):

    def __init__(self, arg1, arg2, cell):
        self.arg1 = arg1
        self.arg2 = arg2
        self.cell = cell
        self.amount_ancilliary = Instruction.size_of_binary_int

    @staticmethod
    def parse(string):
        string_no_spaces = string.rstrip().lstrip()

        if string_no_spaces[0:3].lower() != "add":
            return None

        split_instruction = string_no_spaces.split(" ")

        arg1 = AnyOf([Cell, Value]).parse(split_instruction[1])
        arg2 = AnyOf([Cell, Value]).parse(split_instruction[2])
        cell = Cell.parse(split_instruction[3])

        return InstructionAdd(arg1, arg2, cell)

    def data_cells_accesed(self):
        return self.arg1.data_cells_accesed() + self.arg2.data_cells_accesed() + self.cell.data_cells_accesed()

    def amnt_ancilliary_qubits(self):
        return self.amount_ancilliary

    def to_binary(self):
        return self.arg1.to_binary() + self.arg2.to_binary() + self.cell.to_binary()

    @staticmethod
    def from_binary(binary_representation):
        any_of = AnyOf([Cell, Value], [Argument.cell_binary_mask, Argument.value_binary_mask])
        cell = any_of.from_binary(binary_representation[-Instruction.cell_size:])
        arg2 = any_of.from_binary(
            binary_representation[-2 * Instruction.cell_size:-Instruction.cell_size])
        arg1 = any_of.from_binary(
            binary_representation[-3 * Instruction.cell_size:-2 * Instruction.cell_size])
        return InstructionAdd(arg1, arg2, cell)

    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        any_of = AnyOf([Cell, Value])
        int_value_cell1 = any_of.as_int_sql_statement(self.arg1, program)
        int_value_cell2 = any_of.as_int_sql_statement(self.arg2, program)

        shift = 0
        if isinstance(self.arg1, Cell) or isinstance(self.arg2, Cell):
            shift = 2 ** (Instruction.size_of_binary_int + 1) - 2

        int_value_cell_3 = int_value_cell1 + " + " + int_value_cell2 + " - " + str(shift)
        binary_value_cell_3 = " , ".join(
            "q{0} = CAST({1} as INTEGER)".format(
                program.start_data + self.cell.cell * Instruction.size_of_binary_int + i,
                "((" + int_value_cell_3 + ")/{0} ) % {1}".format(2 ** i, 2)) for i in
            range(Instruction.size_of_binary_int))

        update_statement = ""

        if isinstance(self.arg1, Cell) or isinstance(self.arg2, Cell):
            cell_arg = self.arg1
            if isinstance(self.arg2, Cell):
                cell_arg = self.arg2
            # First update to avoid unique errors
            update_statement += "update " + tablename + " set " + ",".join(["q{0} = q{0} + 2".format(
                program.start_data + cell_arg.data_cells_accesed()[0] * Instruction.size_of_binary_int + i) for i in
                range(
                    Instruction.size_of_binary_int)]) + " WHERE " + \
                                Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
                                Instruction.get_instruction_mask(program, int_program_counter,
                                                                 binary_instruction)
            update_statement += ";\n"

        # Update the result
        update_statement += "update " + tablename + " set " + binary_value_cell_3 + " WHERE " + \
                            Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
                            Instruction.get_instruction_mask(program, int_program_counter,
                                                             binary_instruction) + ";\n"

        if isinstance(self.arg1, Cell) or isinstance(self.arg2, Cell):
            cell_arg = self.arg1
            if isinstance(self.arg2, Cell):
                cell_arg = self.arg2
            if cell_arg != self.cell:
                # First update to avoid unique errors
                update_statement += "update " + tablename + " set " + ",".join(["q{0} = q{0} - 2".format(
                    program.start_data + cell_arg.data_cells_accesed()[0] * Instruction.size_of_binary_int + i) for i in
                    range(
                        Instruction.size_of_binary_int)]) + " WHERE " + \
                                    Instruction.get_program_counter_mask(program, binary_program_counter) + " and " + \
                                    Instruction.get_instruction_mask(program, int_program_counter,
                                                                     binary_instruction)
                update_statement += ";\n"
        return update_statement

    def update_program_counter(self):
        return True

    def __eq__(self, other):
        if not isinstance(other, InstructionAdd):
            return False
        return other.arg1 == self.arg1 and other.arg2 == self.arg2 and other.cell == self.cell

    def __repr__(self):
        return "ADD " + str(self.arg1) + " " + str(self.arg2) + " " + str(self.cell)
