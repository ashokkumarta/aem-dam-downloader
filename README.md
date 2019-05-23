# aem-dam-downloader							
Script to download all the assets under the specified path(s) in AEM to a local folders, preserving the same folder structure in the local 

## Dependencies
```
Python 3.7
```

## Usage

Update the configuration in the json file config/config.json and run the download script 
```
python scripts/asset-download.py
```

### Folder structure
```
scripts - contains the script and dependent libraries for this download utility
config - Has a single json configuration file - config.json which holds all the configuration for the download
output - outputs folder. This folder contains the output files  
logs - log files folder. This folder has all the logs generated
download - Assets are downloaded to this folder 
```

###Configuration to change in config.json
```
cq_host - Host name of the AEM instance to connect to 
cq_port - Port number of the AEM instance
cq_user - User ID to connect to the AEM Instance	
cq_password - Password of the AEM User ID
base_paths - List of paths from which assets needs to be downloaded
time_wait_secs - Time delay in secs between each download 
```

###Output files
```
output/successful_assets.lst - List of assets which are downloaded successfully
output/failed_assets.lst - List of assets for which download failed
```

###How to run
Before starting the batch run, ensure
+ Correct configurations are done in the config.json file 
+ download, output and log folders containing data if any from previous run are backed up (if needed) and contents of these folders cleared.  

After the above points are checked, run the script scripts/asset-download.py by executing the below command 
```
python scripts/asset-download.py 
```

###Checking the status of the run
The progress and the status summary of the migration run is displayed on the console. 
Detailed logging is also done to check and validate the migration. 
The following log files can be referred for debugging
+ logs/status.log - Overall summary of the migration run
+ logs/trace.log - Detaied track on the migration run, including the details of the assets download status
+ logs/error.log - Error details about the migration failures
The following output files can be checked to find the details of the assets downloaded vs. failed
+ output/successful_assets.lst - List of assets which are downloaded successfully
+ output/failed_assets.lst - List of assets for which download failed

## Reservation
> These scripts are created for specific use cases. Make sure its tested for your scenario before applying it for production purpose

---
> Environment Tested on:  AEM 6.1, 6.2 & 6.4 | Windows, RHEL5 | Python 3.7.2

