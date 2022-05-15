"""
Author: Hao Zheng

Exercise 5
"""

a = []
while "x" not in a:
    my_variable = input("Enter int >= 0 or 'x' to exit: ")

    if my_variable.isdecimal():
        numb = int(my_variable)
        a.append(numb)

    elif my_variable == "x":
        print(sum(a))
        break
    else:
        print("You must enter an int >= 0 or 'x'")
