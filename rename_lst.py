#!/usr/bin/python3
#Goes into all .m3u files and updates specified string
#Requires Python 3.3 or newer

import os
import sys

from get_options import get_options


#CONFIGURATION#
##################
#Make adjustments here to control the file types included
file_types = list()
file_types.append(".m3u")
file_types.append(".lst")


#HELP
###################
#Help section

help_full = '''
Rename file in m3u
=======================

--old [target_string] --new [new_string]
-o [target_string] -n [new_string]

    Goes through all known types of playlist (.m3u files etc.) and changes target_string
    to new_string. Strings can be partial file names. Case sensitive.

--recursive
-r

    Include subdirectories.


--types
-t

    List known file extensions. Ignores other options except "help".


--help
-h

    Print this help menu. Ignores other options.

'''


#HELPER FUNCTIONS
###################

#Function to list known file types
def known_file_types():
    
    #Get script name
    script_name = os.path.split(sys.argv[0].rstrip("/"))[-1]
    
    print("")
    print(script_name,
          "currently updates the following file types:")
    for type in file_types:
        print(type)
    print()

#Print help 
def print_help():
    print(help_full)

###################


##OPTIONS HANDLING
###################

recursive = False # Initialising variable

#Display help if no options used
if len(sys.argv) < 2:
    print_help()
    exit()


options = get_options(sys.argv)

#Print help
if "help" in options or "h" in options:
    print_help()
    exit()

#Print known file types
if "types" in options or "t" in options:
    known_file_types()
    exit()

#Enable option to include subdirectories
if "recursive" in options or "r" in options:
    recursive = True


#Short-option 'o' same as 'old'
if "o" in options:
    options["old"] = options["o"]
    del options["o"]


if "only" in options:
    try:
        grep_string_only = options["only"]
        if playlist_name != "":
            playlist_name += "_"
        playlist_name += grep_string_only
        del options["only"]
    except:
        print("Missing argument")
        exit()
        
#Short-option 'n' same as 'new'
if "n" in options:
    options["new"] = options["n"]
    del options["n"]

if "old" not in options or "new" not in options:
    print("Option missing.\nUse the '--help' option.")
    exit()
    
if type(options["old"]) is not str or type(options["new"]) is not str:
    print("Missing or invalid argument.\nUse the '--help' option.")
    exit()

#Fail and exit if either string is empty or just whitespace.


old_str = options["old"]
new_str = options["new"]

if old_str.strip() == "" or new_str.strip() == "":
    print("ERROR: If either target_string or new_string are blank or whitespace-only,")
    print("it could lead to unexpected results. Aborting operation with no changes.\n")
    exit()


        
###################

#Counters for changes etc
changes_counter = 0
changed_files_counter = 0
warnings_counter = 0

#Get list of recognised files
#
#Start by listing all files
files = list()
if recursive is False:
    files = files + os.listdir(os.getcwd()) #Only current dir
else:
    #Include subdirectories
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
        for filename in filenames:
            files.append(dirpath + "/" + filename)


#Remove files that don't match selected types or filters
ind = 0
while ind <= len(files) - 1:
    match = False #tracks whether file matched a known extension
    for file_ext in file_types:
        if files[ind].endswith(file_ext):
            match = True
            ind = ind + 1
            break #go to next file in list
    
    #No match found, so delete file and move to next
    if match == False: del files[ind]
    #(no need to change index because files have shifted)  
            
            
#Go through listed files and make the changes
for file in files:
    this_file_changed = False
    
    temp_file = file + ".tmp"    
    fout = open(temp_file, "w")
    
    try:
        with open(file, "r") as fin:
            
            changed_file_was_reported = False

            for line in fin:
                changes_counter += line.count(old_str)
                if changed_file_was_reported is False and line.count(old_str) > 0:
                    print("Changing file: {}".format(file))
                    changed_file_was_reported = True
                    this_file_changed = True
                    
                line = line.replace(old_str, new_str)
                fout.write(line)

        fout.close()
    except:
        # when there's a problem opening/reading file
        print("WARNING: Problem with file {}".format(file))
        warnings_counter += 1

    if this_file_changed is True:
        os.replace(temp_file, file)
        changed_files_counter += 1
    else:
        os.remove(temp_file)


#Report
print("====Report====")
if warnings_counter > 0: print("Got {} warning(s)".format(warnings_counter))
print("Processed {} file(s).".format(len(files)) )
print("Made {} change(s) in {} file(s).".format(changes_counter, changed_files_counter))

    
    
