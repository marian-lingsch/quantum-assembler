from abc import ABC, abstractmethod
from dis import Instruction

from src import utils
from src.instructions.arguments.argument_interface import Argument


class Instruction(ABC):
    size_of_binary_int = 8
    size_of_binary_float = 16
    size_of_float_after_comma = 8
    float_shift = 2 ** 7
    cell_size = size_of_binary_int + Argument.mask_length

    @staticmethod
    @abstractmethod
    def parse(string):
        """
        Parses the string according to the instruction
        :param string: the string representation of the instruction
        :return: None if it could not be parsed, else it returns an instance of Instruction
        """

    @abstractmethod
    def data_cells_accesed(self):
        """
        :return: The data cells which are accessed by the instruction
        """

    @abstractmethod
    def amnt_ancilliary_qubits(self):
        """
        :return: The amount of ancilliry qubits required by the instruction
        """

    @abstractmethod
    def to_binary(self):
        """
        :return: The binary representation of the function
        """

    @staticmethod
    @abstractmethod
    def from_binary(binary_representation):
        """
        The instructions are padded with zeros from the left, till the size of the instruction
        :return: The instruction class from its binary representation
        """

    @abstractmethod
    def update_db_sql_statement(self, tablename, binary_program_counter, int_program_counter, binary_instruction,
                                program):
        """
        :param tablename: The name of the table to be updated the phases are described by the attributes revalue and imvalue and the qubits have the format qi
        :param binary_program_counter: the binary representation of the program counter in order to not execute the instruction in other states
        :param int_program_counter: the int representation of the program counter in order to not execute the instruction in other states
        :param binary_instruction: the binary representation of the instruction in order to not execute the instruction in other states
        :return:
        """

    @staticmethod
    def int_to_binary(value):
        res = utils.int_to_binary(value)
        return res + [0] * max(Instruction.size_of_binary_int - len(res), 0)

    @staticmethod
    def binary_to_int(binary_value):
        assert len(binary_value) <= Instruction.size_of_binary_int
        return utils.binary_to_int(binary_value)

    @staticmethod
    def float_to_binary(value):
        res = utils.int_to_binary((2 ** Instruction.size_of_float_after_comma) * (value + Instruction.float_shift))
        return res + [0] * max(Instruction.size_of_binary_float - len(res), 0)

    @staticmethod
    def binary_to_float(binary_value):
        assert len(binary_value) <= Instruction.size_of_binary_float
        return float(utils.binary_to_int(binary_value)) / (
                2 ** (Instruction.size_of_float_after_comma)) - Instruction.float_shift

    @abstractmethod
    def update_program_counter(self):
        """

        :return: if the program counter should be updated after executing the instruction
        """

    @abstractmethod
    def __eq__(self, other):
        """
        :param other: Another instruction
        :return: if the instructions are equal or not
        """

    @staticmethod
    def generate_qubits_select_in_range(min_range, upper_range):
        return ", ".join(["q" + str(_t) for _t in range(min_range, upper_range)])

    @staticmethod
    def get_program_counter_mask(program, binary_program_counter):
        assert len(binary_program_counter) >= program.program_counter_size
        return " and ".join(["q" + str(t) + " = " + str(binary_program_counter[t]) for t in
                             range(0, program.program_counter_size)])

    @staticmethod
    def statement_to_binary(cell_position, program):
        return " + ".join(
            "{0}*q{1}".format(2 ** i, program.start_data + cell_position * Instruction.size_of_binary_int + i) for i in
            range(Instruction.size_of_binary_int))

    @staticmethod
    def get_instruction_mask(program, pc, binary_instruction):
        return " and ".join(["q" + str(t) + " = " + str(binary_instruction[i]) for i, t in
                             enumerate(
                                 range(
                                     program.program_counter_size + program.anciliary_qubits + pc * program.instruction_size,
                                     program.program_counter_size + program.anciliary_qubits + (
                                             pc + 1) * program.instruction_size))])
