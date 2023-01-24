#prompts user to open cvs file
#extracts data from 'Intensity_IntegratedIntensity_vWF' column
#calculates mean and median and prints histogram form this column
#creates DataFrame with Mean and Median

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from csv import reader

# pobiera z pliku txt sciezke dostepu do folderu-matki
day_paths_file=open(os.getcwd()+"/parentFolders_paths.csv", "r")
day_paths=reader(day_paths_file)



# petla przechodzaca przez liste sciezek folderow z czipami pobrana z pliku csv
for a in day_paths: 
    folder_path=a[0] #kolejny element listy, ale tylko jeden wiec zawsze o numerze 0
    results_file=pd.ExcelWriter(folder_path+'/Results_area_from_FIJI.xls') #plik z zestawieniem wyników dla calego czipa
    list_of_channels=os.listdir(folder_path) #listuje zawartosc folderu czyli foldery z nazwami kanałów
    list_of_channels.sort() #porządkuje numery kanałów, bo python domyślnie układa je randomowo
    for element_in_folder in list_of_channels: #pętla przechodząca przez kolejne folder
            element_in_folder_path=folder_path+'/'+element_in_folder#sciezka dostepu do kazdego pliku lub katalogu w folderze z pomiarami
            if os.path.isdir(element_in_folder_path): #sprawdza czy element w katalogu glownym jest katalogiem, żeby sie nie zawieszal jak w katalogu glownym bedzie tez jakis plik
                channel_number=element_in_folder
                channel_path=element_in_folder_path #sciezka dostepu do folderu kanalu
                writer = pd.ExcelWriter(channel_path+'/Results_area_from_FIJI.xls')#tworzy plik excela do ktorego beda zapisywane wyniki dla kazdego kanalu
                channel_results=pd.DataFrame()#tworzy dataframe do ktorego beda wklejane wyniki z wszystkich plikow z danego kanalu
                list_of_measurements=os.listdir(channel_path) #listuje zawartosc folderu czyli pliki
                list_of_measurements.sort() #porządkuje numery zdjec, bo python domyślnie układa je randomowo
                for measurement_file in list_of_measurements: #listuje zawartosc folderu z plikami csv
                    filename, file_extension = os.path.splitext(measurement_file) 
                    if 'area_FIJI' in filename: #sprawdza czy nazwa pliku zawiera 'area_FIJI' bo w folderze sa tez inne pliki
                        if file_extension==".csv": #sprawdza czy plik jest csv, bo sa tez inne zawierajace area_FIJI' w nazwie
                            measurement_file_path=channel_path+'/'+ measurement_file #sciezka dostepu do pliku csv
                            table=pd.read_csv(measurement_file_path,delimiter=',') #wczytanie pliku csv do DataFrame
                            area=table['Area'] #wczytanie kolumny do tabeli
                            perimeter=table['Perim.']
                            circularity=table['Circ.']
                            feret=table['Feret']
                            sum_area=area.sum()
                            mean_area=area.mean() #liczenie mean z tabeli
                            median_area=area.median()#liczenie median z tabeli
                            mean_perimeter=perimeter.mean() #liczenie mean z tabeli
                            median_perimeter=perimeter.median()#liczenie median z tabeli
                            mean_circularity=circularity.mean() #liczenie mean z tabeli
                            median_circularity=circularity.median()#liczenie median z tabeli
                            mean_feret=feret.mean() #liczenie mean z tabeli
                            median_feret=feret.median()#liczenie median z tabeli
                            ar=np.array([[mean_area,median_area,sum_area,mean_perimeter,median_perimeter,mean_circularity,median_circularity,mean_feret,median_feret]])#wczytanie mean i median do array
                            split_filename=filename.split(sep="_") #pozyskujemy numer zdjecia z nazwy pliku, najpierw tniemy przy '_', dostajemy array z stringami
                            image_number=split_filename[2] # teraz bierzemy trzeci element z arraya, bo tam jest numer zdjecia
                            df = pd.DataFrame(data=ar, index=[image_number], columns=["Mean_Area","Median_Area","Sum_Area","Mean_Perimeter","Median_Perimeter","Median_Circularity","Mean_Circularity","Mean_Feret","Median_Feret"])#wczytanie array do DataFrame
                            channel_results=channel_results.append(df)
                            df.to_excel(writer, sheet_name=filename)
                            histogram=table['Area'].plot(kind='hist', title='Area', range=[0, 1000])#rysuje histogram
                            histogram_path=channel_path+'/'+filename+'histogram.eps'
                            plt.savefig(histogram_path)
                            plt.close(fig=None)  #bez tego dane z kolejnych kanalow dopisuja sie do kolejnych figur w petli
                channel_mean_area_mean=channel_results.loc[:,'Mean_Area'].mean() #liczy srednia ze srednich ze zdjec
                channel_median_area_mean=channel_results.loc[:,'Median_Area'].mean() # liczy srednia z median ze zdjec
                channel_area_mean=channel_results.loc[:,'Sum_Area'].mean() # liczy srednia z powierzchni ze zdjec
                channel_mean_perimeter_mean=channel_results.loc[:,'Mean_Perimeter'].mean() #liczy srednia ze srednich ze zdjec
                channel_median_perimeter_mean=channel_results.loc[:,'Median_Perimeter'].mean() # liczy srednia z median ze zdjec
                channel_mean_circularity_mean=channel_results.loc[:,'Mean_Circularity'].mean() #liczy srednia ze srednich ze zdjec
                channel_median_circularity_mean=channel_results.loc[:,'Median_Circularity'].mean() # liczy srednia z median ze zdjec
                channel_mean_feret_mean=channel_results.loc[:,'Mean_Feret'].mean() #liczy srednia ze srednich ze zdjec
                channel_median_feret_mean=channel_results.loc[:,'Median_Feret'].mean() # liczy srednia z median ze zdjec
                channel_means=pd.DataFrame(data=[[channel_mean_area_mean,channel_median_area_mean,channel_area_mean,channel_mean_perimeter_mean,channel_median_perimeter_mean,channel_mean_circularity_mean,channel_median_circularity_mean,channel_mean_feret_mean,channel_median_feret_mean]], index=["Mean"], columns=["Mean_Area","Median_Area","Sum_Area","Mean_Perimeter","Median_Perimeter","Mean_Circularity","Median_Circularity","Mean_Feret","Median_Feret"]) #tworzy dataframe z tymi srednimi
                channel_results=channel_results.append(channel_means) #dodaje ten dataframe do czastkowych
                channel_results.to_excel(results_file, sheet_name=channel_number)
                writer.close()      
    results_file.close()
