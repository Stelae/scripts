#!/usr/bin/python3

#Short script that takes a text file containing a "messy" (copy-pasted from cli)
#list of installed packages and converts it to a neat list
#Files must be in the directory of the script.


import os

fname_in = "packages.txt"
fname_out = "out.txt"


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
#if os.path.isfile(fname_out):
    #print("File", fname_out, "already exists. Aborting operation")
    #exit()

fout = open(fname_out, "w")

for package in packages:
    fout.write(package + "\n")
    
#Another copy of the list without line breaks
fout.write("\n\n") #Spacing between copies of list
for package in packages:
    fout.write(package + " ")

fout.close()