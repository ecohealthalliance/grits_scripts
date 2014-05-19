#Script to infer grid event if event keys ( pathogen name, location, year ) 
#are present in abstracts

import csv
import re
from collections import defaultdict
from collections import Counter
import argparse

#Dictionary to hold GRID Event Keys
event_term_list = defaultdict(list)

#Initialize GRID event key list
def createEventTermList():
    with open("grid_events.csv", "r") as f:
        reader = csv.reader(f)
        key = ""
        for row in reader:
            key = row[0]
            for i in range(1, len(row)):
                row[i] = row[i].lower()
                if row[i] != '':
                    event_term_list[key].append(row[i])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("outputFile",help="Name of output CSV file",type=str)
    parser.add_argument("thresholdVal",help="Number of matches required to infer GRID event",type=int)	
    args = parser.parse_args()
    out_file = outputFile
    threshold = thresholdVal

    #This is being done so that large files could 
    #be broken down into smaller chunks and parsed. 
    #It could be replaced if an alternative is found.
    filelist = ['pubmed_research_articles']
    
    #Call function to create GRID Event dictionary
    createEventTermList()

    num_no_match = 0
    num_without_doi = 0
    total = 0
    f_out = open(out_file, "w")

    #Iterate through list of files
    for file_name in filelist:
        in_file = file_name + ".csv"
        header = "doi,year,month,article_title,abstract,keywords,journal_title,journal_publisher,journal_volume,journal_issue".split(",")
        with open(in_file, "r") as f:
            csv.field_size_limit(100000000)
            reader = csv.DictReader(f, header)
            for row in reader:
                total += 1
		
		#Verify if file has doi. If not, 
		#then parse next article.
                if row['doi'] == "na":
                    num_without_doi += 1
                    continue

                abstract = ""

		#This is done to create uniformity in 
		#case matching.
                abstract = row['abstract'].lower()

		#Initialize variables to store matched terms
                terms_present = defaultdict(list)
                num_match = [0] * len(event_term_list)

		#Iterate through GRID event terms and search 
		#for them in abstracts. If present, update 
		#variables.
                for id_i, terms in event_term_list.items():
                    for val in terms:
                        val = '\\b(' + val.lower() + ')\\b'
                        match = re.search(val, abstract)
                        if match is not None:
                            id_val = int(id_i)
                            num_match[id_val] = num_match[id_val] + 1
                            terms_present[id_i].append(match.group(0))

		#Check for number of matches for each event against 
		#threshold. If present, write to file.	
                for x in range(0, len(event_term_list)):
                    final_text = ""
                    if num_match[x] > threshold:
                        index = str(x)
                        event_name = ",".join(event_term_list[index])
                        final_text = "\"" + str(x) + "\"" + "," \
                            + "\"" + event_name + "\"" + "," + "\"" + row['doi'] + "\"" + "," \
                            + "\"" + row['year'] + "\"" + "," \
                            + "\"" + row['month'] + "\"" + "," \
                            + "\"" + row['article_title'] + "\"" + "," \
                            + "\"" + row['journal_title'] + "\"" \
                            + "," + "\""
                        for val in terms_present[index]:
                            final_text = final_text + val + ","
                        final_text = final_text[:-1] + "\"" + \
                            "," + "\"" + row['abstract'] + "\""

                        f_out.write(final_text)
                        f_out.write("\n")
        f.close()

if __name__ == '__main__':
    main()
