# Metadata To csv Python script
The script created to prepare a csv sheet to run the Islandora Workbench to import relational data from the old Louisiana Digiatal Library to the new website. It starts with the initial CSV metadata made created from xml files from the website. It has two stages:
### 1) creating needed columns and drops the unwanted fields from Metadata.
- a) In the first step, the script gets the metadata csv and uses existance of OBJ files in the directory, and process them to generate a right pattern for file column according to existance of those OBJ data for each node.
- b) Next, it will create needed columns such as file, field_weight, field_member_of and adds those file directory patters to the file columns according for each node(webpage).
- c) Also, it drops unwanted columns that are not in Drupal default. the existance of these columns will stop workbench process as these fields do not exist in Drupal. 

### 2) Processing the RDF files to write down the relationships(parent and children pages)
- 1) With itterring into the file directory, and ittering into .RDF files, the script uses tags, attributes and texts in RDF and cleans their name in a order that drupal can understand it.
- 2) Using three main tags inside the RDFs, which determine the relationship between nodes, parent_id column can be filled out. Having information about relationships is crutial in the Workbench data ingestion stage. 
- 3) Also, with ittering trhough RDFs we get the currect information about field_weight, which indicates order of children pages.
- 4) Finally, we will fill populate parent_id and field_weight column using processed data and export it into the CSV file.
