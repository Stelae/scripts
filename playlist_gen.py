#!/usr/bin/python3
#Generate a playlist for VLC from the relevant files in the folder
#If file exists, it's overwritten

import os
import sys

from get_options import get_options

#CONFIGURATION#
##################
#Make adjustments here to control the file types included
file_types = list()
file_types.append(".mp4")
file_types.append(".webm")
file_types.append(".3gp")
file_types.append(".mkv")
file_types.append(".avi")

#Pre-fix
prefix = "./"

#Output file
#playlist_name = "playlist"
playlist_ext = "m3u"
playlist_name = os.getcwd().split("/")[-1] #Name of current directory

#Output file prefix (to bring to top of files).
#Comment out to disable the prefix.
outfile_prefix = "0-"


#HELP
###################
#Help section

help_full = '''
Playlist Generator v1.1
=======================

[no options]

    Generate a playlist of known file types in the current directory


--only [search_string]
-o [search_string]

    List only includes files with [search_string] in their names.
    Case insensitive. Is overriden by an "except" match.
    

--except [search_string]
-x [search_string]

    List excludes files with [search_string] in their names.
    Case insensitive. Takes precedence over an "only" match.


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
    print(sys.argv[0],
          "currently looks for the following extensions:")
    for type in file_types:
        print(type)
    print()

#Print help 
def print_help():
    print(help_full)

###################



#MAIN
###################
grep_string_only = ""
grep_string_x = "*"


#Check for options

recursive = False # Initialising variable

if len(sys.argv) > 1:
    
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

    
    #Short-option 'o' same as 'only'
    if "o" in options:
        options["only"] = options["o"]
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
            

    #Short-option 'x' same as 'except'
    if "x" in options:
        options["except"] = options["x"]
        del options["x"]
    
    if "except" in options:
        try:
            grep_string_x = options["except"]
            if playlist_name != "":
                playlist_name += "_"
            playlist_name += "No_" + grep_string_x
            del options["except"]
        except:
            print("Missing argument")
            exit()
        
            

#Get list of recognised files
#
#Start by listing all files
files = list()
if recursive is False:
    files = files + os.listdir() #Only current dir
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
        if files[ind].endswith(file_ext) \
            and grep_string_only.casefold() in files[ind].casefold() \
            and grep_string_x.casefold() not in files[ind].casefold():
            #Note: casefolded strings are used for caseless matching
            match = True
            ind = ind + 1
            break #go to next file in list
    
    #No match found, so delete file and move to next
    if match == False: del files[ind]
    #(no need to change index because files  have shifted)        
    
#If playlist is empty, exit with message
if len(files) < 1:
    print("\nWARNING: Playlist would be empty. No files generated.\n")
    exit()


#Sort files alphabetically, ignoring case
files.sort(key=str.lower)

#Write list to file
playlist_name = playlist_name + "." + playlist_ext #add extension
if outfile_prefix: #add prefix to file name if it exists
    playlist_name = outfile_prefix + playlist_name

fout = open(playlist_name, "w") #Overwrite

for filename in files:
    filepath = os.path.relpath(filename, "./")
    fout.write(prefix + filepath + "\r\n")

fout.close()
