
path=File.directory()
lineseparator = "\n";
channel_folder_paths=split(File.openAsString(path+"/workingFolders_paths.csv"), lineseparator);



last_row=0; 

for (s=0; s<channel_folder_paths.length; s++) {  // loop to open subfolders  
	    
list = getFileList(channel_folder_paths[s]);
			
			for (a=0; a<list.length; a++){ //loop to go through the files
					
					if(endsWith(list[a], "Probabilities.tif")){  	
						open(channel_folder_paths[s]+"/"+list[a]);
						run("Split Channels");//.tif file consists of two probability maps: C1-probability that object is solid thrombus, C2-that it belongs to the other class
						active_windows = getList("image.titles");  
						for(i = 0;i<active_windows.length;i++){	
							if(matches(active_windows[i],".*C1.*")){ //selects window with a probability map that objects are solid thrombi
								selectWindow(active_windows[i]);
								thrombi_map=active_windows[i];
							}
							if(matches(active_windows[i],".*C2.*")){
								close(active_windows[i]);
							
							}
						}


//extract image number form a filename
split_filename=split(thrombi_map, "-"); //dzieli nazwe pliku przy -
image_name=split_filename[2]; //bierze tę część po -
split_filename=split(image_name, "_"); //dzieli nazwe po _
image_name=split_filename[0]; //bierze te czesc przed _


selectWindow(thrombi_map);
setThreshold(128, 255); //threshold objects with the probability of being solid thrombi higher than 0.5
						//i.e. higher than 128 after renormalisation from 0-1 range to 0-255



run("Analyze Particles...", "size=0-Infinity add include add"); 

// if image is empty, Analazye Particles does not make analysis, roiManager is empty and does not produce csv file
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
