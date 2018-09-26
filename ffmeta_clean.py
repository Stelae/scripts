#!/usr/bin/python3
#
#Clean metadata fron all mp4 files in folder using ffmpeg.
#
#Requires minimum version 3.3 (for the os.replace() function)


import os
from shutil import which

warn_counter = 0 #Count warnings for reporting
file_counter = 0 #Count files processed for reporting

#Check if ffmpeg installed
package = "ffmpeg"
if which(package) is None:
    print("Could not find", package, "in path. Please check that it is installed.")
    print("No action taken")
    exit()


#Get list of mp4 files
file_ext = ".mp4"
files = [] #list of mp4 files
all_files = os.listdir()
for filename in all_files:
    if filename.endswith(file_ext):
        files.append(filename)
        
#del all_files #Note: patchwork to fix bug

if len(files) < 1:
    print("WARNING: No", file_ext, "files have been found.")


#Run ffmpeg to strip metadata for each file, but don't overwrite existing files
###########################################

for filename in files:
    temp_file = "_".join( ("temp",filename) )
    ffmpeg_parameters = { "input_file": filename,
                          "output_file": temp_file
                          }
    
    #Check if output_file already exists to not overwrite
    if os.path.isfile(ffmpeg_parameters["output_file"]):
        print("WARNING: Failed to process", filename)
        print("Skipping to next file\n")
        warn_counter = warn_counter + 1
        continue


    #Write to temp file and replace original
    ########################################
    #FFMpeg parmeter explanation:
    #-nostdin: non-interactive (because we are directing output to file,
    #   so questions would be invisible otherwise).
    #-i [file]: input file
    #-map_metadata -1: removes all metadata (note: some metadata cannot be removed.
    #-c copy: make direct copy (no encoding)
    #-shortest: if streams have different length, crop to shortest
    ######################
    
    ffmpeg_cmd = 'ffmpeg -nostdin -i "%(input_file)s" -map_metadata -1 -c copy \
    "%(output_file)s" >> ffmpeg_output.log 2>&1' % ffmpeg_parameters
    #Note: Using double quotes around file names because if a filename contains
    #a single quote (apostrophe), it causes an error.

    try:
        error = os.system(ffmpeg_cmd + " >> ffmpeg_output.log") #ffmpeg should return 0 if it worked
    except:
        print("WARNING: Something went wrong when trying to execute ffmpeg on",
              filename
              )
        print("Skipping to next file\n")
        warn_counter = warn_counter + 1
        continue
    
    if error:
        print("WARNING: ffmpeg failed to process", filename)
        print("Skipping to next file\n")
        warn_counter = warn_counter + 1
        continue
    else:
        file_counter = file_counter + 1
        
     
    try:
        os.replace(temp_file, filename)
    except:
        print("WARNING: Could not update",
              filename,
              "; possible permissions problem."
              )
        print("Processed output saved as", temp_file)
        print("\n")
        warn_counter = warn_counter + 1


#Reporting
###########
print("Finished. Script processed", file_counter, "files.")
if warn_counter > 1:
    print("There were", warn_counter, "warnings.")
elif warn_counter == 1:
    print("There was", warn_counter, "warning.")
else:
    print("There were no warnings.")
    
