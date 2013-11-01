# Script for gathering definitions from Google
# search.

import urllib2
import csv
import lxml.html as lxml
import random
import argparse
from time import sleep


# Global dictionary holding disease name
diseaseList = []

def populateDiseaseList(input_file):
# Populate dictionary with disease names
    with open(input_file, 'r') as fp_in:
        url_reader = csv.reader(fp_in)
        for row in url_reader:
            disease_list.append(row[0])

def extractDefinitions(output_file):
# Extract links from google search results
    first_source = ""
    second_source = ""
    third_source = ""

    # Write headers to output file
    f_out = open(output_file, "w")
    f_out.write(
        "disease,definition_1,source_1,definition_2,source_2,definition_3,source_3")
    f_out.write("\n")

    # Iterate through disease list
    for disease in disease_list:
        # Add headers to request. This is being done as requests from bots was
        # being rejected
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
               }

        # Replace all spaces with '+'. This is being done to develop query for
        # search
        modified_disease = disease.replace(" ", "+")

        # Generate URL for search
        url_def = "https://www.google.com/search?q=define+%3A+" + modified_disease
        print url_def

        # Send requests and parse response from Google
        req = urllib2.Request(url_def, headers=hdr)
        response = urllib2.urlopen(req)
        html_text = response.read().decode('utf-8')
        raw_text = lxml.document_fromstring(html_text)

        # It was seen while testing that any search term with define
        # could generate definitions from two sources ( maximum ),
        # however the tags for these definitions varies. 3 tags were
        # prominent:
        # 1. div with class name 'kno-fb-ctx kno-desc'
        # 2. ol with class name 'lr_dct_wd_ol'
        # 3. ol with class name 'lr_dct_sf_sens'

        # Located on right side of search results
        first_def = raw_text.xpath(
            "//div[@class='kno-fb-ctx kno-desc']//text()")
        if first_def != []:
            url_def_link = raw_text.xpath(
                "//div[@class='kno-fb-ctx kno-desc']//a[@class='fl q kno-desca-lnk']/@href")
            first_source = first_source.replace("\"", "")
            first_source = "\"" + first_def[0] + "\",\"" + first_def[
                len(first_def) - 1] + " ( " + url_def_link[0] + " )\""
        else:
            first_source = "\"na\"" + "," + "\"na\""

        # Quite unsure as to why two tags are being used instead of one for
        # the following

        # Located just below search box, source is wikipedia
        second_def = raw_text.xpath("//ol[@class='lr_dct_wd_ol']//text()")
        if second_def != []:
            second_source = second_source.replace("\"", "")
            second_source =  "\"" + \
                second_def[0] + "\",\"" + second_def[1] + "\""
        else:
            second_source = "\"na\"" + "," + "\"na\""

        # Located just below the search, source is not known
        third_def = raw_text.xpath("//ol[@class='lr_dct_sf_sens']//text()")
        if third_def != []:
            third_source = third_source.replace("\"", "")
            third_source = "\"" + third_def[2] + "\""
        else:
            third_source = "\"na\"" + "," + "\"na\""

        # Concatente all results into a string, encode and write to file
        final_source = "\"" + disease + "\"," + \
            first_source + "," + second_source + "," + third_source
        final_source = final_source.encode('utf-8')
        f_out.write(final_source)
        f_out.write("\n")
        first_source = second_source = third_source = final_source = ""

        # Delay
        sleep(random.lognormvariate(1.5, 0.5))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "diseaseFile", help="CSV input file with list of diseases to be scrapped", type=str)
    parser.add_argument(
        "definitionFile", help="CSV output file with list of diseases and scrapped definitions", type=str)
    args = parser.parse_args()
    input_file = args.diseaseFile
    output_file = args.definitionFile

    populateDiseaseList(input_file)
    extractDefinitions(output_file)

if __name__ == '__main__':
    main()
