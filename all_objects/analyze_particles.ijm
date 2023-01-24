path=File.directory()
lineseparator = "\n";
channel_folder_paths=split(File.openAsString(path+"/workingFolders_paths.csv"), lineseparator);

for (z=0; z<channel_folder_paths.length;z++){
	
list = getFileList(channel_folder_paths[z]);

for (s=0; s<list.length; s++) {
				if(endsWith(list[s], "Predictions.tif")){  //bierze tylko tiffy z predykcjami 
						open(channel_folder_paths[z]+"/"+list[s]);
						thrombi_map=getTitle();
						
						selectWindow(thrombi_map);
						run("Invert LUT");
						setAutoThreshold("Otsu");
						run("Analyze Particles...", "size=0-Infinity add include add"); //tworzy tabelę ROI z thrombusów, zakleja dziury w trombusach
						roiManager("measure")
						
						close(thrombi_map);
						selectWindow("ROI Manager");  
						run("Close"); 
												//wyjmujemy numer zdjecia z nazwy pliku:
						split_filename=split(thrombi_map, "-"); //dzieli nazwe pliku przy -
						image_name=split_filename[1]; //bierze tę część po -
						split_filename=split(image_name, "_"); //dzieli nazwe po _
						image_name=split_filename[0]; //bierze te czesc przed _
						saveAs("Measurements", channel_folder_paths[z]+"/"+"area_FIJI_"+image_name+".csv");	
						close("area_FIJI.csv");
						close("Results");
						close("Threshold");}
																}	


												}   
     										
											
	
											
run("Quit");