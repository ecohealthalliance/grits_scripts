#Script for obtaining metadata information about 
#for datasets. For this, it is necessary to have active
#links which end with file names ( name and extension ).

#Links for HTML pages will not work. 

import csv
import commands
import re
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("inFile","Input file with information about datasets",type=str)
	parser.add_argument("outFile","Output file with dataset statistics",type=str)	
	args = parser.parse_args()
	file_name_in = args.inFile
	file_name_out = args.outFile

	#Read variables from File
	f_out = open(file_name_out,"wb")

	header = "name,repoURL,sourceURL,wgetURL,have,source,newCategories,categories,scope,eTag,lastModifiedDateInSource,geoResolution,startDate,endDate,timeResolution,rasterized,fileType,fileSize,internalLocation,ckanURL,notes".split(",")

	with open(file_name_in) as f_in:
		reader = csv.DictReader(f_in,header)

		#Iterate through data read from file
		for row in reader:

			#Initialize required variables
			size_of_files = 0
			file_types = ""
			e_tags = ""
			last_modified_dates = ""

			#Check if file was previously downloaded. 
			#If yes, check next link. Please note, 
			#this field was marked manually and currently,
			#there is "no" automated way of knowing this.
			#For future, this could be updated using CKAN
			if row['have'] == "yes":
				continue

			#Check if direct links to files are present. Please 
			#note that these links were obtained manually. 
			if row['wgetURL'] != "":
	
				#Extract links to multiple files if they are 
				#present. Often, datasets were found to have 
				#mutliple files.
				links = row['wgetURL'].split(',') 

				#Iterate through each link and aggregate 
				#metadata information for each dataset
				for link in links:
					
					#Replace new lines ( if any ) from links
					link = link.replace("\n","")

					#Extract content length from value returned by CURL
					command = "curl --head " + link + " | grep Content-Length"
					val = commands.getoutput(command)
					size = re.sub("[\D\d]+Content-Length: ","",val)

					#This is being done to remove junk characters. The cause
					#of the junk characters is not known. 
					if size == val:
						size = 0

					#Aggregate file sizes
					try:
						size_of_files = size_of_files + int(size)
					except:
						continue
						
					#Extract content type ( or file type ) from value 	
					#returned by CURL
					command = "curl --head " + link + " | grep Content-Type"
					val = commands.getoutput(command)
					file_type = re.sub("[\D\d]+Content-Type: ","",val)
					file_type = file_type.replace("\n","").replace("application/","").replace("\r","")

					#This is being done to remove junk characters
					if file_type == val:
						file_type = ""

					#Concatenate multiple file types if multiple files are
					#present
					file_types = file_types + file_type + ","		

					#Extract ETag from value returned by CURL. This is 
					#useful for versioning of files.
					command = "curl --head " + link + " | grep ETag"
					val = commands.getoutput(command)
					e_tag = re.sub("[\D\d]+ETag: ","",val)
					e_tag = e_tag.replace("\"","")

					#Being done to remove junk characters
					if e_tag == val:
						e_tag = ""

					#Remove tags and aggregate ETags if multiple 
					#files are present
					e_tag = e_tag.replace("\r","")
					e_tags = e_tags + e_tag + ","

					#Extract last modified date from value returned by CURL
					command = "curl --head " + link + " | grep Last-Modified"
					val = commands.getoutput(command)
					last_modified = re.sub("[\D\d]+Last-Modified: ","",val)

					#Remove junk characters if any, present
					if last_modified == val:
						last_modified = ""
					
					#Aggregate last modified dates of files if multiple files are 
					#present
					last_modified = last_modified.replace("\r","").replace(",","")
					last_modified_dates  = last_modified_dates + last_modified + "," 
			
			
			#Convert size of files from bytes to MB
			size_of_files = float(size_of_files) / (1024*1024)
			
			#Remove "," from end of strings which hold file types,
			#etags and last modifed dates
			file_types = file_types[:-1]	
			e_tags = e_tags[:-1]
			last_modified_dates = last_modified_dates[:-1]

			#Write value to file
			final_str = "\"" + row['name'] + "\"" + "," + "\"" + str(size_of_files) + "\"" + "," + "\"" + file_types + "\""	+ "," + "\"" + e_tags + "\"" + "," + "\"" + last_modified_dates + "\""
			f_out.write(final_str)
			f_out.write("\n")

if __name__ == '__main__':
	main()	
