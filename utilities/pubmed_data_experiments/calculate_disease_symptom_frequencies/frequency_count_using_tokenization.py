# Script to calculate disease and symptom frequencies
# in abstracts from PubMED Open Access Dataset. For this
# purpose, PubMED abstracts were used.
import csv
import nltk
from collections import OrderedDict

# Global dictionaries which hold disease and
# symptom dictionaries
diseaseDict = OrderedDict()
symptomDict = OrderedDict()

# Function to initialize symptom dictionary


def developSymptomDict():
    with open("list_symptoms.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            symptomDict[row[0]] = 0

# Function to initialize disease dictionary


def developDiseaseDict():
    with open("disease_definitions.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            diseaseDict[row[0]] = 0


def main():
    global diseaseDict, symptomDict
    developSymptomDict()
    developDiseaseDict()

    # This is being done to process files in large or small
    # chunks. However, if an alternative is found, it is to
    # be changed.
    file_list = ['pubmed_data.csv']
    header = "doi,year,month,article_title,abstract,keywords,journal_title,journal_publisher,journal_volume,journal_issue".split(
        ",")
    csv.field_size_limit(100000000)

    # Read each file(s) from file list
    for file_name in file_list:
        abstract_count = 0
        f = open(file_name, "r")
        reader = csv.DictReader(f, header)
        for row in reader:
            if row['abstract'] != "na":

                # Call function to calculate frequencies of
                #symptoms and diseases in abstracts
                frequencyCount(row['abstract'])

    # Write symptom dictionary to file
    f = open("symptom_count.csv", "w")
    for key, val in symptomDict.items():
        str_val = key + "," + str(val)
        f.write(str_val)
        f.write("\n")
    f.close()

    # Write disease dictionary to file
    f = open("disease_count.csv", "w")
    for key, val in diseaseDict.items():
        str_val = key + "," + str(val)
        f.write(str_val)
        f.write("\n")
    f.close()


# Main function to calculate frequencies
def frequencyCount(abstract):
    global diseaseDict, symptomDict

    # Initialize list of NLTK stopwords
    stopwords = set(nltk.corpus.stopwords.words('english'))

    # Tokenize abstract to sentence level
    for sentence in nltk.tokenize.sent_tokenize(abstract):

        # Tokenize each sentence to term level
        for term in nltk.tokenize.word_tokenize(sentence):

            # Verify if term is a stop word and proceed only
            # if not
            if term not in stopwords:

                # If term is present in disease dictionary,
                # increment count by 1
                for key, val in diseaseDict.items():
                    if key.lower() == term.lower():
                        diseaseDict[key] += 1

                # If term is present in symptom dictionary,
                # increment county by 1
                for key, val in symptomDict.items():
                    if key.lower() == term.lower():
                        symptomDict[key] += 1

if __name__ == '__main__':
    main()
