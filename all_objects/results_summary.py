

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from csv import reader

#grabs paths of folders with single experiments froma file created by pipeline.py
day_paths_file=open(os.getcwd()+"/parentFolders_paths.csv", "r")
day_paths=reader(day_paths_file)



#loop which goes through experiment folders
for a in day_paths: 
    folder_path=a[0]
    results_file=pd.ExcelWriter(folder_path+'/Results_area_from_FIJI.xls') #create an excel file which will contain results from an experiment folder
    list_of_channels=os.listdir(folder_path) #lists folders containing results of individual channels
    list_of_channels.sort() #organizes folder names in an order because listdir gives a random order
    for element_in_folder in list_of_channels: #loop which goes through folders containing results of individual channels
            element_in_folder_path=folder_path+'/'+element_in_folder#path to each file or folder in experiment folder
            #in experiment folder there are channel folders and .xls result file created in line 18                                                                                            
            if os.path.isdir(element_in_folder_path): #code below is to work on channel folders, therefore it must skip the .xls file
                channel_number=element_in_folder
                channel_path=element_in_folder_path
                writer = pd.ExcelWriter(channel_path+'/Results_area_from_FIJI.xls')#creates an .xls file to combine data from all images in this channel
                channel_results=pd.DataFrame()#data frame to combine the results from this channel
                list_of_measurements=os.listdir(channel_path) #lists all files in channel folder
                list_of_measurements.sort() #sorts the files by names
                for measurement_file in list_of_measurements: #loop to go through the files in the channel folder
                    filename, file_extension = os.path.splitext(measurement_file)#splits filename and its extension
                    if 'area_FIJI' in filename: #to select files with 'area_FIJI' in their names 
                        if file_extension==".csv": #to select .csv files i.e. files containing measured parameters
                            measurement_file_path=channel_path+'/'+ measurement_file #path to the .csv file with measured parameters
                            table=pd.read_csv(measurement_file_path,delimiter=',') #reads .csv file to DataFrame
                            area=table['Area'] #reads Area column from .csv file
                            perimeter=table['Perim.']
                            circularity=table['Circ.']
                            feret=table['Feret']
                            sum_area=area.sum() #summarizes area of objects in the image
                            mean_area=area.mean() #calculates mean area from the image
                            median_area=area.median()#calculates mean area from the image
                            mean_perimeter=perimeter.mean() 
                            median_perimeter=perimeter.median()
                            mean_circularity=circularity.mean() 
                            median_circularity=circularity.median()
                            mean_feret=feret.mean() 
                            median_feret=feret.median()
                            ar=np.array([[mean_area,median_area,sum_area,mean_perimeter,median_perimeter,mean_circularity,median_circularity,mean_feret,median_feret]])#writes means and medians to array
                            split_filename=filename.split(sep="_") #to grab image number from the filename we first splt at "_", we get an array with 'area', 'FIJI', image number
                            image_number=split_filename[2] #take the third element in the array i.e. image number
                            df = pd.DataFrame(data=ar, index=[image_number], columns=["Mean_Area","Median_Area","Sum_Area","Mean_Perimeter","Median_Perimeter","Median_Circularity","Mean_Circularity","Mean_Feret","Median_Feret"])#reading the array to dataframe
                            channel_results=channel_results.append(df)#appends dataframe with results from the image to dataframe combining results of individual images in the channel
                            df.to_excel(writer, sheet_name=filename)#writes results from individual image to excel file which summarizes data from this channel
                            histogram=table['Area'].plot(kind='hist', title='Area', range=[0, 1000])#draws a histogram of area distribution in the image
                            histogram_path=channel_path+'/'+filename+'histogram.eps'
                            plt.savefig(histogram_path)
                            plt.close(fig=None)  
                channel_mean_area_mean=channel_results.loc[:,'Mean_Area'].mean() #calculates mean of mean area values in particular images in the channel
                channel_median_area_mean=channel_results.loc[:,'Median_Area'].mean() #calculates mean of median area values in particular images in the channel
                channel_area_mean=channel_results.loc[:,'Sum_Area'].mean() #calculates mean value of summarized areas in particular images in the channel
                channel_mean_perimeter_mean=channel_results.loc[:,'Mean_Perimeter'].mean() 
                channel_median_perimeter_mean=channel_results.loc[:,'Median_Perimeter'].mean() 
                channel_mean_circularity_mean=channel_results.loc[:,'Mean_Circularity'].mean() 
                channel_median_circularity_mean=channel_results.loc[:,'Median_Circularity'].mean()
                channel_mean_feret_mean=channel_results.loc[:,'Mean_Feret'].mean() 
                channel_median_feret_mean=channel_results.loc[:,'Median_Feret'].mean() 
                #create dataframe with the above calculated means
                channel_means=pd.DataFrame(data=[[channel_mean_area_mean,channel_median_area_mean,channel_area_mean,channel_mean_perimeter_mean,channel_median_perimeter_mean,channel_mean_circularity_mean,channel_median_circularity_mean,channel_mean_feret_mean,channel_median_feret_mean]], index=["Mean"], columns=["Mean_Area","Median_Area","Sum_Area","Mean_Perimeter","Median_Perimeter","Mean_Circularity","Median_Circularity","Mean_Feret","Median_Feret"]) 
                channel_results=channel_results.append(channel_means) #appends this dataframe with mean values to the dataframe which contains values for individual images
                channel_results.to_excel(results_file, sheet_name=channel_number)#writes this dataframe to excel file which summarizes data from experiment folder
                                                                                #sheet name is a channel number
                writer.close()      
    results_file.close()
