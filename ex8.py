"""
Author: Hao Zheng
Matr.Nr.: K01608113
Exercise 8
"""


def fun(lines):
    # input is list
    # return tuple
    # remove lines starting with #
    lines = [i for i in lines if i.startswith("#") == False]
    new = []
    for i in lines:
        split = i.split()
        for x in split:
            new.append(x)
    unique_insensitive = set([i.lower() for i in new])

    unique_sensitive = set(new)
    output = (len(unique_sensitive), len(unique_insensitive))
    return output


out = fun(["    ",
           "   ",
           "# should results in (0, 0)",
           ""])
print(out)
