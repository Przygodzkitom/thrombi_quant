#skrypt uruchamiający headless Ilastik pixel classification na plikach z folderu wskazanego przez użytkownika
#z modelu w lokalizacji wpisanej na sztywno


import os
import subprocess
from csv import reader

# pobiera z pliku txt sciezke dostepu do folderu-matki
channel_paths_file=open(os.getcwd()+"/workingFolders_paths.csv", "r")
channel_paths=reader(channel_paths_file)


    
ilastik_location= 'C:/Program Files/ilastik-1.4.0b21/'
project_pxl_location=os.getcwd()+'/Ilastik_training/pxl.ilp'
project_obj_location=os.getcwd()+'/Ilastik_training/obj.ilp'




os.chdir(ilastik_location)

# petla przechodzaca przez liste sciezek folderow z kanałami pobrana z pliku csv
for channel in channel_paths: 
    channel_path=channel[0] + "/" #sciezka dostepu odczytana jako str z list
    files=os.listdir(channel_path)
   
    for file in files: 
        
        command1='ilastik.exe --headless --project=%s --raw_data=%s%s' %(project_pxl_location, channel_path, file) # definiuje wywołanie headless pxl classification
        subprocess.call(command1, shell=True)# wywoluje powyższe
        file_no_ext=os.path.splitext(file)[0]#potrzebna nazwa pliku bez rozszerzenia 
        #teraz definiuje wywolanie headless obj classification, jako prediction map bierze plik ktory zrobil po wywolaniu poprzedniej komendy
        command2='ilastik.exe --headless --project=%s --export_source="Object Probabilities" --raw_data=%s%s --prediction_maps=%s%s%s' %(project_obj_location, channel_path, file, channel_path, file_no_ext, "_Probabilities.h5")
        subprocess.call(command2, shell=True)

 
    
