# Script for extracting links for all outbreaks from WHO's webpage.
# Outbreak lists are maintained for years 1996 - 2013 and each page
# has a seperate URL.
# For example, outbreaks from 2012 can be seen at:
# http://www.who.int/csr/don/archive/year/2012/en/index.html

import csv
import lxml.html as l
import urllib2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output_file", help="CSV output file", type=str)

    args = parser.parse_args()
    csv_file = args.output_file

    f_out = open(csv_file, "w")

    # Initialize loop to extract data for years 1996 - 2013
    for year in range(1996, 2014):

        # Construct link for a year
        link = "http://www.who.int/csr/don/archive/year/" + \
            str(year) + "/en/index.html"
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
               }

        # Sending request and reading response from WHO
        req = urllib2.Request(link, headers=hdr)
        response = urllib2.urlopen(req)
        html_text = response.read()
        raw_string = l.document_fromstring(html_text)

        # Links are present in ul tag with class-name "auto-archive". Create
        # Xpath expression to extract them.
        paras = raw_string.xpath("//ul[@class='auto_archive']//@href")

        # All links extracted above are incomplete. Constuct complete
        # links and write them to output file.
        for link in paras:
            text = str(
                year) + "," + link.replace("/entity",
                                           "http://www.who.int")
            f_out.write(text)
            f_out.write("\n")

if __name__ == "__main__":
    main()
