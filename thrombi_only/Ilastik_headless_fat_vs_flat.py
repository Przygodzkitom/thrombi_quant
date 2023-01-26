#script launches Ilastik operation in headless mode


import os
import subprocess
from csv import reader

#grabs the paths of the folders where the images from a single channel are located
#csv file which contains these paths was created by the pipeline.py script
channel_paths_file=open(os.getcwd()+"/workingFolders_paths.csv", "r")
channel_paths=reader(channel_paths_file)


    
ilastik_location= 'C:/Program Files/ilastik-1.4.0b21/' #this line must contain the actual path to Ilastik .exe or.sh file
project_pxl_location=os.getcwd()+'/Ilastik_training/pxl.ilp'
project_obj_location=os.getcwd()+'/Ilastik_training/obj.ilp'




os.chdir(ilastik_location)


for channel in channel_paths: 
    channel_path=channel[0] + "/" 
    files=os.listdir(channel_path)
   
    for file in files: 
        #defines a call of headless pxl classification
        command1='ilastik.exe --headless --project=%s --raw_data=%s%s' %(project_pxl_location, channel_path, file) #replace 'ilastik.exe' with an appropriate executable file name depending on your system
        subprocess.call(command1, shell=True)
        file_no_ext=os.path.splitext(file)[0]#grabs the filename without extension  
        #defines a call of headless obj classification, as a prediction map it takes a file created by the previous command
        command2='ilastik.exe --headless --project=%s --export_source="Object Probabilities" --raw_data=%s%s --prediction_maps=%s%s%s' %(project_obj_location, channel_path, file, channel_path, file_no_ext, "_Probabilities.h5")#replace 'ilastik.exe' with an appropriate executable file name depending on your system
        subprocess.call(command2, shell=True)

 
    
