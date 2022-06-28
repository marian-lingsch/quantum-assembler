from src.instructions.instruction_interface import Instruction
from src.utils import int_to_binary, binary_to_int, split_list


class TestParser:

    def test_int_to_binary_conversion(self):
        for i in [0, 1, 2, 3, 4, 16, 17, 18, 19, 20, 128, 256, 1023, 1024, 10000000]:
            assert binary_to_int(int_to_binary(i)) == i

    def test_binary_to_int_conversion(self):
        for i in [[0], [1], [0, 1], [1, 1], [0, 0, 1], [0, 0, 0, 1]]:
            assert int_to_binary(binary_to_int(i)) == i

    def test_split_list(self):
        lst = list(range(100))
        for n in [2, 4, 5, 10, 20, 25]:
            assert split_list(lst, n) == [list(range(v * n, (v + 1) * n)) for v in range(100 // n)]

    def test_float_to_binary_conversiont(self):
        for i in [0.0, 1.0, -1.0, 2, -2, 2.5, 2.25, 2.125, -2.125, -5, 5, -5.625, 5.625]:
            assert abs(Instruction.binary_to_float(Instruction.float_to_binary(i)) - i) < 1e-8
