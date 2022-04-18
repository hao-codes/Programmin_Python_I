"""
Author: Hao Zheng
Matr.Nr.: K01608113
Exercise 17
"""
import numpy as np


def gen_next_state(state, scope=list):
    state_rows, state_columns = state.shape
    # print(state)
    row_range, col_range = list(range(0, state_rows + 1)), list(range(0, state_columns + 1))

    # check if scope is none or scope values are valid
    if scope == None:
        cropped = state.copy()

    elif (scope[0] in row_range and scope[2] in row_range and scope[0] < scope[2]) and scope[1] in col_range and scope[
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
                            borderhelp_array[i, j - 1] + borderhelp_array[i, j + 1] + borderhelp_array[i + 1, j - 1] + \
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
