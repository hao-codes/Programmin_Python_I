"""
Author: Hao Zheng

Exercise 13
"""

# get_file_metadata(data_as_string: str)
# return 3 objeccts: hamster ID as string, data entry as integer, column names as list of strings
import re

'''filename = "invalidformat_0.gene.dat"  # Path and name of the file to read
with open(filename, "r") as f:
    file_content = f.read()
# split lines into list
file_content = file_content.split("\n")

indices = []
values = []
if file_content[0] != "% HEADER_START" and file_content[0] != "":
    raise AttributeError("Invalid file format")
for count, value in enumerate(file_content):
    if value in ["% HEADER_START", "% HEADER_END", "% DATA_END"]:
        values.append(value)
        indices.append(count)

if len(indices) == 3:
    x, y = indices[1], indices[2]
    # if indices[0] != 0:

    if file_content[x] == "% DATA_END" and file_content[y] == "% HEADER_END":
        print("ERROR")
        raise AttributeError("% DATA_END is before % HEADER_END")

else:
    print("ERROR")
    raise AttributeError("File does not contain %HEADER_START, %HEADER_END or %DATA_END")

header_lines = file_content[file_content.index("% HEADER_START"): file_content.index("% HEADER_END")]

for h in header_lines:
    if h.startswith("%") or h == "":
        pass
    else:
        raise AttributeError("Header has non-empty lines without % at start")

try:
    hamster_id = [i for i in header_lines if i.startswith("% ID")][0]
    hamster_id = hamster_id[len("% ID:"):].strip()
except:
    raise AttributeError("ID not in header")

try:
    date = [i for i in header_lines if i.startswith("% Date")][0]
    date = date[len("% Date:"):].strip()
except:
    raise AttributeError("Date not in header")
try:
    date = int(date)
except:
    raise TypeError

try:
    columns = [i for i in header_lines if i.startswith("% Columns")][0]
    columns = columns[len("% Columns:"):].strip()
except:
    raise AttributeError("Columns not in header")
columns = columns.split(";")

print(hamster_id)
print(date)
print(columns)
print("----")'''


def get_file_metadata(data_as_string: str):
    filename = data_as_string  # Path and name of the file to read
    # with open(filename, "r") as f:
    #    file_content = f.read()
    # split lines into list
    file_content = filename.split("\n")

    indices = []
    values = []
    if file_content[0] != "% HEADER_START" and file_content[0] != "":
        raise AttributeError("Invalid file format")
    for count, value in enumerate(file_content):
        if value in ["% HEADER_START", "% HEADER_END", "% DATA_END"]:
            values.append(value)
            indices.append(count)

    if len(indices) == 3:
        # if indices[0] != 0:
        #   raise AttributeError("Invalid file format")
        x, y = indices[1], indices[2]
        if file_content[x] == "% DATA_END" and file_content[y] == "% HEADER_END":
            # print("ERROR")
            raise AttributeError("% DATA_END is before % HEADER_END")

    else:
        # print("ERROR")
        raise AttributeError("File does not contain %HEADER_START, %HEADER_END or %DATA_END")

    header_lines = file_content[file_content.index("% HEADER_START"): file_content.index("% HEADER_END")]

    for h in header_lines:
        if h.startswith("%") or h == "":
            pass
        else:
            raise AttributeError("Header has non-empty lines without % at start")

    try:
        hamster_id = [i for i in header_lines if i.startswith("% ID")][0]
        hamster_id = hamster_id[len("% ID:"):].strip()
    except:
        raise AttributeError("ID not in header")

    try:
        date = [i for i in header_lines if i.startswith("% Date")][0]
        date = date[len("% Date:"):].strip()
    except:
        raise AttributeError("Date not in header")
    try:
        date = int(date)
    except:
        raise TypeError

    try:
        columns = [i for i in header_lines if i.startswith("% Columns")][0]
        columns = columns[len("% Columns:"):].strip()
    except:
        raise AttributeError("Columns not in header")
    columns = columns.split(";")

    # print("TEST")
    return hamster_id, date, columns

# out = get_file_metadata("invaliddate.gene.dat")
