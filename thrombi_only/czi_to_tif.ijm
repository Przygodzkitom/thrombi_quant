path=File.directory()
lineseparator = "\n";
channel_folder_paths=split(File.openAsString(path+"/workingFolders_paths.csv"), lineseparator);

for (z=0; z<channel_folder_paths.length;z++){
	
list = getFileList(channel_folder_paths[z]);

for (s=0; s<list.length; s++) {
	
open(channel_folder_paths[z]+"/"+list[s]);



run("Subtract Background...", "rolling=50");
saveAs("tiff",channel_folder_paths[z]+"/"+list[s]);
File.delete(channel_folder_paths[z]+"/"+list[s]);
close(); 
          }
     }


run("Quit");