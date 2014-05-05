import csv
import nltk
from collections import OrderedDict

diseaseDict = OrderedDict()
symptomDict = OrderedDict()
d_s = 0
s_s = 0

def developSymptomDict():
	with open("list_symptoms.csv") as f:
		reader = csv.reader(f)
		for row in reader:
			symptomDict[row[0]] = 0

def developDiseaseDict():
	with open("disease_definitions.csv") as f:
		reader = csv.reader(f)
		for row in reader:
			diseaseDict[row[0]] = 0
def main():
	global diseaseDict, symptomDict
	developSymptomDict()
	developDiseaseDict()
        file_list = ['files1.csv']
        #file_list = ['A_B_files.csv']
        header = "doi,year,month,article_title,abstract,keywords,journal_title,journal_publisher,journal_volume,journal_issue".split(",")
        csv.field_size_limit(100000000)
        for file_name in file_list:
               abstract_count = 0
               f = open(file_name,"r")
               reader = csv.DictReader(f,header)
               for row in reader:
                        if row['abstract'] != "na":
	   			frequencyCount(row['abstract'])
	
	f = open("symptom_count.csv", "w")
	for key, val in symptomDict.items():
		str_val = key + "," + str(val)
		f.write(str_val)
		f.write("\n")
	f.close()
	
	f = open("disease_count.csv", "w")
        for key, val in diseaseDict.items():
                str_val = key + "," + str(val)
                f.write(str_val)
                f.write("\n")
        f.close()


def frequencyCount(abstract):
	global diseaseDict, symptomDict
	stopwords = set(nltk.corpus.stopwords.words('english'))
	for sentence in nltk.tokenize.sent_tokenize(abstract):
		for term in nltk.tokenize.word_tokenize(sentence):
			if term not in stopwords:
				for key, val in diseaseDict.items():
					if key.lower() == term.lower():
						diseaseDict[key] += 1
				for key, val in symptomDict.items():
					if key.lower() == term.lower():
						symptomDict[key] += 1

if __name__ == '__main__':
        main()

