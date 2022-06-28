from src.main import main


class TestPrograms:

    def test_set_program_state(self):
        result, _, _ = main("src/tests/programs/set_values.qc", 10)
        assert result == [(0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                           0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                           1.0, 0.0)]

    def test_set_program_values2(self):
        _, result, _ = main("src/tests/programs/set_values.qc", 10)
        assert result == [({'d0': 5, 'd1': 3, 'd2': 2, 'd3': 0, 'd4': 0, 'd5': 0, 'd6': 0, 'd7': 0, 'd8': 0, 'd9': 0,
                            'd10': 2}, 1.0, 0.0)]

    def test_swap_program(self):
        result_orig, _, _ = main("src/tests/programs/swap.qc", 2)
        result_final, _, _ = main("src/tests/programs/swap.qc", 10)
        assert len(result_final) == 1
        assert len(result_orig) == 1
        # To eliminate the dependency on the program counter
        assert result_orig[0][5:] == result_final[0][5:]

    def test_skip_program(self):
        result_orig, _, _ = main("src/tests/programs/skip.qc", 0)
        result_final, _, _ = main("src/tests/programs/skip.qc", 10)
        assert len(result_final) == 1
        assert len(result_orig) == 1
        # To eliminate the dependency on the program counter
        assert result_orig[0][5:] == result_final[0][5:]

    def test_set_pc_program(self):
        result_orig, _, _ = main("src/tests/programs/setpc.qc", 1)
        result_final, _, _ = main("src/tests/programs/setpc.qc", 11)
        assert len(result_final) == 1
        assert len(result_orig) == 1
        # To eliminate the dependency on the program counter
        assert result_orig == result_final

    def test_if_then_else_program(self):
        _, result_final, program_counters = main("src/tests/programs/if_then_else.qc", 10)
        # To eliminate the dependency on the program counter
        assert program_counters == [(5, 1.0, 0.0)]
        assert result_final == [({'d0': 1, 'd1': 4, 'd2': 6}, 1.0, 0.0)]

    def test_if_then_else_program2(self):
        _, result_final, program_counters = main("src/tests/programs/if_then_else2.qc", 10)
        # To eliminate the dependency on the program counter
        assert program_counters == [(7, 1.0, 0.0)]
        assert result_final == [({'d0': 0, 'd1': 4, 'd2': 6}, 1.0, 0.0)]

    def test_if_then_else_program3(self):
        _, result_final, program_counters = main("src/tests/programs/if_then_else3.qc", 10)
        # To eliminate the dependency on the program counter
        assert program_counters == [(2, 1.0, 0.0)]
        assert result_final == [({'d0': 0}, 1.0, 0.0)]

    def test_if_then_else_program4(self):
        _, result_final, program_counters = main("src/tests/programs/if_then_else4.qc", 10)
        # To eliminate the dependency on the program counter
        assert program_counters == [(4, 1.0, 0.0)]
        assert result_final == [({'d0': 0}, 1.0, 0.0)]
