"""
Author: Hao Zheng

Exercise 20
"""

"""
###############################################################################
The following copyright statement applies to all code within this file.

Copyright statement:
This  material,  no  matter  whether  in  printed  or  electronic  form,
may  be  used  for personal  and non-commercial educational use only.
Any reproduction of this manuscript, no matter whether as a whole or in parts,
no matter whether in printed or in electronic form, requires explicit prior
acceptance of the authors.
###############################################################################

Template file for solution of assignment 3, exercises 18, 19, 20, 21. Contains
backbone for GameOfLife class and example usage of GameOfLife at the end of the
file. Make sure you only changed the methods you are supposed to change in
the file you hand in as your solution.
"""

# Add your import statements here
import re
# Do not modify these import statements
import os

import numpy as np
import tqdm
from matplotlib import pyplot as plt


class GameOfLife:

    def read_config_file(config_file: str):
        print("config_file: " +config_file)
        with open(config_file, "r") as f:
            file_content = f.read()
        file_content_lines = file_content.split("\n")

        for i in file_content_lines:
            if i.startswith("iteration_count:"):
                iteration_count_line = i
            elif i.startswith("dead_symbol:"):
                dead_symbol_line = i
            elif i.startswith("live_symbol:"):
                live_symbol_line = i
            elif i.startswith("init_state:"):
                init_state_line = i
            elif i.startswith("scope:"):
                scope_line = i
        # iteration count as int
        try:
            iteration_count_line
        except:
            raise AttributeError("Iteration Count cannot be extracted")
        # if not iteration_count_line:
        #     raise AttributeError("Iteration Count cannot be extracted")
        try:
            iteration_count_line = iteration_count_line.split()
            iteration_count = int(iteration_count_line[1])
            # print(iteration_count)
        except:
            raise AttributeError("Value is not convertible to integer")

        # dead symbol - char - can be whitespace char, only 1 char
        try:
            dead_symbol_line
        except:
            raise AttributeError("Dead Symbol cannot be extracted")
        # if not dead_symbol_line:
        #     raise AttributeError("Dead Symbol cannot be extracted")

        dead_symbol_line = dead_symbol_line.split(":")
        dead_symbol = dead_symbol_line[1].strip()
        dead_symbol = dead_symbol.replace('\"', "")

        if len(dead_symbol) != 1:
            raise AttributeError("Dead Symbol value is not a single character")

        # print(dead_symbol)

        # live symbol - char - can be whitespace char, only 1 char
        try:
            live_symbol_line
        except:
            raise AttributeError("Live Symbol cannot be extracted")
        # if not live_symbol_line:
        #     raise AttributeError("Live Symbol cannot be extracted")
        # live_symbol_line = live_symbol_line.replace(" ", "")
        live_symbol_line = live_symbol_line.split("\"")

        if len(live_symbol_line[1]) == 1:
            live_symbol = live_symbol_line[1]
        else:
            raise AttributeError("live Symbol value is not a single character")
        # print(live_symbol)

        # extract init , only live and dead symbol, multiple lines - turn to 2d np.array
        try:
            init_state_line
        except:
            raise AttributeError("Init state entry cannot be extracted")

        regex = r"^init_state:\s*\"([^']*)\""
        matches = re.finditer(regex, file_content, re.MULTILINE)

        match = [p.group() for p in matches]
        if match == []:
            raise AttributeError("init state cannot be extracted")

        init_state_str = match[0]
        # print(init_state_str)
        init_state_list = init_state_str.split("\"\n")

        # print(init_state_list)
        init_state = init_state_list[1]
        init_state = init_state.replace("\"", "")
        for i in init_state:
            if i != dead_symbol and i != live_symbol and i != "\n":
                # print(init_state.index(i))
                # print("other symbol: ???" + i + "???")

                raise ValueError("There are other characters than the symbols for dead or live cells in init_state")
        # convert symbols to 0 and 1 as int
        init_state = init_state.replace(dead_symbol, "0")
        init_state = init_state.replace(live_symbol, "1")
        init_state_a = init_state.split("\n")
        init_state_a = list(filter(None, init_state_a))
        non_empty_count = 0
        for i in init_state_a:
            if i != "":
                non_empty_count += 1
        if non_empty_count == 0:
            raise ValueError("The number of non-empty lines is 0")

        length = len(init_state_a[0])
        if all(len(i) != length for i in init_state_a):
            raise ValueError("Non-empty lines do not have the same length")

        # print(init_state_a)
        # create np array
        init_state_final = []
        for i in init_state_a:
            line = []
            for j in i:
                line.append(j)
            init_state_final.append(line)

        init_state_array = np.array(init_state_final, dtype="int32")
        # init_state_array = init_state_array.astype(int)

        # extract scope
        # It is specified in a line with the following format: scope: (row_1, col_1) (row_2, col_2)
        try:
            scope_line
        except AttributeError:
            print("Scope cannot be extracted")
        # if not scope_line:
        #     raise AttributeError("Scope cannot be extracted")

        # scope_line_list = scope_line.split("(")
        # print(scope_line_list)

        pattern = r"\((.*?)\)"
        scope_list = [p.group() for p in re.finditer(pattern, scope_line)]
        # print(scope_list)
        if len(scope_list) != 2:
            raise AttributeError("Scope cannot be extracted")

        scope_1, scope_2 = scope_list[0], scope_list[1]
        scope_1 = scope_1.replace("(", "").replace(")", "").replace(" ", "")
        scope_2 = scope_2.replace("(", "").replace(")", "").replace(" ", "")

        scope_1, scope_2 = scope_1.split(","), scope_2.split(",")
        if len(scope_1) != 2 or len(scope_2) != 2:
            raise AttributeError("Scope cannot be extracted, not enough values given")
        # print(scope_1, scop_2)

        try:
            scope_1 = [int(i) for i in scope_1]
            scope_2 = [int(i) for i in scope_2]
        except:
            raise AttributeError("row_1, col_1, row_2, col_2 are not convertable to an integer.")

        final_scope = scope_1 + scope_2

        return iteration_count, dead_symbol, live_symbol, init_state_array, final_scope

    # Here you should modify the __init__ method (ex18, ex21)
    def __init__(self, config_file: str, state_output_file: str, plot_output_dir: str, video_output_file: str):

        # path attributes, create directories if they don't exist
        config_entries = self.read_config_file(config_file)
        # print("config_file: " + config_file)
        # print(config_entries)
        # print(type(config_entries))
        self.iteration_count = config_entries[0]
        self.dead_symbol = config_entries[1]
        self.live_symbol = config_entries[2]
        self.init_state = config_entries[3]
        self.scope = config_entries[4]

        self.current_iteration = 0
        # current state of game at start = init state
        self.state = config_entries[3]
        print(self.state)
        print(type(self.state))

        self.state_output_file = state_output_file
        if not os.path.exists(self.state_output_file):
            os.makedirs(self.state_output_file)
        else:
            file = open(self.state_output_file, "r+")
            file.truncate(0)
            file.close()

        # print(self.state_output_file)
        self.plot_output_dir = plot_output_dir
        if not os.path.exists(self.plot_output_dir):
            os.makedirs(self.plot_output_dir)
        self.video_output_file = video_output_file
        if not os.path.exists(self.video_output_file):
            os.makedirs(self.video_output_file)
        print(self.plot_output_dir)
        print(self.video_output_file)

        # write empty file/ overwrite file in path state_output_file
        # if not os.path.exists(self.state_output_file):

        # Here you should modify the make_video method (ex20)
        def make_video(self):

            pass

        # my solutions fpr ex16, ex17
        def read_config_file(config_file: str):
            with open(config_file, "r") as f:
                file_content = f.read()
            file_content_lines = file_content.split("\n")

            for i in file_content_lines:
                if i.startswith("iteration_count:"):
                    iteration_count_line = i
                elif i.startswith("dead_symbol:"):
                    dead_symbol_line = i
                elif i.startswith("live_symbol:"):
                    live_symbol_line = i
                elif i.startswith("init_state:"):
                    init_state_line = i
                elif i.startswith("scope:"):
                    scope_line = i
            # iteration count as int
            try:
                iteration_count_line
            except:
                raise AttributeError("Iteration Count cannot be extracted")
            # if not iteration_count_line:
            #     raise AttributeError("Iteration Count cannot be extracted")
            try:
                iteration_count_line = iteration_count_line.split()
                iteration_count = int(iteration_count_line[1])
                # print(iteration_count)
            except:
                raise AttributeError("Value is not convertible to integer")

            # dead symbol - char - can be whitespace char, only 1 char
            try:
                dead_symbol_line
            except:
                raise AttributeError("Dead Symbol cannot be extracted")
            # if not dead_symbol_line:
            #     raise AttributeError("Dead Symbol cannot be extracted")

            dead_symbol_line = dead_symbol_line.split(":")
            dead_symbol = dead_symbol_line[1].strip()
            dead_symbol = dead_symbol.replace('\"', "")

            if len(dead_symbol) != 1:
                raise AttributeError("Dead Symbol value is not a single character")

            # print(dead_symbol)

            # live symbol - char - can be whitespace char, only 1 char
            try:
                live_symbol_line
            except:
                raise AttributeError("Live Symbol cannot be extracted")
            # if not live_symbol_line:
            #     raise AttributeError("Live Symbol cannot be extracted")
            # live_symbol_line = live_symbol_line.replace(" ", "")
            live_symbol_line = live_symbol_line.split("\"")

            if len(live_symbol_line[1]) == 1:
                live_symbol = live_symbol_line[1]
            else:
                raise AttributeError("live Symbol value is not a single character")
            # print(live_symbol)

            # extract init , only live and dead symbol, multiple lines - turn to 2d np.array
            try:
                init_state_line
            except:
                raise AttributeError("Init state entry cannot be extracted")

            regex = r"^init_state:\s*\"([^']*)\""
            matches = re.finditer(regex, file_content, re.MULTILINE)

            match = [p.group() for p in matches]
            if match == []:
                raise AttributeError("init state cannot be extracted")

            init_state_str = match[0]
            # print(init_state_str)
            init_state_list = init_state_str.split("\"\n")

            # print(init_state_list)
            init_state = init_state_list[1]
            init_state = init_state.replace("\"", "")
            for i in init_state:
                if i != dead_symbol and i != live_symbol and i != "\n":
                    # print(init_state.index(i))
                    # print("other symbol: ???" + i + "???")

                    raise ValueError("There are other characters than the symbols for dead or live cells in init_state")
            # convert symbols to 0 and 1 as int
            init_state = init_state.replace(dead_symbol, "0")
            init_state = init_state.replace(live_symbol, "1")
            init_state_a = init_state.split("\n")
            init_state_a = list(filter(None, init_state_a))
            non_empty_count = 0
            for i in init_state_a:
                if i != "":
                    non_empty_count += 1
            if non_empty_count == 0:
                raise ValueError("The number of non-empty lines is 0")

            length = len(init_state_a[0])
            if all(len(i) != length for i in init_state_a):
                raise ValueError("Non-empty lines do not have the same length")

            # print(init_state_a)
            # create np array
            init_state_final = []
            for i in init_state_a:
                line = []
                for j in i:
                    line.append(j)
                init_state_final.append(line)

            init_state_array = np.array(init_state_final, dtype="int32")
            # init_state_array = init_state_array.astype(int)

            # extract scope
            # It is specified in a line with the following format: scope: (row_1, col_1) (row_2, col_2)
            try:
                scope_line
            except AttributeError:
                print("Scope cannot be extracted")
            # if not scope_line:
            #     raise AttributeError("Scope cannot be extracted")

            # scope_line_list = scope_line.split("(")
            # print(scope_line_list)

            pattern = r"\((.*?)\)"
            scope_list = [p.group() for p in re.finditer(pattern, scope_line)]
            # print(scope_list)
            if len(scope_list) != 2:
                raise AttributeError("Scope cannot be extracted")

            scope_1, scope_2 = scope_list[0], scope_list[1]
            scope_1 = scope_1.replace("(", "").replace(")", "").replace(" ", "")
            scope_2 = scope_2.replace("(", "").replace(")", "").replace(" ", "")

            scope_1, scope_2 = scope_1.split(","), scope_2.split(",")
            if len(scope_1) != 2 or len(scope_2) != 2:
                raise AttributeError("Scope cannot be extracted, not enough values given")
            # print(scope_1, scop_2)

            try:
                scope_1 = [int(i) for i in scope_1]
                scope_2 = [int(i) for i in scope_2]
            except:
                raise AttributeError("row_1, col_1, row_2, col_2 are not convertable to an integer.")

            final_scope = scope_1 + scope_2

            return iteration_count, dead_symbol, live_symbol, init_state_array, final_scope

        def gen_next_state(state, scope=list):
            state_rows, state_columns = state.shape
            # print(state)
            row_range, col_range = list(range(0, state_rows + 1)), list(range(0, state_columns + 1))

            # check if scope is none or scope values are valid
            if scope == None:
                cropped = state.copy()

            elif (scope[0] in row_range and scope[2] in row_range and scope[0] < scope[2]) and scope[1] in col_range and \
                    scope[
                        3] in col_range and scope[1] < scope[3]:
                cropped = state[scope[0]:scope[2], scope[1]:scope[3]]
            else:
                cropped = state.copy()
            rows, columns = cropped.shape
            borderhelp_array = np.zeros((rows + 2, columns + 2), dtype="int32")
            borderhelp_array[1:-1, 1:-1] = cropped
            new_cropped = np.zeros((rows + 2, columns + 2), dtype="int32")
            # for i in range(1, rows):
            #     print(i)

            for i in range(1, rows + 1):
                for j in range(1, columns + 1):
                    cell = borderhelp_array[i, j]
                    neighbour_sum = borderhelp_array[i - 1, j - 1] + borderhelp_array[i - 1, j] + borderhelp_array[
                        i - 1, j + 1] + \
                                    borderhelp_array[i, j - 1] + borderhelp_array[i, j + 1] + borderhelp_array[
                                        i + 1, j - 1] + \
                                    borderhelp_array[i + 1, j] + borderhelp_array[i + 1, j + 1]

                    if cell == 1:
                        if neighbour_sum < 2 or neighbour_sum > 3:
                            new_cropped[i, j] = 0
                        elif neighbour_sum in [2, 3]:
                            new_cropped[i, j] = 1
                    if cell == 0 and neighbour_sum == 3:
                        new_cropped[i, j] = 1
            # print(new_cropped)

            new_cropped = new_cropped[1:-1, 1:-1]

            # if state.shape == new_cropped.shape:
            #     new_state = new_cropped
            # else:
            #     new_state = np.zeros(state.shape, dtype="int32")
            #     new_state[scope[0]:scope[2], scope[1]:scope[3]] = new_cropped
            # print(new_state)
            return new_cropped

        # @staticmethod
        # def read_config_file(config_file: str):
        #     """Template version of read_config_file(). This is not a valid solution for ex16."""
        #     init_state = np.array(
        #         [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        #     iteration_count = 10
        #     dead_symbol = '-'
        #     live_symbol = 'o'
        #     scope = [1, 10, 10, 27]
        #     return iteration_count, dead_symbol, live_symbol, init_state, scope

        # Here you should modify the step method (ex21)
        def step(self):
            """Compute the next tick of the simulator and return current number of iteration.
            Returns None if game is completed."""
            self.current_iteration += 1
            if self.current_iteration > self.iteration_count:
                return None
            if self.current_iteration == 1:
                self.state = self.gen_next_state(self.state, self.scope)
            else:
                self.state = self.gen_next_state(self.state, None)
            self.__write_state__()
            self.__state_to_image__()
            return self.current_iteration

        # def gen_next_state(self, state: np.ndarray, scope):
        #     """Template version of gen_next_state(). This is not a valid solution for ex17."""
        #     temp_state_1 = np.array(
        #         [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        #     temp_state_2 = np.array(
        #         [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        #     if np.all(self.state == temp_state_1):
        #         new_state = temp_state_2
        #     else:
        #         new_state = temp_state_1
        #     return new_state

        def __state_to_image__(self):
            """Save state to image file"""
            image_file = os.path.join(self.plot_output_dir, f"state_{self.current_iteration:05}.png")
            fig, ax = plt.subplots()
            ax.imshow(np.asarray(self.state, dtype=np.uint8))
            fig.tight_layout()
            fig.savefig(image_file)
            plt.close(fig)

    # Here you should modify the __write_state__ method (ex19)
    def __write_state__(self, live_symbol=None, dead_symbol=None):
        # check live and dead symbol
        if live_symbol is not None and len(live_symbol) == 1 and isinstance(live_symbol, str):
            live_sym = live_symbol
        else:
            live_sym = self.live_symbol
        if dead_symbol is not None and len(dead_symbol) == 1 and isinstance(dead_symbol, str):
            dead_sym = dead_symbol
        else:
            dead_sym = self.dead_symbol
        # replace o and 1's
        state = self.state
        # print("initial")
        # print(state)
        state = np.where(state == 1, live_sym, state)
        state = np.where(state == "0", dead_sym, state)
        # print(state)
        state_str = ""
        for line in range(0, len(state)):
            for i in state[line]:
                state_str += i
            # if line != state[-1]:
            state_str += "\n"
        # open output file and add state - do not overwrite
        with open(self.state_output_file, "a") as output_file:
            output_file.write(state_str + "\n")
            output_file.close()
        return NotImplemented

    # Here you should modify the make_video method (ex20)
    def make_video(self):

        img_folder = self.plot_output_dir
        video_folder = self.video_output_file
        with open(video_folder, "w"):
            if os.name == "nt":
                command = f"ffmpeg -r 10 -pattern_type glob -i \"{img_folder}/*png\" -c:v libx264 -vprofile baseline -pix_fmt yuv420p -c:a aac -movlags faststart {video_folder}"
                # command = f'ffmeg -framerate 24 -i \"{img_folder}\'
                # ffmpeg -framerate 24 -i img%03d.png output.mp4
                # os.system(
                #    f"ffmpeg -r 10 -pattern_type glob -i \"{img_folder}/*png\" -c:v libx264 -vprofile baseline -pix_fmt yuv420p -c:a aac -movlags faststart {video_folder}.mp4")
                print(command)
                os.system(command)
        return NotImplemented

    # Here you should modify the step method (ex21)
    def step(self):
        """Compute the next tick of the simulator and return current number of iteration.
        Returns None if game is completed."""
        self.current_iteration += 1
        if self.current_iteration > self.iteration_count:
            return None
        if self.current_iteration == 1:
            self.state = self.gen_next_state(self.state, self.scope)
            if self.state in self.seen_generations:
                self.in_loop = True
            else:
                self.seen_generations.append(self.state)
        else:
            self.state = self.gen_next_state(self.state, None)
            if self.state in self.seen_generations:
                self.in_loop = True
            else:
                self.seen_generations.append(self.state)
        self.__write_state__()
        self.__state_to_image__()
        return self.current_iteration

    def gen_next_state(state, scope):
        # scope = [row1, col1, row2, col2]
        if scope is not None:
            row1, col1, row2, col2 = scope
            if row1 < 0 or row1 >= row2 or row1 >= len(state) \
                    or col1 < 0 or col1 >= col2 or col1 >= len(state[0]) \
                    or row2 > len(state) or col2 > len(state[0]):
                scoped_state = state
            else:
                scoped_state = state[row1:row2, col1:col2]
        else:
            scoped_state = state

        new_state = np.zeros_like(scoped_state)
        new_state[:-1, :] += scoped_state[1:, :]  # add bottom neighbor
        new_state[1:, :] += scoped_state[:-1, :]  # add top neighbor
        new_state[:, :-1] += scoped_state[:, 1:]  # add right neighbor
        new_state[:, 1:] += scoped_state[:, :-1]  # add left neighbor

        # add diagonal neighbors
        new_state[:-1, :-1] += scoped_state[1:, 1:]
        new_state[1:, 1:] += scoped_state[:-1, :-1]
        new_state[:-1, 1:] += scoped_state[1:, :-1]
        new_state[1:, :-1] += scoped_state[:-1, 1:]

        # Rule 1: Any live cell with fewer than two live neighbors in the current state dies, as if by underpopulation
        new_state[new_state < 2] = 0
        # Rule 2: Any live cell with two or three live neighbors in the current state lives on to the next generation
        new_state[new_state == 2] = scoped_state[new_state == 2]  # Transfer living cells from state (no new created!)
        # Rule 2 and 4: Any dead cell with exactly three live neighbors in the current state becomes a live cell,
        # as if by reproduction
        new_state[new_state == 3] = 1  # Set to live, regardless of if living cell was there before
        # Rule 3: Any live cell with more than three live neighbors in the current state dies, as if by over population
        new_state[new_state > 3] = 0

        return new_state
    # def gen_next_state(self, state: np.ndarray, scope):
    #     """Template version of gen_next_state(). This is not a valid solution for ex17."""
    #     temp_state_1 = np.array(
    #         [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    #     temp_state_2 = np.array(
    #         [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    #     if np.all(self.state == temp_state_1):
    #         new_state = temp_state_2
    #     else:
    #         new_state = temp_state_1
    #     return new_state

    def __state_to_image__(self):
        """Save state to image file"""
        image_file = os.path.join(self.plot_output_dir, f"state_{self.current_iteration:05}.png")
        fig, ax = plt.subplots()
        ax.imshow(np.asarray(self.state, dtype=np.uint8))
        fig.tight_layout()
        fig.savefig(image_file)
        plt.close(fig)

    if __name__ == "__main__":
        import argparse

        # Create a parser
        parser = argparse.ArgumentParser()
        parser.add_argument('config_file', help='configuration file', type=str)
        parser.add_argument('state_output_file', help='file to write state to', type=str)
        parser.add_argument('plot_output_dir', help='directory to write plotted states to', type=str)
        parser.add_argument('video_output_file', help='file to write video to', type=str)

        # Parse the arguments
        args = parser.parse_args()

        # Create game instance
        game = GameOfLife(config_file=args.config_file, state_output_file=args.state_output_file,
                          plot_output_dir=args.plot_output_dir, video_output_file=args.video_output_file)

        current_iteration = 0
        with tqdm.tqdm() as progressbar:  # Show a progressbar
            while current_iteration is not None:  # Continue until current iteration is None (=End of game)
                current_iteration = game.step()
                progressbar.update()

        # Save video to file
        game.make_video()
