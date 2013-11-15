# Script for converting PubMED XML file into
# JSON

from lxml import objectify, etree
import json
import xmltodict
import csv
import re


def generateFileList():
    # Populate a list structure with files to be
    # converted

    # Read file holding names of files to be
    # converted
    f = open("list_of_files.csv", "r")
    files = csv.reader(f)
    for row in files:
        file_name = row[0]

        # Add to list structure only if it ends with ".nxml"
        # extension
        if file_name[-5:] == ".nxml":
            file_list.append(file_name)

    return file_list


def convertToJson(file_list):
    # Convert XML file to JSON

    # Iterating through all file names in file list
    for file_name in file_list:
        try:
            # Read all data from file in string format
            f = open(file_name, "r")
            text = f.read()

            # Convert string data into XML obj
            root = objectify.fromstring(text)
            obj_xml = etree.tostring(root)

            # Convert the XML obj into JSON obj
            obj_dict = xmltodict.parse(obj_xml)
            obj_json = json.dumps(obj_dict, indent=4)

            # Write JSON obj to file. Stripping the complete filepath
            # to extract file name and replacing ".nxml" extension
            # with ".json"
            new_file_name = "json/" + \
                re.sub("[\d\D]+/", "", file_name[:-5]) + ".json"
            f_out = open(new_file_name, "w")
            f_out.write(obj_json)

            f_out.close()
            f.close()
        except:
            # If file could be not be found, print file name. ( For debugging )
            print file_name + ¨ not found. Skipping ! ¨
            continue

if __name__ == "__main__":
    file_list = generateFileList()
    convertToJson(file_list)
