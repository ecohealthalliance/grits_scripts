#Script to parse multiple json files ( developed from 
#PubMED XML files ) and aggregate them into one csv file.

#The variable names are arbitrary after a point as I ran out
#of ideas to name them.

import os
import json
from pprint import pprint
import argparse

final_abstract = ""

#Function to extract abstract from json file
def extractAbstract(data):
	global final_abstract	
	for attr,val in data.iteritems():
		if isinstance(val,dict):
			if attr == "abstract":
				final_abstract = parseAbstract(val)
			else:
				extractAbstract(val)

#Function to parse abstract once found
def parseAbstract(val):
	abstract = ""
	try:
		for k,v in val.iteritems():
			if isinstance(v, dict) is True:
				for k1, v1 in v.items():
					for v4 in v1:
						try:
							for k5,v5 in v4.items():
								if k5 == 'p':
									abstract = abstract + v5 + " "
						except:	
							continue
					if k1 == '#text':
						abstract = abstract + v1 + " "

			elif isinstance(v, list) is True:
				for v2 in v:
					if isinstance(v2,dict) is False:
						abstract = abstract + v2 + " "
					else:
						for k3, v3 in v2.items():
							if isinstance(v3,dict) is True:
								for k7,v7 in v3.items():
									if k7 == '#text':
										abstract = abstract + v7 + " "
							elif isinstance(v3,list) is True:
								for v8 in v3:
									if isinstance(v8, dict) is True:
										for k9,v9 in v8.items():
											if k9 == '#text':
												abstract = abstract + v9 + " "
							else:
								if k3 == 'p':
									abstract = abstract + v3 + " "
			else: 
				#Direct text condition
				if k == "p":
					abstract = v
				elif k != "p" and k != "":
					continue
				else:
					abstract = v
	except:
		abstract = "na"

	if abstract == "":
		abstract = "na"
	return abstract
	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("pathJSONFiles","Enter complete path where all json files are stored ( Please end with / )",type=str)
	parser.add_argument("outputFile","Output csv file",type=str)
	args = parser.parse_args()
	
        global final_abstract
	numFiles = 0
	output_file = outputFile
	path_json_files = pathJSONFiles

	f_out = open(output_file, "w")
	for dirpath, dirname, files in os.walk(path_json_files):
		for val in files:
			if val.endswith(".json"):
				#Initialize variables
				final_text = ""
				article_title = ""
				journal_title = ""
				keywords = ""
				doi = ""
				journal_publisher = ""
				journal_volume = ""
				journal_issue = ""				
				final_abstract = ""
			
				#Load data for each file
				val = path_json_files + val
				json_data = open(val)
			        data = json.load(json_data)
				if data['article']['@article-type'] != "research-article":
					continue
				
				#Extract abstract
				extractAbstract(data)		
				if final_abstract is None:
                                        final_abstract = "na"
                                else:
                                        final_abstract = final_abstract.replace("\""," ")

				#Extract keywords
				try:   
        	       			for val in data['article']['front']['article-meta']['kwd-group']['kwd']:
                	       			keywords = keywords + val + ","
               				keywords = keywords[:-1]
        			except:
               				keywords = "na"
	
        			#Extract article title
				try:
					temp = data['article']['front']['article-meta']['title-group']['article-title']
		
					if temp is None:
						article_title = "na"
					try:
						if isinstance(temp,dict) is True:
							for key, val in temp.items():
								if len(temp) == 1 and key == "related-article":
									article_title = "na"

								if key == "#text" or key == "sc" or key == "bold" or key == "italic":
									if isinstance(temp[key],list) is True:
										for v2 in temp[key]:
											if isinstance(v2,dict) is True:
												for v3 in v2.values():
													article_title = article_title + " " + v3
											else:	
												article_title = article_title + " " + v2
									else:	
										if isinstance(temp[key],dict) is True:
											continue
										else: 							
											article_title = article_title + temp[key]										
						else:
							article_title = temp
					except:
						article_title = "na"
				except:
					article_title = "na"
	
				if article_title is None:
					article_title = "na"
				else:
					article_title = article_title.replace("\""," ")	
	
        			#Extract journal title
				try:
        				journal_title = data['article']['front']['journal-meta']['journal-title-group']['journal-title']
				except:
					journal_title = data['article']['front']['journal-meta']['journal-title']

				#Extract doi
				try:
					doi_data = data['article']['front']['article-meta']
					for k1, v1 in doi_data.items():
						if k1 == "article-id":
							for v2 in v1:
								flag = False
								for k3 in v2.keys():
									if v2[k3] == "doi":
										flag = True
									if k3 == "#text" and flag == True:
										doi = v2[k3]
				except:
					doi = "na"
		
				if doi == "":
					doi = "na"
					
				#Extract journal publisher
				try:
					journal_publisher = data['article']['front']['journal-meta']['publisher']['publisher-name']
				except:
					journal_publisher = "na"

				if journal_publisher == "" or journal_publisher is None:
					journal_publisher = "na"

				#Extract journal volume
				try:
					journal_volume = data['article']['front']['article-meta']['volume']
			
				except:
					journal_volume = "na"

				if journal_volume == "" or journal_volume is None:
					journal_volume = "na"

				#Extract journal issue
				try:
					journal_issue = data['article']['front']['article-meta']['issue']
				except:
					journal_issue = "na"

				if journal_issue == "" or journal_issue is None:
					journal_issue = "na"
				
				#Extract publication date
				try:
					val = data['article']['front']['article-meta']['pub-date']
					if isinstance(val,list) is True:
						for val1 in val:
							if val1['@pub-type'] == "epub":
								if isinstance(val1['year'],dict) is True:
									article_date_year = val1['year']['#text']
								else:
									article_date_year = val1['year']

								article_date_month = val1['month']
				except:
					article_date = "na"
				
				if article_date_year == "" or article_date_year is None:
					article_date_year = "na"

				if article_date_month == "" or article_date_month is None:
					article_date_month = "na"


        			#Build final text to be written into file
        			final_text = "\"" + doi + "\"" \
						+ "," + "\"" + article_date_year + "\"" \
						+ "," + "\"" + article_date_month + "\"" \
						+ "," + "\"" + article_title + "\"" \
						+ "," + "\"" + final_abstract + "\"" \
						+ "," + "\"" + keywords + "\"" \
						+ "," + "\"" + journal_title + "\"" \
						+ "," + "\"" + journal_publisher + "\"" \
						+ "," + "\"" + journal_volume + "\"" \
						+ "," + "\"" + journal_issue + "\"" 
        			
        			final_text = final_text.encode('utf-8')
        			f_out.write(final_text)
        			f_out.write("\n")
				json_data.close()
	
	f_out.close()

if __name__ == '__main__':
	main()
