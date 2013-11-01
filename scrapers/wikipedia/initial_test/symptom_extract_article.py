#Script to extract symptom paragraph for a disease
#from Wikipedia. The diseases used are present in 
#file 'diseases.csv' and corresponding symptoms from 
#wikipedia are being written into 'symptom_definitions.csv'
#This script can be modified for extracting Wikipedia articles
#in entirity or by section.

import csv
import lxml.html as l
from lxml import etree
import urllib2
import re

#Global dictionary holding disease name 
#and corresponding wikipedia link
urlDict = {}

#Populate disease and wikipedia URL in 
#dictionary
def populateURL(f_in):
	with open(f_in,'r') as fp_in:
		urlReader = csv.reader(fp_in)
		for row in urlReader:
			urlDict[row[0]] = row[1]

#Extract complete menu list from wikipedia 
#article to verifiy if symptoms are present in it.
#It was observed that symptoms are defined under
#the heading "Signs and symptoms" in most
#disease articles. 
def extractHtml():
	initial_string = "Signs and symptoms"
	f_out = "symptom_definitions.csv"
	fp_out = open(f_out,'w')
	
	#Sending request and parsing response to verify 
	#if symptoms section is present.
	for disease, url in urlDict.items():

		#Populating User-Agent header of HTTP request
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
		}
		
		#Sending request and receving response
		req = urllib2.Request(url, headers=hdr)
		response = urllib2.urlopen(req)
		html_text = response.read()

		#Parsing response to extract all menu items 
		raw_text = l.document_fromstring(html_text)
		menu_items = raw_text.xpath("//div[@id='mw-content-text']/h2/span/text()")

		#Verifying if symptoms paragraph is present 
		#in menu extracted. If present, processing is to 
		#be done for extracting symptom paragraph.
		if initial_string in menu_items:
			extractSymptom(disease, raw_text, menu_items, initial_string, fp_out)	
	fp_out.close()

#Function to extract symptom paragraph if it is present 
def extractSymptom(disease, raw_text, menu_items, initial_string, fp_out):

	#Parsing response to extract data of 3 types:
	#1. All text present in header ( tag h2)
	#2. All text present in paragraph ( tag p )
	#3. All text present in lists ( tag /ul/li )
	#The above is being done because Wikipedia content
	#is written in a div ( with id 'mw-content-text')
	#and tags h2, p and ul/li are present as siblings 
	#under that div.
	paras = raw_text.xpath("//div[@id='mw-content-text']/h2//text() | //div[@id='mw-content-text']/p//text() | //div[@id='mw-content-text']/ul/li//text()")
	
	#extracting next menu item string or heading after 
	#symptoms 
	final_string = ""
	for index, menu in enumerate(menu_items):
		if menu == initial_string:
			final_string = menu_items[index+1]

	#slicing extracted text array from wikipedia 
	#for text between symptoms heading and next heading
	#(extracted above)
	begin_index = 0
	end_index = 0
	for index, text in enumerate(paras):
		if text == initial_string:
			#Value being incremented as current value 
			#is 'Signs and Symptoms' ( which is not needed )
			begin_index = index + 1
		if text == final_string:
			end_index = index
	paras = paras[begin_index:end_index]	

	#Building symptoms paragraph
	final_text = ""
	for text in paras:
		final_text = final_text + text
	final_text = re.sub(r"[[][0-9a-zA-Z ]+]","",final_text)
	final_text = final_text.replace('"',' ')
	final_text = final_text.replace('\r\n',' ')

	#Function to write disease and symptom paragraph
	#into output file
	writeToFile(disease, final_text, fp_out)	

#Write disease and symptom extracted from wikipedia
#into output file, ie. symptom_defintions.csv
def writeToFile(disease, final_text, fp_out):
	fileStr = disease + ",\"" + final_text + "\""
	fileStr = fileStr.encode('utf-8')
	fp_out.write(fileStr)
	fp_out.write("\n")

#Main function
def main():
	f_in = "diseases.csv"
	populateURL(f_in)
	extractHtml()

if __name__ == '__main__':
	main()
