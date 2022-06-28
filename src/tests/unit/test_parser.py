from src.instructions.instruction_set_data import InstructionSetData
from src.instructions.instruction_stop import InstructionStop
from src.instructions.instruction_swap import InstructionSwap
from src.parser import Parser
from src.program import Program


class TestParser:

    def test_swap_program(self):
        program = Parser().parse("src/tests/programs/swap.qc")
        assert program == Program(
            [InstructionSetData(0, 1), InstructionSetData(1, 2), InstructionSwap(0, 1), InstructionSwap(0, 1),
             InstructionStop()])
