# Script to extract Outbreak news from WHO Links and
# write to CSV file.

import csv
import lxml.html as l
import urllib2


def main():
    year = 0
    link = ""
    final_text = ""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "link_file", help="CSV input file having list of links with fields 'Year,'Link' in the same order", type=str)
    parser.add_argument(
        "news_file", help="CSV output file with scraped data with fields 'Year','Link','News' in the same order", type=str)

    args = parser.parse_args()
    link_file = args.link_file
    news_file = args.news_file

    f_in = open(link_file, "r")
    f_out = open(news_file, "w")
    reader = csv.reader(f_in)
    for row in reader:

        # Extract year and link from first and second field in
        # CSV file.
        year = row[0]
        link = row[1]
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
               }

        # Sending request and reading response from medicinenet
        req = urllib2.Request(link, headers=hdr)
        response = urllib2.urlopen(req)
        html_text = response.read()
        raw_string = l.document_fromstring(html_text)

        # All text is present in div with id name called primary. Build
        # an XPath expression to extract all text.
        reports = raw_string.xpath("//div[@id='primary']//text()")
        for text in reports:
            text = text.encode('utf-8')

            # Concatenate text to build one complete Outbreak news text
            news_text = news_text + \
                text.replace(
                    "\n",
                    " ").replace(
                    "\r",
                    "").replace(
                    "\t",
                    "").lstrip(
                ).rstrip(
                ).replace(
                    "\"",
                    " ") + " "

        # Build text to write into CSV file with 'Year' and 'Link'
        write_text = "\"" + str(year) + "\",\"" + \
            link + "\",\"" + news_text[:-1] + "\""
        f_out.write(write_text)
        f_out.write("\n")
        news_text = ""

if __name__ == "__main__":
    main()
