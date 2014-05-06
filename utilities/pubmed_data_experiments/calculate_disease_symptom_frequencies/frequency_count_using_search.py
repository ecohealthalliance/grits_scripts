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

    #Iterate through disease dictionary to verify 
    #if any diseases are referred to in abstracts
    for key, val in diseaseDict.items():
         term = '\\b(' + key.lower() + ')\\b'
         match = re.search(term, abstract)
         if match is not None:
             diseaseDict[key] += 1

     #Iterate through symptom dictionary to verfiy
     #if any symptoms are referred to in abstracts
     for key, val in symptomDict.items():
         term = '\\b(' + key.lower() + ')\\b'
         match = re.search(term, abstract)
         if match is not None:
             symptomDict[key] += 1

if __name__ == '__main__':
    main()
