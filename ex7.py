"""
Author: Hao Zheng

Exercise 7
"""


def fun(long_string):
    count = {}
    #long_string = long_string.lower()
    unique_ch = []
    for x in long_string:
        if x.isalpha():
            unique_ch.append(x)
    unique_ch = set(unique_ch)
    for i in unique_ch:
        count[i] = long_string.count(i)

    return count
