"""
Author: Hao Zheng

Exercise 10
"""


def fun(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    except TypeError:
        raise ValueError((f"a ({type(a)}) or b ({type(b)}) was incompatible with division"))
