import time

import numpy as np
from matplotlib import pyplot as plt

from src.db_simulator import DBSimulator
from src.instructions.arithmetic.instruction_add import InstructionAdd
from src.instructions.arithmetic.instruction_division import InstructionDivision
from src.instructions.arithmetic.instruction_modulo import InstructionModulo
from src.instructions.arithmetic.instruction_multiplication import InstructionMultiplication
from src.instructions.arithmetic.instruction_sqrt import InstructionSqrt
from src.instructions.arithmetic.instruction_substract import InstructionSubstract
from src.instructions.boolean.instructio_or import InstructionOr
from src.instructions.boolean.instruction_and import InstructionAnd
from src.instructions.boolean.instruction_not import InstructionNot
from src.instructions.instruction_if_then_else import InstructionIfThenElse
from src.instructions.instruction_set_data import InstructionSetData
from src.instructions.instruction_set_pc import InstructionSetProgramCounter
from src.instructions.instruction_skip import InstructionSkip
from src.instructions.instruction_stop import InstructionStop
from src.instructions.instruction_swap import InstructionSwap
from src.instructions.quantum.instruction_diffusion import InstructionDiffusion
from src.instructions.quantum.instruction_havoc_data import InstructionHavocData
from src.instructions.quantum.instruction_havoc_data_bit import InstructionHavocDataBit
from src.instructions.quantum.instruction_phase import InstructionPhase
from src.parser import Parser


def dummy():
    # Required for initializing the subclasses of the Instruction correctly
    i = InstructionStop()
    i = InstructionSwap(1, 1)
    i = InstructionSetData(1, 1)
    i = InstructionSetProgramCounter(1)
    i = InstructionSkip()
    i = InstructionAdd(1, 1, 1)
    i = InstructionMultiplication(1, 1, 1)
    i = InstructionHavocDataBit(0)
    i = InstructionHavocData(0, 1, 1)
    i = InstructionModulo(0, 1, 2)
    i = InstructionDivision(0, 1, 2)
    i = InstructionAnd(0, 1, 2)
    i = InstructionOr(0, 1, 2)
    i = InstructionNot(0, 1)
    i = InstructionIfThenElse(0, 1, 2)
    i = InstructionSubstract(0, 1, 2)
    i = InstructionDiffusion()
    i = InstructionPhase()
    i = InstructionSqrt()


def main(filename, iterations):
    program = Parser().parse(filename)
    if program is None:
        return None
    simulator = DBSimulator(program)
    simulator.execute(iterations)
    return simulator.get_state(), simulator.get_data(), simulator.get_program_counter()


def main_benchmark(filename, iterations_simulator, iterations_run):
    times = []
    for n in range(2, 2 ** 8 - 1):
        if n % 10 == 0:
            print("Iteration: " + str(n))
        time_forn = []
        for _ in range(iterations_run):
            file_contents = open(filename, mode="r").read()
            new_file_contents = file_contents.replace("NUMBER1", str(n))
            amount_of_havoc_bits = int(np.ceil(np.log2(np.ceil(np.sqrt(n)))))
            new_file_contents = new_file_contents.replace("NUMBER2",
                                                          str(np.min([7, np.max([1, amount_of_havoc_bits])])))
            new_filename = filename + ".bench"
            open(new_filename, mode="w+").write(new_file_contents)
            start = time.time()
            main(new_filename, iterations_simulator)
            end = time.time()
            time_forn.append(end - start)
        times.append(time_forn)
    return times


if __name__ == "__main__":
    print("Executing Quantum Benchmark")
    times_quantum = main_benchmark("benchmark/erathostenes.qc", 300, 1)
    print("Executing Classic Benchmark")
    times_classic = main_benchmark("benchmark/erathostenes_classic.qc", 300, 1)

    average_time_classic = list(map(lambda x: np.average(x), times_classic))
    average_time_quantum = list(map(lambda x: np.average(x), times_quantum))

    print("Times Classic", average_time_classic)
    print("Times Quantum", average_time_quantum)

    plt.plot(range(2, len(average_time_classic) + 2), average_time_classic, label="Average Times Classic")
    plt.plot(range(2, len(average_time_quantum) + 2), average_time_quantum, label="Average Times Quantum")
    plt.xlabel("Number to be factored")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.savefig("benchmark.png")
