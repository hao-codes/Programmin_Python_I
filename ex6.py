"""
Author: Hao Zheng

Exercise 6
"""


def fun(long_string):
    words = long_string.split()
    words = [x for x in words if x != "end" and x != "exit"]

    words = [i.upper() for i in words]

    words = ";".join(words)
    return words
