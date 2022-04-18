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


def count_bases_and_subsequence(data_as_string, subsequence):
    """This function will scan the string 'data_as_string', count the
    individual bases, and count an arbitrary subsequence of bases specified in
    'subsequence'."""

    # We can convert the subsequence string to lower case letters to make the
    # subsequence count case insensitive:
    subsequence = subsequence.lower()  # this converts everything to lower case
    
    # We could also convert data_as_string to lower case but this is less
    # memory efficient (we would duplicate the whole string in memory), so we
    # will use a different approach later.
    
    # Split file content string into lines
    lines = data_as_string.split("\n")  # alternative: data_as_string.splitlines()

    # Dictionary to store the counts of individual bases in
    counts = dict(a=0, c=0, g=0, t=0)
    
    # Our counter for the subsequence
    subsequence_count = 0
    
    # Split the subsequence string to a list where each element is a character
    subsequence_list = list(subsequence)
    
    # Create a dummy-list which we will later fill with the most recent bases
    # to compare with subsequence_list. We will use None to initialize the
    # list elements. Later we will add None as element instead of a base if
    # the line is invalid.
    recent_bases_list = [None] * len(subsequence_list)
    
    # Iterate over all lines
    for line in lines:
        if line == "% DATA_END":  # End of data reached?
            # If end of data is reached, escape from loop
            break
        elif (len(line) == 0) or line.startswith("%"):  # Invalid data line?
            # Add None to the end and remove first element for subsequence
            # comparison:
            recent_bases_list = recent_bases_list[1:] + [None]
            # If empty line or comment line, skip to next line
            continue
        
        # Get values of columns in this line:
        info, base, quality = line.split(";")
        
        if float(quality) < 0.07:  # Quality too low?
            # Add None to the end and remove first element for subsequence
            # comparison:
            recent_bases_list = recent_bases_list[1:] + [None]
            # If quality < 0.07, skip to next line
            continue
        
        # Remove leading and trailing whitespace characters, just in case
        base = base.strip()
        
        # Make sure we are case insensitive
        base = base.lower()
        
        # We could use if-elif-else conditions here to increase count-variables
        # for the individual bases. But since we use a dictionary for the
        # counts, we can just use the base itself as key:
        try:
            # Increase counter for the specific base
            counts[base] += 1
            # Add the base to the end and remove first element
            recent_bases_list = recent_bases_list[1:] + [base]
        except KeyError:  # Current Base does not exist in our dictionary keys
            # Add None to the end and remove first element for subsequence
            recent_bases_list = recent_bases_list[1:] + [None]
            # If the base entry was not in our dictionary keys, go to the next line
            continue
        
        # If the recent bases match the subsequence, we increase the
        # subsequence count by 1:
        if recent_bases_list == subsequence_list:
            subsequence_count += 1
            # Add None as last list character to avoid over-lapping matches
            # (this is not relevant for the grading but makes more sense in
            # this setting)
            recent_bases_list = recent_bases_list[1:] + [None]
    
    # Return the counts
    return subsequence_count, counts


if __name__ == "__main__":
    #
    # Just for testing/debugging
    #
    filename = "ex11_testfiles/correct_7.gene.dat"  # Some testfile to read
    with open(filename, "r") as fh:
        file_content = fh.read()  # Read file content as string
    
    subsequence = "ATTC"  # Some arbitrary subsequence
    
    # Function call
    subsequence_count, base_counts = count_bases_and_subsequence(
            data_as_string=file_content, subsequence=subsequence)
    
    # Print result
    print(subsequence_count, base_counts)
