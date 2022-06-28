from src.main import main


class TestArithmeticPrograms:

    def test_add_program(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/addition.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 2, 'd1': 3, 'd2': 5}, 1.0, 0.0)]

    def test_add_program2(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/addition2.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 2, 'd1': 0, 'd2': 5}, 1.0, 0.0)]

    def test_add_program3(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/addition3.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 0, 'd1': 0, 'd2': 5}, 1.0, 0.0)]

    def test_mul_program(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/multiplication.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 3, 'd1': 2, 'd2': 6}, 1.0, 0.0)]

    def test_mul_program2(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/multiplication2.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 3, 'd1': 0, 'd2': 6}, 1.0, 0.0)]

    def test_div_program(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/division.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 12, 'd1': 3, 'd2': 4}, 1.0, 0.0)]

    def test_div_program2(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/division2.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 12, 'd1': 0, 'd2': 4}, 1.0, 0.0)]

    def test_mod_program(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/modulo.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 10, 'd1': 3, 'd2': 1}, 1.0, 0.0)]

    def test_mod_program2(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/modulo2.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 10, 'd1': 0, 'd2': 1}, 1.0, 0.0)]

    def test_sub_program(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/substraction.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 1, 'd1': 10, 'd2': 9}, 1.0, 0.0)]

    def test_sub_program2(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/substraction2.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 1, 'd1': 0, 'd2': 9}, 1.0, 0.0)]

    def test_sqrt_program(self):
        _, result_final, _ = main("src/tests/programs/arithmetic/sqrt.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 4, 'd1': 2}, 1.0, 0.0)]
