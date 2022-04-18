"""
Author -- Michael Widrich, Andreas Schörgenhumer
Contact -- schoergenhumer@ml.jku.at
Date -- 04.11.2021

###############################################################################

The following copyright statement applies to all code within this file.

Copyright statement:
This  material,  no  matter  whether  in  printed  or  electronic  form,
may  be  used  for personal  and non-commercial educational use only.
Any reproduction of this manuscript, no matter whether as a whole or in parts,
no matter whether in printed or in electronic form, requires explicit prior
acceptance of the authors.

###############################################################################
"""

import os
import glob


def get_hamsters(folderpath: str):
    # Search for all files ending in '*.gene.dat' in the folder folderpath
    # and sort the list
    filepaths = sorted(glob.glob(os.path.join(folderpath, "**", "*.gene.dat"), recursive=True))
    nfiles = len(filepaths)
    # Loop through all files
    for i, filepath in enumerate(filepaths):
        # Open each file in read mode and get its content
        with open(filepath, "r") as f:
            content = f.read()
        # Yield one file content per iteration
        yield i, nfiles, os.path.basename(filepath), content


if __name__ == "__main__":
    folderpath = "ex12_testfiles/test3"
    file_reader = get_hamsters(folderpath=folderpath)
    # This should print the name and length of each file content for all sorted files:
    for i, nfiles, filename, file_content in file_reader:
        # file_content should be the content of a file as string
        print(f"[{i + 1}/{nfiles}] {filename}: {len(file_content)}")
