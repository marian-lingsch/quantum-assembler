from abc import ABC, abstractmethod


class Argument(ABC):
    mask_length = 1
    cell_binary_mask = [0]
    value_binary_mask = [1]

    @staticmethod
    @abstractmethod
    def parse(string):
        """

        :param string: The string used in order to parse the argument
        :return: The argument as a class
        """
        pass

    @abstractmethod
    def data_cells_accesed(self):
        """

        :return: The cells accesed by the type if any
        """
        pass

    @abstractmethod
    def to_binary(self):
        """

        :return: The binary representation to recover the information in the argument
        """

    @abstractmethod
    def as_int_sql_statement(self, program):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __repr__(self):
        pass
