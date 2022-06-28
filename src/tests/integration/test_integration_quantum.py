from src.main import main
from src.tests.integration.utils import data_result_to_set


class TestQuantumPrograms:

    def test_havoc_bit_program(self):
        _, result_final, _ = main("src/tests/programs/quantum/havoc_bit.qc", 10)
        assert len(result_final) == 2
        # To eliminate the dependency on the program counter
        assert data_result_to_set(result_final) == data_result_to_set(
            [({'d0': 0}, 0.7071067811865476, 0.0), ({'d0': 1}, 0.7071067811865476, 0.0)])

    def test_havoc_bit_program2(self):
        _, result_final, _ = main("src/tests/programs/quantum/havoc_bit2.qc", 10)
        assert len(result_final) == 2
        # To eliminate the dependency on the program counter
        assert data_result_to_set(result_final) == data_result_to_set(
            [({'d0': 0}, 0.7071067811865476, 0.0), ({'d0': 1}, -0.7071067811865476, 0.0)])

    def test_havoc_bit_program3(self):
        _, result_final, _ = main("src/tests/programs/quantum/havoc_bit3.qc", 10)
        assert len(result_final) == 1
        # To eliminate the dependency on the program counter
        assert result_final == [({'d0': 0}, 1.0000000000000002, 0.0)]

    def test_havoc_program(self):
        _, result_final, _ = main("src/tests/programs/quantum/havoc.qc", 10)
        assert len(result_final) == 16
        # To eliminate the dependency on the program counter
        assert data_result_to_set(result_final) == data_result_to_set(
            [({'d0': 0}, 0.25000000000000006, 0.0), ({'d0': 8}, 0.25000000000000006, 0.0),
             ({'d0': 4}, 0.25000000000000006, 0.0), ({'d0': 12}, 0.25000000000000006, 0.0),
             ({'d0': 2}, 0.25000000000000006, 0.0), ({'d0': 10}, 0.25000000000000006, 0.0),
             ({'d0': 6}, 0.25000000000000006, 0.0), ({'d0': 14}, 0.25000000000000006, 0.0),
             ({'d0': 1}, 0.25000000000000006, 0.0), ({'d0': 9}, 0.25000000000000006, 0.0),
             ({'d0': 5}, 0.25000000000000006, 0.0), ({'d0': 13}, 0.25000000000000006, 0.0),
             ({'d0': 3}, 0.25000000000000006, 0.0), ({'d0': 11}, 0.25000000000000006, 0.0),
             ({'d0': 7}, 0.25000000000000006, 0.0), ({'d0': 15}, 0.25000000000000006, 0.0)])

    def test_nondet_multiplication(self):
        _, result_final, program_counters = main("src/tests/programs/quantum/nondet_multiplication.qc", 10)
        # To eliminate the dependency on the program counter
        # TODO Fix float comparison. All the file
        assert set(program_counters) == set(
            [(10, 0.5000000000000001, 0.0), (10, 0.5000000000000001, 0.0), (10, 0.5000000000000001, 0.0),
             (10, 0.5000000000000001, 0.0)])
        assert data_result_to_set(result_final) == data_result_to_set(
            [({'d0': 0, 'd1': 6, 'd2': 2, 'd3': 6, 'd4': 16}, 0.5000000000000001, 0.0),
             ({'d0': 2, 'd1': 6, 'd2': 2, 'd3': 8, 'd4': 4}, 0.5000000000000001, 0.0),
             ({'d0': 1, 'd1': 6, 'd2': 2, 'd3': 7, 'd4': 8}, 0.5000000000000001, 0.0),
             ({'d0': 3, 'd1': 6, 'd2': 2, 'd3': 9, 'd4': 2}, 0.5000000000000001, 0.0)])

    def test_factoring(self):
        _, result_final, program_counters = main("src/tests/programs/quantum/factoring.qc", 10)
        # To eliminate the dependency on the program counter

        for pc, _, _ in program_counters:
            assert pc == 6 or pc == 7

        for d, _, _ in result_final:
            if d["d1"] != 0:
                assert d["d0"] % d["d1"] == d["d4"]

    def test_phase(self):
        _, result_final, program_counters = main("src/tests/programs/quantum/phase.qc", 10)
        # To eliminate the dependency on the program counter
        # TODO Fix float comparison. All the file
        assert program_counters == [(3, 0.0, -1.0)]
        assert result_final == [({'d0': 1}, 0.0, -1.0)]

    def test_diffusion_program(self):
        _, result_final, _ = main("src/tests/programs/quantum/diffusion.qc", 10)
        assert len(result_final) == 4
        # To eliminate the dependency on the program counter
        assert data_result_to_set(result_final) == data_result_to_set(
            [({'d0': 0}, 0.5000000000000001, 0.0), ({'d0': 2}, 0.5000000000000001, 0.0),
             ({'d0': 1}, 0.5000000000000001, 0.0), ({'d0': 3}, 0.5000000000000001, 0.0)])

    def test_diffusion_program2(self):
        _, result_final, _ = main("src/tests/programs/quantum/diffusion2.qc", 10)
        assert len(result_final) == 16
        # To eliminate the dependency on the program counter
        assert data_result_to_set(result_final) == data_result_to_set(
            [({'d0': 0, 'd1': 5, 'd2': 7, 'd3': 9}, 0.6875000000000001, 0.0),
             ({'d0': 8, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0), ({'d0': 4, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0),
             ({'d0': 12, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0), ({'d0': 2, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0),
             ({'d0': 10, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0), ({'d0': 6, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0),
             ({'d0': 14, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0), ({'d0': 1, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0),
             ({'d0': 9, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0), ({'d0': 5, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0),
             ({'d0': 13, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0), ({'d0': 3, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0),
             ({'d0': 11, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0), ({'d0': 7, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0),
             ({'d0': 15, 'd1': 5, 'd2': 7, 'd3': 9}, 0.1875, 0.0)])
