import json, re, csv

def get_disease_symptoms(disease):
    disease_symptoms = set([])

    disease_regex = re.compile(disease)

    with open('data/promed_network_with_symptoms_and_diseases.json') as f:
        nodes = json.loads(f.read())["nodes"]

        for node in nodes:
            match = disease_regex.search(node.get('title'))
            if match:
                disease_symptoms.update(node.get('symptoms'))
    return disease_symptoms

def load_symptoms():
    symptoms = None
    with open('data/Matrix_symp_dis_v3.csv', 'rU') as f:
        reader = csv.reader(f)
        reader.next()  # skip header
        symptoms = [row[0] for row in reader]

    return symptoms


if __name__ == '__main__':
    DISEASES = ['Novel coronavirus', 'H7N9']
    disease_symptoms = [get_disease_symptoms(disease) for disease in DISEASES]
    symptoms = load_symptoms()

    rows = [[0 for i in range(0, len(DISEASES) + 1)] for j in range(0, len(symptoms) + 1)]
    rows[0][0] = 'Symptom'
    rows[0][1:len(DISEASES) + 1] = DISEASES

    for i in range(0, len(symptoms)):
        rows[i + 1][0] = symptoms[i]
        for j in range(0, len(DISEASES)):
            if symptoms[i] in disease_symptoms[j]:
                rows[i + 1][j + 1] = 1

    with open('data/Generated_matrix_symp_dis.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rows)






    


