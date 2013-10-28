# Script to extract first sentence from
# symptom description found on medicinenet.com

import csv
import lxml.html as l
import urllib2
import nltk.tokenize
import re
import argparse

# Dictionary storing symptom and corresponding url
# from medicinenet.
urlDict = {}

# Function for extracting article from medicinenet.com


def extractArticle(outputFile):
    final_text = ""
    concat_text = ""
    f_out = open(outputFile, "w")

    # Read each symptom and url combination from
    # dictionary
    for symptom, url in urlDict.items():
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
               }

        # Sending request and reading response from medicinenet
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        html_text = response.read()

        # Converting response to parseable format
        raw_string = l.document_fromstring(html_text)

        # Medicinenet articles are present in a "div"
        # by the name of "article" in most cases. The text to be
        # scraped is present in <p></p> tags within
        # the div. Creating a list of <p></p> tag text
        paras = raw_string.xpath("//div[@class='article']/p//text()")
        if paras == []:
            paras = raw_string.xpath("//div[@class='article']//p//text()")

        # Obtaining text from all <p></p> within the <div>
        # with name 'article'
        raw_text = [ex.replace('\r\n', ' ') for ex in paras if ex is not None]
        for text in raw_text:
            concat_text = concat_text + text
        # Tokenizing the first paragraph
        sentences = [
            sentence for sentence in nltk.tokenize.sent_tokenize(concat_text)]

        # Write the symptom and first sentence to file symptom_definitions.csv

        sentences[0] = re.sub(r"[A-Za-z]+ :", "", sentences[0])
        final_text = "\"" + symptom + "\",\"" + sentences[0] + "\""
        writeToFile(f_out, final_text)
        concat_text = ""
    f_out.close()

# Function to write symptoms and corresponding definitions
# The output is in a file symptom_definitions.csv and in the
# format (symptom name, symptom definition )


def writeToFile(f_out, final_text):
    f_out.write(final_text)
    f_out.write("\n")

# Function to populate urlDict dictionary


def createLinkList(inputFile):
    with open(inputFile, 'r') as f_out_links:
        urlReader = csv.reader(f_out_links)
        for row in urlReader:
            urlDict[row[0]] = row[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "symptomFile", help="CSV input file with list of symptoms and medicinenet links", type=str)
    parser.add_argument(
        "definitionFile", help="CSV output file with list of symptoms and scrapped definitions", type=str)
    args = parser.parse_args()
    inputFile = args.symptomFile
    outputFile = args.definitionFile

    createLinkList(inputFile)
    extractArticle(outputFile)

if __name__ == '__main__':
    main()
