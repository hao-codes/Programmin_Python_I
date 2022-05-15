"""
Author: Hao Zheng

Exercise 14
"""

# take 3 commandlines arguments: nput_folder, output_file, and subsequence

import numpy as np
import sys
import pandas as pd
from ex11 import count_bases_and_subsequence
from ex12 import get_hamsters
from ex13 import get_file_metadata

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
arguments = sys.argv
# arguments.remove("ex14.py")
# if len(arguments) == 3:
# input_folder, output_file, subsequence = arguments[0], arguments[1], arguments[2]


input_folder, output_file, subsequence = arguments[1], arguments[2], arguments[3]

# print(input_folder)
# print(output_file)
# print(subsequence)

generator_result = get_hamsters(input_folder)
# i, nfiles, os.path.basename(filepath), content

my_array = np.zeros((180, 5), dtype="float64")
# print(my_array)
# print(my_array.shape)

for i in generator_result:
    # print(type(i[0]))
    current_file, total_files, filename, file_content = i[0], i[1], i[2], i[3]

    sub_base_counts = count_bases_and_subsequence(file_content, subsequence)

    subsequence_count = sub_base_counts[0]
    base_count = sub_base_counts[1]
    # print("a: " + str(base_count["a"]))
    meta = get_file_metadata(file_content)

    date = meta[1]

    my_array[date, 0] = my_array[date, 0] + subsequence_count
    my_array[date, 1] = my_array[date, 1] + base_count["a"]
    my_array[date, 2] = my_array[date, 2] + base_count["c"]
    my_array[date, 3] = my_array[date, 3] + base_count["g"]
    my_array[date, 4] = my_array[date, 4] + base_count["t"]

    # print(meta)  # hamster_id, date, columns
    # print(sub_base_counts)
    # print(base_count)
    print(f"[{current_file + 1}/{total_files}] Processing {filename}")

my_array = my_array / 15
'''print(my_array.dtype)
print(my_array[:5, ])
print(my_array.dtype)'''

df = pd.DataFrame(my_array, columns=["subsequence", "a", "c", "g", "t"], )
'''print("----")
print(df.iloc[0, 3])

print("----")

print(df["a"][2])
print("----")
print(type(df["a"][2]))

# save as csv output file
# print(date_test)
print(date_test.count(179))'''

df.to_csv(output_file, ",", index=False)
