from src.instructions.instruction_interface import Instruction
# This file needs to be aware of the instructions
from src.program import Program


class Parser:

    def __init__(self):
        self.labels_to_instruction_position = {}

    def parse(self, filename):
        file_contents = open(filename, mode="r").read()
        counter = 0
        instructions = []

        # First collect labels
        for line in file_contents.split("\n"):
            if line.lstrip()[0:2] == "//" or len(line.replace(" ", "")) == 0:
                continue

            possible_label = Parser.parse_label(line)
            if possible_label is not None:
                self.labels_to_instruction_position[possible_label] = counter
                continue

            counter += 1

        # Then create the program
        for line in file_contents.split("\n"):

            if line.lstrip()[0:2] == "//" or len(line) == 0:
                continue

            possible_label = Parser.parse_label(line)
            if possible_label is not None:
                continue

            for k, v in self.labels_to_instruction_position.items():
                line = line.replace(k, str(v))

            for inst in Instruction.__subclasses__():
                possible_instruction = inst.parse(line)
                if possible_instruction is not None:
                    instructions.append(possible_instruction)
                    break

        if instructions == []:
            print("Empty program")
            return None

        return Program(instructions)

    @staticmethod
    def parse_label(label):
        if label.rstrip()[-1] == ":":
            return label.rstrip().lstrip()[:-1]
        else:
            return None
