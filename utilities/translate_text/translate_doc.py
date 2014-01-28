# script to translate a document from one language to another

import urllib2
import json
import argparse


def readText(f):
# Function to read text from input file

    f_in = open(f, "r")
    text = f_in.read()
    f_in.close()
    return text


def translateText(source_text, source_lang, dest_lang):
# Function to translate text

    # Reconstruct input text to build url for Google translate
    # URL
    source_text = source_text.replace("%", " ").replace("\n", " ").replace(" ", "%20")

    # The Google Translate API can be used only on registering for billing.
    # Once done, extract the API Key and update API_KEY variable with it.
    API_KEY = ""

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
           }
    link = "https://www.googleapis.com/language/translate/v2?key=" + API_KEY + \
        "&source=" + source_lang + "&target=" + dest_lang + "&q=" + source_text

    # Send request and convert response to json object
    req = urllib2.Request(link, headers=hdr)
    response = urllib2.urlopen(req)
    text = response.read()
    json_obj = json.loads(text)

    return json_obj


def writeText(json_obj, f):
# Function to write translated text into output file
    f_out = open(f, "w")

    # Write value of key 'translatedText' from returned JSON object
    # into output file
    translated_text = json_obj['data']['translations'][0]['translatedText']
    translated_text = translated_text.encode('utf-8')
    f_out.write(translated_text)
    f_out.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sourceFile", help="Input text file with content to be translated", type=str)
    parser.add_argument(
        "translatedFile", help="Output text file with translated content ", type=str)
    parser.add_argument(
        "sourceLang", help="Language of content to be translated ", type=str)
    parser.add_argument(
        "translatedLang", help="Langauge into which content is to be translated ", type=str)

    args = parser.parse_args()

    # Read input file
    text = readText(args.sourceFile)

    # Translate text from input file
    json_obj = translateText(text, args.sourceLang, args.translatedLang)

    # Write text to output file
    writeText(json_obj, args.translatedFile)

if __name__ == "__main__":
    main()
