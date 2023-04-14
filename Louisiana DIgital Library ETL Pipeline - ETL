# ETL pipeline for LDL contents

You should follow steps to download LDL metadata. There are 2 main ways to do so. One requires server access, the other uses a shell script to curl down datastreams from the LDL website.


### 1)  Extract your Datasteam files (rdf, xml, obj)to a directory for the post processing later.
- ***A. Getting PidList:***</br>
     - Use lsu vpn </br>
     - ssh to lsu subnet machine</br>
     - ssh to dgi-ingest server (hosted on aws)</br>
     - `drush -u 1 islandora_datastream_crud_fetch_pids --collection="hnoc-aww:collection" --pid_file=/tmp/collection-data/hnoc-aww:collection.txt`</br>
     - `drush -u 1 idcrudfd --pid_file=/tmp/collection-data/hnoc-aww\:collection.txt --datastreams_directory=/tmp/collection-data/ds --dsid=OBJ`</br>
     - How do we identify compounds, and get their children?</br>
        - Example: https://ingest.louisianadigitallibrary.org/islandora/object/hnoc-aww%3A40/manage/</br>
        - Search for content type, Use machine name from link{1}/collection: compoundCModel, sp_pdf, sp_large_image_cmodel</br>

- ***B) Downloading the Datastream files:*** </br>
     - target collection => hnoc-awww:collection</br>
     - visit https://ingest.louisianadigitallibrary.org/islandora/object/hnoc-aww:collection/manage</br>
     - PIDS written to file /tmp/hnoc-aww-namespaced.txt 
     - after login via server and nav to drupal root (aka /var/www/data)
     - `drush -u 1 islandora_datastream_crud_fetch_pids --namespace=hnoc-aww --pid_file=/tmp/hnoc-aww-namespaced.txt`
     - `mkdir /tmp/hnoc`
     - Run these drush commands in sequence to download OBJ, RDF and MODS files:</br>
     ```
        drush -u 1 idcrudfd --pid_file=/tmp/hnoc-aww-namespaced.txt --datastreams_directory=/tmp/hnoc --dsid=OBJ </br>
        drush -u 1 idcrudfd --pid_file=/tmp/hnoc-aww-namespaced.txt --datastreams_directory=/tmp/hnoc --dsid=RELS-EXT </br>
        drush -u 1 idcrudfd --pid_file=/tmp/hnoc-aww-namespaced.txt --datastreams_directory=/tmp/hnoc --dsid=MODS </br>
     ```

     - compress the datastreams for export:</br>
     ```
        cd /tmp/hnoc</br>
        zip hnoc-data.zip *  
     ```
     - move the file to the /tmp directory so it is accessible</br>
        `mv hnoc-data.zip /tmp/`</br>
     - log out of the ingest server, back into the computer on the subnet `ctl-D`</br>
     - scp the file:</br>
        `cp dgi-ingest:/tmp/hnoc-data.zip ~/Downloads`</br>
     - CTL+D (to log out of subnet machine.)</br>
     - copy to other computes as needed.   </br>
        `cp Work:/tmp/hnoc-data.zip ~/Downloads/`</br></br>
            
### 2) Debug and Run xml2workbench tool:</br>
xml2workbench is a python script that extracts metadata from xml files, for each node in old Digital Library website. It scripted by Rosie Le Faive. However, the original python script will not work on the Louisiana Digital Library contents, adn it needs to be edited according to our need, so it could be run on all XML files to expot the metadata.</br
- ***Edit the code:*** </br>
Edit the code to fix Nan-type errors in order to have the code work on creating the right metadata fields according to LDL fields (Documentation about the steps to fix the code is on (https://github.com/Miladkhanlou/XML-to-Metadata-Tool)</br>
- ***Change the input directory:*** </br>
- ***Run the xml2workbench.py*** </br></br>

### 3) Run the metadata process tool:</br>
The metadata_process is a customized python script for processing, cleaning and fixing data on each the dataset.</br>
To learn more about how script work,s please visit: (https://github.com/Miladkhanlou/Post-Processing-Tool-For-LDL)</br></br>
### 4) Install, configure and run Islandora Workbench ingest tool: </br>
After post processing metadata, now every thing is ready to run Islandora workbench to ingest data into the new Digital Library website.
See documentation on how to install and configure isladnora workbench ingestion tool and running using bash (https://github.com/Miladkhanlou/Islandora_workbench_Ingest_tool)</br>
