from dataclasses import replace
from fileinput import filename
import pandas as pd
import xml.etree.ElementTree as ET
import glob
from os import listdir , sep, path
import os

###### Getting a Directory path with Data/"CollectionName" ######
Paths = "Data/"
OBJ_paths = []
RDF_paths = []
for filenames in os.listdir(Paths):
    OBJ_paths.append(filenames) #EDIT >>> We will not concat the fileNames with the path! Only use the path if we wantour data in the separate folders
    RDF_paths.append(Paths) #EDIT >>> For second part, RDF processing
# print("These are all the files we use to process rdfs and OBJS: \n{}".format(OBJ_paths))
# print("------------------------------------------------")

###### Getting a Collection name ######
files = listdir('csv/')
files.sort()
direct = []
for file in files:
    if file.endswith(".csv"):
        direct.append(file)
# print("This will be the initial CSV Metadata,which is xml2workbench output, we use to process: \n{}".format(direct))
# print("------------------------------------------------")

#################### 2) Getting data and fill the file column if files exist in the Data directory ########################
def input_directory(directory, OBJS):
    Collection = directory.split(".")[0]
    LDLdf = pd.DataFrame(pd.read_csv(directory))
    LDLdf.rename(columns= {'PID' : 'id'},  inplace = True)
    coll_name = []
    coll_num = []
    fileName = []
    id_to_list = LDLdf["id"].tolist() ###Putting the elements of id column to a list###
    for IDs in id_to_list:
        splitted_IDs= IDs.split(':')
        coll_name.append(splitted_IDs[0])
        coll_num.append(splitted_IDs[1])
    for s in range(len(coll_name)):
        fileName.append("{}_{}_OBJ".format(coll_name[s], coll_num[s]))
    ObjFiles = [] #getting the names of the OBJ FILES 
    fileformat = "" #getting the file type of OBJ FILES
    
    # FILES = os.listdir(OBJS)         #EDIT >>>Do not need to get into the folder as we will not have folders
    for file in OBJ_paths:
        if "OBJ" in file:
            ObjFiles.append(file.split(".")[0])
            fileformat =  ".{}".format(file.split(".")[1])

    #Filling the file_column list to fill the file column:
    file_column = []
    for fileNames in fileName:
        if fileNames in ObjFiles:
            file_column.append("Data/{}{}".format(fileNames,fileformat)) #EDIT >>> deleted Collection form formating the name because we do not have a folder consist of data for each collection
        else:
            file_column.append("")
    # print("This will be concat of the the name of File column generated for the files that are Objects: \n{}".format(file_column))
    # print("------------------------------------------------")


    LDLdf["file"] = file_column
    del fileformat
    LDLdf["parent_id"] = ""
    LDLdf["field_weight"] = ""
    LDLdf["field_member_of"] = ""
    LDLdf["field_model"] = "Language"
    LDLdf["field_resource_type"] = "some test Value, Should not be empty" #something we can drive from by checking the file extension of obj 
    LDLdf.drop("field_date_captured", inplace=True ,axis= 1, errors='ignore')
    LDLdf.drop("field_is_preceded_by", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("field_is_succeeded_by", inplace=True ,axis= 1,errors='ignore')
    return LDLdf

#CREATE OUTPUT CSV
def run_name_change():
    for csvs, OBJs in zip(direct, OBJ_paths):
        data = input_directory(csvs,OBJs)
        
        nameChange = data.to_csv("/Users/mfatol1/Documents/LDL Migration/Git/Post-Processing-Tool-For-LDL/csv/output/{}".format(csvs), index=False)
        
    return data
run_name_change()


#################### 2) fill field_member_of, parent_id, field_weight column ########################

def inputrdf(RDF_dir, dir):
    data = glob.glob("{}/*.rdf".format(RDF_dir))
    # print("List of the RDFs in the folder: \n{}".format(data))
    print("------------------------------------------------")
    tags = [] #getting none-splitted
    val = [] #adding values to
    tag_name = [] #ALL the Tags in the rdf
    attrib = []
    text = []
    weightList= []
    data.sort()
    for dirs in data:
        rdf = ET.parse("{}".format(dirs))
        itter = rdf.iter()
        for inner in itter:
            tags.append(inner.tag)
            val.append(inner.attrib)
            text.append(inner.text)

    for tag in tags:
        split_tags = tag.split('}')
        tag_name.append(split_tags[1]) # ALL THE TAGS
    for vals in val:
        attrib.append(list(vals.values()))
    for num in range(len(tags)):
        if "isSequenceNumberOf" in tags[num]:
            weightList.append(text[num])
        else:
            weightList.append("")
    mylist = list(zip( tag_name, attrib, weightList))
    mylist_to_list = [list(i) for i in mylist] ##Extra(To make each element from tuple to list)##
    splitting = []
    for each in mylist_to_list:
        if each[0] == ("RDF"):
            splitting.append(each)
        if each[0] == ("hasModel"):
            splitting.append(each)
        if each[0] == ("isConstituentOf"):
            splitting.append(each)
        # if each[0] == ("isPageOf"):
        #     splitting.append(each)
        if each[0] == ("isSequenceNumber"):
            splitting.append(each)
        if each[0] == ("isPageNumber"):
            splitting.append(each)
        if each[0] == ("isSection"):
            splitting.append(each)
        if each[0] == ("isMemberOf"):
            splitting.append(each)
        if each[0] == ("deferDerivatives"):
            splitting.append(each)
        if each[0] == ("generate_ocr"):
            splitting.append(each)
    new = [ones for ones in mylist_to_list if ones not in splitting] #only keeps Description, isSequenceNumberOf and isMemberOfCollection
    weight = []
    field_member_of = []
    parrent = []
    count = []
    for q in new:
        if "isPageOf" in q[0]:
            print(q)
            count.append(q)

    for r in range(len(new)):
        if r+1 > (len(new)):
            break   
        else:
            if "Description" in new[r][0]:
                if "isPageOf" in new[r+1][0]:
                    collectionName = RDF_dir.split("/")[1]
                    nameofnumber = new[r+1][1][0]
                    ParentNumber = nameofnumber.split(":")[2]
                    parrent.append("{}:{}".format(collectionName, ParentNumber))
                    weight.append(new[r+1][2])
                    
                if "Description" in new[r+1][0]:
                    collectionName = RDF_dir.split("/")[1]
                    parrent.append("{}:COLLECTION".format(collectionName))
                    weight.append("")
                                        
                if "isSequenceNumberOf" in new[r+1][0]:
                    collectionName = RDF_dir.split("/")[1]
                    nameofnumber = new[r+1][0]
                    ParentNumber = nameofnumber.split("_")[1]
                    parrent.append("{}:{}".format(collectionName, ParentNumber))
                    weight.append(new[r+1][2])
                                      
                if "isMemberOfCollection" in new[r+1][0]:
                    Collection = new[r+1][1][0].split("/")[1]
                    field_member_of.append(Collection)
                    parrent.append(Collection)
                    weight.append("")

                if "isMemberOfCollection" not in new[r+1][0]:
                    field_member_of.append("")

    #Collection:
    print("collection RDF directory: {}/ NO SUBDIRECTORY!".format(RDF_dir)) #directory of data
    print("Metadata csv: {}".format(dir)) #directory of csv
    #info:
    print("number of Meta list: ({})".format(len(new))) #LENGH OF "new" LIST CONTAINING ALL 2 TAGS
    print("Lenght of field_member_of(collections): ({})".format(len(field_member_of))) #Lenght of field_member_of(collections)
    print("Lenght of weight(child numbers): ({})".format(len(weight))) #Lenght of field_member_of(collections)
    print("Lenght of parrent names: ({})".format(len(parrent))) #Lenght of parrent names
    print("--------------------------------------------------------------------------------------------------------------------")

    LDL2 = pd.read_csv("csv/output/{}.csv".format(dir.split('.')[0])) #EDIT >>> Changed the format from spliting the name of the directory to csv file, because we do not have collection folder containing RDFs, so we split the name after "/" which is the name of the directory (Data/Collection_Name) 
    LDL2df = pd.DataFrame(LDL2)     
    LDL2df["parent_id"] = parrent    
    LDL2df["field_weight"] = weight
    LDL2df["field_edtf_date_created"] = ""
    LDL2df["field_linked_agent"] = ""

    

    parentChild = LDL2df.to_csv("/Users/mfatol1/Documents/LDL Migration/Git/Post-Processing-Tool-For-LDL/csv/output/{}".format(dir), index=False)
    return parentChild

def run():
    for path, dir in zip(RDF_paths, direct):
        input = inputrdf(path, dir)
    return input
run()