from src.analysis.reversibility import reversible
from src.parser import Parser


class TestAnalysis:

    def test_for_program(self):
        program = Parser().parse("src/tests/programs/for_loop.qc")
        assert not reversible(program)

    def test_for2_program(self):
        program = Parser().parse("src/tests/programs/for_loop2.qc")
        assert not reversible(program)

    def test_if_then_else_program(self):
        program = Parser().parse("src/tests/programs/if_then_else.qc")
        assert reversible(program)

    def test_if_then_else2_program(self):
        program = Parser().parse("src/tests/programs/if_then_else2.qc")
        assert reversible(program)

    def test_skip_program(self):
        program = Parser().parse("src/tests/programs/skip.qc")
        assert reversible(program)

    def test_factoring_program(self):
        program = Parser().parse("src/tests/programs/quantum/factoring.qc")
        assert reversible(program)

    def test_havoc_program(self):
        program = Parser().parse("src/tests/programs/quantum/havoc.qc")
        assert reversible(program)

    def test_nondet_multiplication_program(self):
        program = Parser().parse("src/tests/programs/quantum/nondet_multiplication.qc")
        assert reversible(program)
