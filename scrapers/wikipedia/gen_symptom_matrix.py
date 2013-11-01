#Script to generate a symptom matrix from 
#a list of symptoms and list of symptom definitions

import csv
import numpy as np
import re
import collections as col
import argparse

#List to hold symptoms
symptomList = []

#List to hold diseases
diseaseList = []

def generateSymptomList(f_symp_file):
# Function to extract create symptom list
	with open(f_symp_file,"r") as s:
		s_reader = csv.reader(s)
		for symptom in s_reader:	
			symp = symptom[0].replace("\"","")
			symptomList.append(symp.lower())

def writeToFile(f_out_file, matrix):
#Write final matrix values to output file

	#Write headers to output file
	f_out = open(f_out_file,"w")
	f_out.write(",")
	f_out.write(",".join(diseaseList))
	f_out.write("\n")

	#Write matrix to output file
	for i,symptom in enumerate(symptomList):
		new_text = symptom + "," + ",".join(str(x) for x in matrix[i,0:len(symptomList)].tolist())
		f_out.write(new_text)
		f_out.write("\n")
def main():	
	parser = argparse.ArgumentParser()
	parser.add_argument(
        	"symptomFile", help="CSV input file having list of symptoms", type=str)
    	parser.add_argument(
        	"definitionFile", help="CSV input file having scraped Wikipedia symptoms in format (disease name, symptom definition) ", type=str)
    	parser.add_argument(
        	"outputFile", help="CSV outfile file to store symptom matrix ", type=str)


    	args = parser.parse_args()
    	f_symp_file = args.symptomFile
    	f_def_file = args.definitionFile
	f_out_file = args.outputFile	

	generateSymptomList(f_symp_file)
	f_p = open(f_def_file,"r")
	readText = csv.reader(f_p, delimiter=',', quotechar='"')
	matrix_symp_dis = None

	countNa = 0
	
	#Iterate through each tuple 
	for row in readText:
		if row[1] == "na":
			countNa += 1
			continue
		#Create an empty symptom dictionary 
		sym_dict = col.OrderedDict((sym,0) for sym in symptomList)
		symptom_l = ""

		#Populating disease list
		disease = row[0]
		diseaseList.append(disease)

		symp_def = row[1].lower()
		symp_count = np.zeros(len(symptomList), dtype=np.int)		

		#Verify if symptom term is present in definition. If yes, 
		#mark corresponding key in symptom dictionary.
		for symptom in symptomList:
				regex = re.compile('[\d\D]*%s[\d\D]*'%symptom)
				if regex.match(symp_def) is not None:
					sym_dict[symptom] = 1

		#Transfer values from symptom dictionary to array
		symp_count = np.array([val for val in sym_dict.values()], dtype=np.int)

		#Create a matrix of dimensions (number of diseases X number of symptoms )
		if matrix_symp_dis is None:
			matrix_symp_dis = symp_count
		else:
			matrix_symp_dis = np.vstack((matrix_symp_dis,symp_count))

	#Write transposed matrix to output file
	writeToFile(f_out_file, matrix_symp_dis.T)
	print "Number of nas : " + str(countNa) 
			
if __name__ == "__main__":
	main()
