"""
Author: Hao Zheng
Matr.Nr.: K01608113
Exercise 15
"""

import os
import sys
import subprocess
from plot_csv import plot_csv

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))
arguments = sys.argv
output_folder = arguments[1]

# Create a folder with name 125 in folder output_folder
folder = output_folder + "/125"
current_dir = os.getcwd()
# print(current_dir)
path = os.path.join(current_dir, folder)
# print(path)
try:
    os.makedirs(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)

# call hamstergenegen.py wiht folder 125 as command line argument

subprocess.call([sys.executable, "hamstergenegen.py", folder])

# call ex14.py: folder with data, outputfile name, subsequence
output_csv = output_folder + "/patterns_analysis.csv"
subprocess.call([sys.executable, "ex14.py", folder, output_csv, "acag"])

# use plot csv func form plot csv: plot_csv(inputfilename: str, outputfilename: str):

plot_csv(output_csv, output_folder + "/patterns_analysis.png")
