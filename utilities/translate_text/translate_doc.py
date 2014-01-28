# script to translate a document from one language to another

import urllib2
import json
import argparse

def translateText(source_text, source_lang, dest_lang, API_KEY):
# Function to translate text

    # Reconstruct input text to build url for Google translate
    # URL
    source_text = source_text.replace("%", " ").replace("\n", " ")
    source_text = urllib.quote(source_text)

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
           }
    link = "https://www.googleapis.com/language/translate/v2?key=" + API_KEY + \
        "&source=" + source_lang + "&target=" + dest_lang + "&q=" + source_text

    # Send request and convert response to json object
    req = urllib2.Request(link, headers=hdr)
    response = urllib2.urlopen(req)
    text = response.read()
    json_obj = json.loads(text)
    
    # Extract translated text from json object
    translated_text = json_obj['data']['translations'][0]['translatedText']
    translated_text = translated_text.encode('utf-8')

    return translated_text

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
    parser.add_argument(
	"apikey", help="API Key from Google Translate API", type=str)

    args = parser.parse_args()

    # Read input file
    f_in = open(args.sourceFile)
    source_text = f_in.read()

    # Translate text from input file
    translated_text = translateText(source_text, args.sourceLang, args.translatedLang, args.apikey)

    # Write value of key 'translatedText' from returned JSON object
    # into output file
    f_out = open(args.translatedFile, "w")
    f_out.write(translated_text)
    f_out.close()

if __name__ == "__main__":
    main()
