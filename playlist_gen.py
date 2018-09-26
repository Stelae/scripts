#!/usr/bin/python3
#Generate a playlist for VLC from the relevant files in the folder
#If file exists, it's overwritten

import os

#CONFIGURATION#
##################
#Make adjustments here to control the file types included
file_types = list()
file_types.append(".mp4")
file_types.append(".webm")
file_types.append(".3gp")
file_types.append(".mkv")

#Pre-fix
prefix = "./"

#Output file
#playlist_name = "playlist"
playlist_ext = "m3u"
playlist_name = os.getcwd().split("/")[-1] #Name of current directory

#Output file prefix (to bring to top of files).
#Comment out to disable the prefix.
outfile_prefix = "0-"


#MAIN
###################

#Get list of recognised files
files = os.listdir() #Start by listing all files

#Remove files that don't match selected types
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
    #(no need to change index because files  have shifted)        
    

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