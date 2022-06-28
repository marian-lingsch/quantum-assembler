from src.main import main


class TestBooleanPrograms:

    def test_and_program(self):
        _, result_final, _ = main("src/tests/programs/boolean/and.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 1, 'd1': 0, 'd2': 0, 'd3': 1, 'd4': 1, 'd5': 1, 'd6': 0, 'd7': 1, 'd8': 0,
                                  'd9': 0, 'd10': 0, 'd11': 0}, 1.0, 0.0)]

    def test_and_program2(self):
        _, result_final, _ = main("src/tests/programs/boolean/and2.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 0, 'd1': 0, 'd2': 0, 'd3': 1, 'd4': 0, 'd5': 1, 'd6': 0, 'd7': 1, 'd8': 0,
                                  'd9': 0, 'd10': 0, 'd11': 0}, 1.0, 0.0)]

    def test_or_program(self):
        _, result_final, _ = main("src/tests/programs/boolean/or.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 1, 'd1': 0, 'd2': 1, 'd3': 1, 'd4': 1, 'd5': 1, 'd6': 0, 'd7': 1, 'd8': 1,
                                  'd9': 0, 'd10': 0, 'd11': 0}, 1.0, 0.0)]

    def test_or_program2(self):
        _, result_final, _ = main("src/tests/programs/boolean/or2.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 0, 'd1': 0, 'd2': 1, 'd3': 1, 'd4': 0, 'd5': 1, 'd6': 0, 'd7': 1, 'd8': 1,
                                  'd9': 0, 'd10': 0, 'd11': 0}, 1.0, 0.0)]

    def test_not_program(self):
        _, result_final, _ = main("src/tests/programs/boolean/not.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 0, 'd1': 1, 'd2': 1, 'd3': 0}, 1.0, 0.0)]

    def test_not_program2(self):
        _, result_final, _ = main("src/tests/programs/boolean/not2.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 0, 'd1': 1, 'd2': 0, 'd3': 0}, 1.0, 0.0)]
