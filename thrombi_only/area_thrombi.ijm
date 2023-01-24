//Macro ktore dziala na plikach wynikowych Ilastika w ktorych sa dwie klasy obiektow. Kazdy taki wynikowy tiff ma dwa kanaly z prawdopodobienstwami dla obu klas przeliczonymi na skale 0-255
//Kanaly trzeba rozdzielic i wziac ten ktory nas interesuje lub oba
path=File.directory()
lineseparator = "\n";
channel_folder_paths=split(File.openAsString(path+"/workingFolders_paths.csv"), lineseparator);



last_row=0; //zmienna potrzebna w pętli dodawania nazwy treatmentu

for (s=0; s<channel_folder_paths.length; s++) {  // pętla do otwierania podfolderow  
	    
list = getFileList(channel_folder_paths[s]);
			
			for (a=0; a<list.length; a++){ //pętla do przeglądania plików
					
					if(endsWith(list[a], "Probabilities.tif")){  //bierze tylko tiffy z predykcjami obiektów	
						open(channel_folder_paths[s]+"/"+list[a]);
						run("Split Channels");
						active_windows = getList("image.titles");  //pobiera listę aktywnych okien
						for(i = 0;i<active_windows.length;i++){	//pętla do wybrania z aktywnych okien tego które zawiera mapę probability thrombusow (w tym przypadku ma w nazwie C2)
							if(matches(active_windows[i],".*C1.*")){
								selectWindow(active_windows[i]);
								thrombi_map=active_windows[i];
							}
							if(matches(active_windows[i],".*C2.*")){
								close(active_windows[i]);
							
							}
						}


//wyjmujemy numer zdjecia z nazwy pliku:
split_filename=split(thrombi_map, "-"); //dzieli nazwe pliku przy -
image_name=split_filename[2]; //bierze tę część po -
split_filename=split(image_name, "_"); //dzieli nazwe po _
image_name=split_filename[0]; //bierze te czesc przed _

//setAutoThreshold("Default dark");
selectWindow(thrombi_map);
setThreshold(128, 255); //proguje obiekty ktore maja probability 0.5 ze sa thrombusami (128, bo Ilastik generuje tiff gdzie probability 0-1 przeliczone na 0-255)

//setOption("BlackBackground", true);
//run("Convert to Mask");


run("Analyze Particles...", "size=0-Infinity add include add"); //tworzy tabelę ROI z thrombusów, zakleja dziury w trombusach

// if image empty, Analazye Particles does not make analysis, roiManager is empty and does not produce csv file
// to solve this, the part after "if" generates csv with zeroes
if (roiManager("Count") == 0){
	 columns = 13;
  rows = 1;
  run("Clear Results");
  table_headers=newArray("Area", "X", "Y", "Perim.", "Circ.","Feret", "FeretX", "FeretY", "FeretAngle", "MinFeret", "AR", "Round", "Solidity");
  
  for (col=1; col<=columns; col++) {
     for (row=0; row<rows; row++) {
        data = 0;
        start=col-1;
        end=start+1;
        header=Array.slice(table_headers, start, end);
        setResult(header[0], row, data); //
     }
  }

	saveAs("Measurements", channel_folder_paths[s]+"/"+"area_FIJI_"+image_name+".csv");
}


roiManager("measure");



close(thrombi_map);
selectWindow("ROI Manager");  
run("Close"); 

						
saveAs("Measurements", channel_folder_paths[s]+"/"+"area_FIJI_"+image_name+".csv");	
close("area_FIJI.csv");
close(thrombi_map);
close("Results");
close("Threshold");
}	


}   
     
     
}
run("Quit");
