import sqlite3

import numpy as np
from src.instructions.instruction_interface import Instruction
from src.utils import split_list, binary_to_int


class DBSimulator:

    def __init__(self, program):
        self.program = program
        self.conn = sqlite3.connect(':memory:')
        self.cur = self.conn.cursor()
        self.amnt_qubits = program.amnt_qubits
        self.conn.create_function("pow", 2, np.power)
        self.conn.create_function("sqrt", 1, lambda x: int(np.sqrt(x)))
        # See: https://blog.devart.com/increasing-sqlite-performance.html
        self.cur.execute('''PRAGMA threads = 8''')  # Maximum of the compiled version of sql
        self.cur.execute('''PRAGMA journal_mode = OFF''')
        self.cur.execute('''PRAGMA synchronous  = OFF''')
        self.cur.execute('''PRAGMA LOCKING_MODE  = EXCLUSIVE''')
        self.table_name = "quantumstate"
        self.init_db()

    def init_db(self):
        query_create = "CREATE TABLE " + self.table_name + " ("
        primary_key = ""
        for t in range(self.amnt_qubits):
            query_create += "q" + str(t) + " Integer , "
            if t == 0:
                primary_key += "q" + str(t)
            else:
                primary_key += ", " + "q" + str(t)
        # Uniqueness constraint is violated on updates by mysql
        # https://stackoverflow.com/questions/11207574/how-to-swap-values-of-two-rows-in-mysql-without-violating-unique-constraint
        query_create += " revalue REAL, imvalue REAL, PRIMARY KEY (" + primary_key + "))"
        # query_create += " revalue REAL, imvalue REAL)"
        self.cur.execute(query_create)
        binary_state = [0 for _t in range(self.program.program_counter_size + self.program.anciliary_qubits)]
        binary_state += self.program.as_binary()
        binary_state += [0] * self.program.data_size
        self.cur.execute("insert into " + self.table_name + " values (?" + ", ?" * (self.amnt_qubits + 1) + ")",
                         binary_state + [1.0, 0.0])
        self.conn.commit()
        return

    def execute(self, iterations):
        for _t in range(iterations):
            self.make_step()
        return self.get_state()

    def make_step(self):
        int_pcs, binary_pcs = self.get_program_counters()
        assert len(int_pcs) == len(binary_pcs)
        instruction_objects, binary_instructions, program_counter_pos_instruction = self.get_instructions(int_pcs,
                                                                                                          binary_pcs)
        assert len(instruction_objects) == len(binary_instructions)
        for i in range(len(instruction_objects)):
            query_script = instruction_objects[i].update_db_sql_statement(self.table_name,
                                                                          program_counter_pos_instruction[i][1],
                                                                          program_counter_pos_instruction[i][0],
                                                                          binary_instructions[i], self.program)
            self.cur.executescript(query_script)
            if instruction_objects[i].update_program_counter():
                self.update_program_counter(program_counter_pos_instruction[i][1],
                                            program_counter_pos_instruction[i][0], binary_instructions[i])
        return

    def get_program_counters(self):
        self.conn.commit()
        binary_pcs = self.cur.execute("Select DISTINCT " +
                                      self.generate_qubits_select_in_range(0, self.program.program_counter_size) +
                                      " FROM " + self.table_name).fetchall()
        return [self.program.binary_program_counter_to_int(pc) for pc in binary_pcs], binary_pcs

    def get_instructions(self, int_pcs, binary_pcs):
        binary_instructions = []
        program_counter = []
        for i, pc in enumerate(int_pcs):
            query_result = self.cur.execute("Select DISTINCT " +
                                            self.get_instruction_qubits(pc) +
                                            " FROM " + self.table_name +
                                            " WHERE " + self.get_program_counter_mask(
                binary_pcs[i])).fetchall()
            program_counter += [(pc, binary_pcs[i])] * len(query_result)
            binary_instructions += query_result

        instruction_objects = []
        for ins_bin in binary_instructions:
            binary_instruction_id = ins_bin[0:self.program.size_of_instruction_ids]
            instruction_data = ins_bin[self.program.size_of_instruction_ids:]
            instruction_id = self.program.binary_to_int(binary_instruction_id)
            instruction_class = self.program.id_to_instruction[instruction_id]
            instruction = instruction_class.from_binary(instruction_data)
            instruction_objects.append(instruction)

        return instruction_objects, binary_instructions, program_counter

    def get_instruction_qubits(self, pc):
        min_range = self.program.program_counter_size + self.program.anciliary_qubits + pc * self.program.instruction_size
        upper_range = self.program.program_counter_size + self.program.anciliary_qubits + (
                pc + 1) * self.program.instruction_size
        return self.generate_qubits_select_in_range(min_range, upper_range)

    def generate_qubits_select_in_range(self, min_range, upper_range):
        return ", ".join(["q" + str(_t) for _t in range(min_range, upper_range)])

    def get_program_counter_mask(self, binary_program_counter):
        assert len(binary_program_counter) >= self.program.program_counter_size
        return " and ".join(["q" + str(t) + " = " + str(binary_program_counter[t]) for t in
                             range(0, self.program.program_counter_size)])

    def get_state(self):
        """
        Only this function commits the final transaction. This is done for performance reasons. Only use this function
        to access the state or commit before accessing the state.
        """
        self.conn.commit()
        all_qubits = ", ".join(["q" + str(t) for t in range(self.amnt_qubits)])
        return self.cur.execute(
            "SELECT * FROM (SELECT " + all_qubits + ", sum(revalue) as revalue, sum(imvalue) as imvalue FROM " + self.table_name + " GROUP BY " + all_qubits + ") WHERE abs(revalue) + abs(imvalue) > pow(10.0, -10)").fetchall()

    def update_program_counter(self, binary_pc, int_pc, binary_instruction):
        new_binary_pc = self.program.program_counter_to_binary(int_pc + 1)
        query = "update " + self.table_name + " set " + " , ".join(["q{0} = {1}".format(t, v) for t, v in enumerate(
            new_binary_pc)]) + " WHERE " + self.get_program_counter_mask(
            binary_pc) + " and " + Instruction.get_instruction_mask(self.program, int_pc, binary_instruction)
        self.cur.execute(query)

    def get_data(self):
        total_data = []
        state = self.get_state()
        for s in state:
            data_binary = split_list(s[self.program.start_data:-2], Instruction.size_of_binary_int)
            total_data.append(({"d" + str(i): binary_to_int(v) for i, v in enumerate(data_binary)}, s[-2], s[-1]))
        return total_data

    def get_program_counter(self):
        total_data = []
        state = self.get_state()
        for s in state:
            data_binary = s[:Instruction.size_of_binary_int]
            total_data.append((binary_to_int(data_binary), s[-2], s[-1]))
        return total_data
