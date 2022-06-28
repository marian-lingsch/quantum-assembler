from src.instructions.instruction_set_data import InstructionSetData
from src.instructions.instruction_swap import InstructionSwap


class TestInstruction:

    def test_set_data_instruction(self):
        instruction_string = "  SET d1 0 "
        instruction = InstructionSetData.parse(instruction_string)
        instruction_expected = InstructionSetData(1, 0)
        assert instruction == instruction_expected

    def test_set_swap_instruction(self):
        instruction_string = "  SWAP d0 d1 "
        instruction = InstructionSwap.parse(instruction_string)
        instruction_expected = InstructionSwap(0, 1)
        assert instruction == instruction_expected

    def test_set_swap_instruction_multi_case(self):
        instruction_string = "  sWaP d0 d1 "
        instruction = InstructionSwap.parse(instruction_string)
        instruction_expected = InstructionSwap(0, 1)
        assert instruction == instruction_expected
