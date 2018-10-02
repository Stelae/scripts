#!/bin/env/python3

#Perform "volumedetect" with ffmpeg on all files
 
import os
from shutil import which

warn_counter = 0 #Count warnings for reporting
file_counter = 0 #Count files processed for reporting

#Check if ffmpeg installed
package = "ffmpeg"
if which(package) is None:
    print("Could not find", package,
          "in path. Please check that it is installed.")
    print("No action taken")
    exit()


#CONFIGURATION#
##################
#Make adjustments here to control the file types included
file_types = list()
file_types.append(".mp4")
file_types.append(".webm")
file_types.append(".3gp")
file_types.append(".mkv")
file_types.append(".avi")


#MAIN#
##################

#Get list of known files
files = [] #list of mp4 files
for file_ext in file_types:
    all_files = os.listdir()
    for filename in all_files:
        if filename.endswith(file_ext):
            files.append(filename)


#ffmpeg -i "Marsha May - Slut Puppies 10 (part 4).mp4" -af "volumedetect" -vn -sn -dn -f null /dev/null
#ffmpeg -i "Chloe Amour - DP Masters 5 (part 3)" -af "volumedetect" -vn -sn -dn -f null /dev/null


########################################
#FFMpeg parmeter explanation:
#-nostdin: non-interactive (because we are directing output to file,
#   so questions would be invisible otherwise).
#-i [file]: input file
#-af: apply audio filter
#-vn: don't include default video stream
#-sn: don't include default subtitle stream
#-dn: don't include default data stream
#-f: force input or output file format    
######################



for file in files:
    
    ffmpeg_cmd = 'ffmpeg -nostdin -i "{0}" -af "volumedetect" \
    -vn -sn -dn -f null /dev/null > "{0}.log" 2>&1'.format(file)
    
    #cat_cmd = 'ls'
    cat_cmd = 'cat "{0}.log" | grep "max_volume"'.format(file)
    #Note: Using double quotes around file names because if a filename contains
    #a single quote (apostrophe), it causes an error.


    print('Processing "{0}"'.format(file))

    try:
        error = os.system(ffmpeg_cmd)
        #ffmpeg should return 0 if it worked
    except:
        print("WARNING: Something went wrong when trying to execute ffmpeg on",
                filename
                )
        print("Skipping to next file\n")
        warn_counter = warn_counter + 1
        continue
    
    error = error + os.system(cat_cmd)

    if error:
        print("WARNING: Error while processing", filename)
        print("")
        warn_counter = warn_counter + 1
        continue
    else:
        file_counter = file_counter + 1
    
    
    print("")

    
    
    
    
    

