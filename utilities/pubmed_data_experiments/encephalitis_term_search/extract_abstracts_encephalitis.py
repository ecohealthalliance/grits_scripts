# Script to calculate number of abstracts which contain
# terms "encephalitis" or "encephalitides".

import csv
import re


def main():
    # Term list for Encephalitis search
    term_list = ['encephalitis', 'encephalitides']
    num_no_match = 0
    num_without_doi = 0
    total = 0

    # Initialize output file
    f_out = open("result.csv", "w")
    header = "doi,year,month,article_title,abstract,keywords,journal_title,journal_publisher,journal_volume,journal_issue".split(
        ",")

    # Iterate through PubMED data
    with open("pubmed_data.csv", "r") as f:
        csv.field_size_limit(100000000)
        reader = csv.DictReader(f, header)

        # Read and process each abstract while generating statistics.
        for row in reader:

            # Increment article count
            total += 1

            # Verify if article has doi. If not, then
            # stop processing of current article and
            # proceed to next
            if row['doi'] == "na":
                num_without_doi += 1
                continue

            # Check if encephalitis related terms are present in
            # abstracts
            abstract = ""
            abstract = row['abstract'].lower()
            terms_present = ""
            for term in term_list:
                match = re.search(term, abstract)
                if match is not None:
                    terms_present = terms_present + match.group(0) + ","

            # Write results to output file
            final_text = ""
            if terms_present != "":
                final_text = "\"" + row['doi'] + "\"" + "," + "\"" + row['journal_title'] + "\"" + "," + "\"" + terms_present[:-1] + "\"" + "," + "\"" + abstract + "\""
                f_out.write(final_text)
                f_out.write("\n")
            else:
                num_no_match += 1

        # Print out final statistics
        print "Number of files :" + str(total)
        print "Number of files without DOI :" + str(num_without_doi)
        print "Number of files without match ( in files with DOI ) :" + str(num_no_match)

if __name__ == '__main__':
    main()
