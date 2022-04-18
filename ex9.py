"""
Author: Hao Zheng
Matr.Nr.: K01608113
Exercise 9
"""
def fun(data):
    # data is list of lists
    # return list
    output = []
    for nested in data:
        indicator = nested[0]
        for i in range(1, 1 + indicator):
            output.append(nested[i])
    return output
