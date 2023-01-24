#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 08:47:57 2021

@author: tomasz
"""
import tkinter as tk
from tkinter import filedialog as fd 
import subprocess
import os
import pandas as pd
from pathlib import Path
import psutil




def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;






def callback(): #funkcja wykonujaca wybor folderu-matki 
    global selected_folder_path
    selected_folder_path = fd.askdirectory() #pobiera sciezke folderu
tk.Button(text='Choose directory', command=callback).pack(fill=tk.X)#tworzy przycisk ktory wywoluje f-cje callback
tk.mainloop()

channelFolder_path_list=[]     #creates list to which folder paths will be appended
parentFolder_path_list=[]

#loop to create list of folders which contain images from a single channel
for (path, dir, files) in os.walk(selected_folder_path):
    if not dir:  # if "dir" list empty, meaning that the folder is the last in the tree and contains only files
        channelFolder_path_list.append(path)    # append path of this folder to the list

df = pd.DataFrame(channelFolder_path_list)    # list of paths to dataframe
df.to_csv('workingFolders_paths.csv', index=False, header=False)  # dataframe saved to csv file in the folder from which the script was launched

script_path=os.getcwd()+"\\czi_to_tif.ijm" #checks a path from which the script was run and creates a path were macro is located

# odpalamy makro ImageJ przerabiajace czi do tif i robiace preprocessing
# makro musi byc umieszczone w katalogu makr ImageJ w tej lokalizacji z ktorej jest uruchamiany ImageJ
# warto zmienic zeby ImageJ byl odpalany w headless
cmd = ["C:\\Program Files\\Fiji.app\\ImageJ-win64.exe","-macro",script_path]
process = subprocess.Popen(cmd)


while checkIfProcessRunning('ImageJ-win64'): 
   
   print("FIJI at work")
   
#  odpalam skrypt pythona uruchamiający Ilastika
print("Now we start Ilastik")
os.system('Ilastik_headless_fat_vs_flat.py')


# odpalamy makro ImageJ przerabiajace obliczające pola na postawie predykcji Ilastika
# makro musi byc umieszczone w katalogu makr ImageJ w tej lokalizacji z ktorej jest uruchamiany ImageJ
# warto zmienic zeby ImageJ byl odpalany w headless
script_path=os.getcwd()+"\\area_thrombi.ijm" #checks a path from which the script was run and creates a path were macro is located
cmd = ["C:\\Program Files\\Fiji.app\\ImageJ-win64.exe","-macro",script_path]
process = subprocess.Popen(cmd)

while checkIfProcessRunning('ImageJ-win64'): 
   
   print("FIJI at work")
   
#  odpalam skrypt pythona uruchamiający Ilastika
print("Now we start summary")

#loop to create list of folders which contain folders with images from single channel
#The path to such folder is needed because the script summarizes data for all channels in a single file
#which is located in the folder in which subfolders with channels are contained
for (path, dir, files) in os.walk(selected_folder_path):
    
    if not dir:  # if "dir" list empty, meaning that the folder is the last in the tree and contains only files
        path = Path(path)
        parentFolder_path=path.parent.absolute()
        if not parentFolder_path in parentFolder_path_list: # it has to list the parent folder only once
            parentFolder_path_list.append(parentFolder_path)    # append path of this folder to the list

df = pd.DataFrame(parentFolder_path_list)    # list of paths to dataframe
df.to_csv('parentFolders_paths.csv', index=False, header=False)  # dataframe saved to csv file in the folder from which the script was launched
os.system('results_summary.py')
