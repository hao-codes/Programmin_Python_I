"""
Author: Hao Zheng
Matr.Nr.: K01608113
Exercise 16
"""

import numpy as np
import re


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
