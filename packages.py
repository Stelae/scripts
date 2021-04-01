#!/usr/bin/python3

#Short script that takes a text file containing a "messy" (pasted from cli)
#list of installed packages and converts it to a neat list
#Files must be in the directory of the script.


import os
import unicodedata
import re

# Helper functions
def sanitise(value, allow_unicode=False):
    """
    Adjusted from from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\.\w\s-]', '', value)
    return re.sub(r'[-\s]+', '-', value).strip('-_')
    # return value


# Data
valid_responses = ["y", "yes", "n", "no"]

def main():

    # Default files to use
    fname_in = "packages.txt"
    fname_out = "packages_out.txt"

    while not os.path.isfile(fname_in):
        use_custom = None # user's response on whether to use custom files.
        while (str(use_custom).lower() not in valid_responses):
            use_custom = input("File \"{}\" does not exist. Enter custom files (y/n)? ".format(fname_in))

        # Clean response (keep first letter in lower case)
        use_custom = use_custom.lower()[0]
        if (use_custom != "y"):
            print("Terminating program.")
            exit()
        else:
            fname_in = input("Enter input file: ")
            fname_in = sanitise(fname_in)





    #Read input file
    ################
    fhandle = open(fname_in, "r")

    packages = []

    for line in fhandle:
        line = line.strip()
        
        for word in line.split():
            if word[-1] == "}":
                packages.append(word[:-3])
            else:
                packages.append(word)

    fhandle.close()


    #Write output to file
    #####################

    ##Uncomment this for overwrite protection
    while os.path.isfile(fname_out):
        overwrite = None # user's response on whether to overwrite output file.
        while (str(overwrite).lower() not in valid_responses):
            overwrite = input("File \"{}\" exists. Overwrite (y/n)? ".format(fname_out))

        # Clean response (keep first letter in lower case)
        overwrite = overwrite.lower()[0]
        if (overwrite == "y"):
            break
        else:
            fname_out = input("Enter custom output file: ")
            fname_out = sanitise(fname_out)


    fout = open(fname_out, "w")

    for package in packages:
        fout.write(package + "\n")
        
    #Another copy of the list without line breaks
    fout.write("\n\n") #Spacing between copies of list
    for package in packages:
        fout.write(package + " ")

    fout.close()
    print("Saved results as {}\n".format(fname_out))

    return 0


if __name__ == "__main__":
    main()

