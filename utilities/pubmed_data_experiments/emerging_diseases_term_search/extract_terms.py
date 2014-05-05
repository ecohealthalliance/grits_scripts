#Script to generate list of abstracts with emerging terms. 
#The list of terms is present in file emerging_term_list.csv
import csv
import re

#Global list to hold emerging terms
term_list = []

#Function to initialize list of emerging terms
def createTermList():
	with open("emerging_term_list.csv", "r") as f:
		reader = csv.reader(f)
		for row in reader:
			term_list.append(row[0])
		print term_list
	
def main():
	#Populate list of emerging terms
	createTermList()

	#Initialize variables to calculate statistics
	num_without_doi = 0
	total = 0

	#Open output file
	f_out = open("output_file.csv", "w")
	
	#Initialize headers for reading pubmed data file
	header = "doi,year,month,article_title,abstract,keywords,journal_title,journal_publisher,journal_volume,journal_issue".split(",")
	with open("pubmed_data.csv","r") as f:
		csv.field_size_limit(100000000)
		reader = csv.DictReader(f, header)
		
		#Iterate through all abstracts
		for row in reader:
			total += 1

			#If file does not have doi, increment counter 
			#and proceed to next abstract
			if row['doi'] == "na":
				num_without_doi += 1
				continue

			abstract = ""
			abstract = row['abstract'].lower()
			terms_present = ""

			#Verify if any of emerging terms are present in 
			#abstracts
			for term in term_list:
				match = re.search(term, abstract)
				if match is not None:
					terms_present = terms_present + match.group(0) + "," 
			
			#Write final results to output file
			final_text = ""
			if terms_present != "":
				final_text = "\"" + row['doi'] + "\"" + "," + "\"" + row['journal_title'] + "\"" + "," + "\"" + terms_present[:-1] + "\""
				f_out.write(final_text)
				f_out.write("\n")				

		print "Number of files :" + str(total)
		print "Number of files without DOI :" + str(num_without_doi)
	
if __name__ == '__main__':
	main()
