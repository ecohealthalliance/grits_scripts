import csv
import os
import commands
import ckan.logic.action.create as ckan_create
import ckanapi
import re
from urllib2 import urlparse
import time

def main():
	
	#Read variables from File
	list_name = "ecohd.csv"
	header = "name,repoURL,sourceURL,wgetURL,have,source,newCategories,categories,scope,eTag,lastModifiedDateInSource,geoResolution,startDate,endDate,timeResolution,rasterized,fileType,fileSize,internalLocation,ckanURL,notes".split(",")
	with open(list_name) as f_in:
		reader = csv.DictReader(f_in,header)
	
		#Create a connection object to CKAN
		demo = ckanapi.RemoteCKAN('http://ec2-23-20-74-45.compute-1.amazonaws.com/', apikey='e96e704b-4584-44e6-92ac-b919e4c9c312')
		for row in reader:

			#Check files for which no files are present and direct links are present
			if row['have'] == "no" and row['wgetURL'] != "" and row['fileSize'] != "":
				dict_package = {}
				dataset_name = ""
				dict_package['name'] = row['name'].replace("(","").replace("&","").replace(")","").replace(":","").replace(",","").replace("'","").replace("/","").replace(".","").replace("\\","").replace("$","").replace("%","").replace(" ","-").replace(";","").lower()
				dataset_name = dict_package['name']
				print dataset_name	
				dict_package['title'] = row['name'] 	
				dict_package['author'] = row['source']
				if row['sourceURL'] != "":
					dict_package['url'] = row['sourceURL']
				else:
					dict_package['url'] = row['repoURL']

				dict_package['notes'] = row['newCategories'] + "," + row['categories'] + "," + row['scope']
		
				#Initialize dictionary for package creation in 
				#CKAN ( CKAN refers a dataset as package) and create 
				#it.
				try:
 	                               pkg = demo.call_action('package_create',dict_package)
				       print "Dataset Creation Successful : " + row['name']
                                except ckanapi.NotAuthorized:
                                       print "Dataset Creation Failed : " + row['name']
				       continue
				
				links = row['wgetURL'].split(',')
				links = [link.replace("\n","") for link in links] 
				formats = row['fileType'].split(',')

				#Iterate through links. This is because multiple files could be 
				#associated to a dataset
				for link,format_t in zip(links,formats):
					#status = -1
					flag = False
					#Download file from source 
					command = "wget --content-disposition " + link + " -P /data_ckan/ 2>&1 | grep 'Saving to:' |awk '{print $3}'"
					ret = commands.getoutput(command)
					
					file_name1 = ret.replace("'","").replace("`","")
					complete_resource_name = file_name1.replace("/data_ckan/","")
					resource_name = complete_resource_name.split(".")[0]


					file_obj = {}
					dict_resource = {}
					dict_resource['package_id'] = dataset_name
					dict_resource['format'] = format_t
					dict_resource['name'] = resource_name
					file_t = open(file_name1)
					file_obj['upload'] = file_t

					#Initialize dictionary for resource creation in 
					#CKAN ( CKAN refers a file as resource) and create 
					#it.
					try:
						res = demo.call_action('resource_create',dict_resource,files=file_obj)
						print "Resource Creation Successful : " + link + "  For Dataset : " + row['name']
						time.sleep(3)
					except ckanapi.NotAuthorized:
						print "Resource Creation Failed : " + link + "  For Dataset : " + row['name']
						continue


if __name__ == '__main__':
	main()	
