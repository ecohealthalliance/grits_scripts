import csv

diseases_by_symptom = None

def _load_matrix_data():
	global diseases_by_symptom
	with open('data/Matrix_symp_dis_v4.csv') as f:
		reader = csv.DictReader(f, delimiter='\t')
		diseases_by_symptom = {}
		for row in reader:
			diseases_by_symptom[row.get('Symptom').lower()] = [disease for disease, present in row.iteritems() if present is '1']
		return diseases_by_symptom

def diagnose_symptoms(symptoms):
	if not diseases_by_symptom:
		_load_matrix_data()
	possible_diseases = {}
	for symptom in symptoms:
		for disease in diseases_by_symptom.get(symptom.lower()) or []:
			if not possible_diseases.get(disease):
				possible_diseases[disease] = []
			possible_diseases[disease].append(symptom)

	if len(possible_diseases):
		max_symptom_diagnosis = max(possible_diseases.iterkeys(), key=(lambda (key): len(possible_diseases[key])))
		max_symptoms = len(possible_diseases[max_symptom_diagnosis])
		return [disease for disease in possible_diseases.iterkeys() if len(possible_diseases[disease]) is max_symptoms]
	else:
		return []
