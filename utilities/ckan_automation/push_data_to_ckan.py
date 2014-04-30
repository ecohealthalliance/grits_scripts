# Script to download files from direct links
# and upload to CKAN while updating corresponding
# metadata. Files to be uploaded are stored in 
#a folder /data_ckan/ in root.

# Print statement are present for logging purposes.

import csv
import os
import commands
import ckan.logic.action.create as ckan_create
import ckanapi
import re
import time
import argparse


def main():
     parser = argparse.ArgumentParser()
     parser.add_argument("fileName", "File holding information and direct URLs to datasets", type=str)
     parser.add_argument("ckanURL", "URL of CKAN", type=str)
     parser.add_argument("ckanAPIKey", "CKAN API Key", type=str)
     args = parser.parse_args()
     file_name = fileName 
     ckan_url = ckanURL
     ckan_api_key = ckanAPIKey

    # Prepare headers to read from file
    header = "name,repoURL,sourceURL,wgetURL,have,source,newCategories,categories,scope,eTag,lastModifiedDateInSource,geoResolution,startDate,endDate,timeResolution,rasterized,fileType,fileSize,internalLocation,ckanURL,notes".split(
        ",")

    # Iterate through file data
    with open(file_name) as f_in:
        reader = csv.DictReader(f_in, header)

        # Create a connection object to CKAN.
        demo = ckanapi.RemoteCKAN(ckan_url,ckan_api_key)

        for row in reader:

            # Check if 1) Files are already present 2) wgetURL is not empty
            # 3) filesize is not zero. Proceed only if all conditions are
            # satisfied. These fields were marked manually.
            if row['have'] == "no" and row['wgetURL'] != "" and row['fileSize'] != "":

                # Initialize dictionary to hold data for CKAN. This
                # will be pushed to CKAN later using their API.
                dict_package = {}

                dataset_name = ""

                # Populate dictionary with metadata to push data into
                # CKAN

                # Remove special characters from names of files. CKAN
                # permits "-" or "_" in names of files.
                dict_package['name'] = row['name'].replace("(", "").replace("&", "").replace(")", "").replace(":", "").replace(",", "").replace("'", "").replace("/", "").replace(".", "").replace("\\", "").replace("$", "").replace("%", "").replace(" ", "-").replace(";", "").lower()
                
		dataset_name = dict_package['name']
                dict_package['title'] = row['name']
                dict_package['author'] = row['source']

                # If source URL ( usually holds the dataset description )
                # is not present, update URL metadata with repository URL
                if row['sourceURL'] != "":
                    dict_package['url'] = row['sourceURL']
                else:
                    dict_package['url'] = row['repoURL']

                # For now, the notes are being updated with categories. This
                # is being done for future reference.
                dict_package['notes'] = row['newCategories'] + \
                    "," + row['categories'] + "," + row['scope']

                # Call API to create dataset
                try:
                    pkg = demo.call_action('package_create', dict_package)
                    print "Dataset Creation Successful : " + row['name']
                except ckanapi.NotAuthorized:
                    print "Dataset Creation Failed : " + row['name']
                    continue

                # Extract individual file links and file formats to
                # upload files for corresponding datasets.
                links = row['wgetURL'].split(',')
                links = [link.replace("\n", "") for link in links]
                formats = row['fileType'].split(',')

                # Iterate through links. This is because multiple files could be
                # associated to a dataset
                for link, format_t in zip(links, formats):

                    # Download file from source and path to which
                    # file was stored. The path is being stored to
                    # extract file name and use it for resource
                    # creation
                    command = "wget --content-disposition " + link + \
                        " -P /data_ckan/ 2>&1 | grep 'Saving to:' |awk '{print $3}'"
                    ret = commands.getoutput(command)

                    # Create resource name from file name
                    resource_file_name = ret.replace("'", "").replace("`", "")
                    complete_resource_name = resource_file_name.replace("/data_ckan/", "")
                    resource_name = complete_resource_name.split(".")[0]

                    # Populate resource metadata
                    file_obj = {}
                    dict_resource = {}
                    # package_id refers to dataset to which resource belongs
                    # to.
                    dict_resource['package_id'] = dataset_name
                    dict_resource['format'] = format_t
                    dict_resource['name'] = resource_name
                    file_t = open(resource_file_name)
                    file_obj['upload'] = file_t

                    # Call API to create resource for dataset
                    try:
                        res = demo.call_action(
                            'resource_create', dict_resource, files=file_obj)
                        print "Resource Creation Successful : " + link + "  For Dataset : " + row['name']

                        # Wait time to permit for file upload
                        time.sleep(3)
                    except ckanapi.NotAuthorized:
                        print "Resource Creation Failed : " + link + "  For Dataset : " + row['name']
                        continue


if __name__ == '__main__':
    main()
