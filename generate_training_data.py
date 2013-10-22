import csv, re, json

from generate_symptom_matrix import get_disease_symptoms

def get_disease_characteristics(disease):
    disease_characteristics = set([])

    disease_regex = re.compile(disease)

    with open('data/promed_with_characteristics.json') as f:
        nodes = json.loads(f.read())["nodes"]

        for node in nodes:
            match = disease_regex.search(node.get('title'))
            if match:
                disease_characteristics.update(node.get('characteristics').keys())
    return disease_characteristics


def get_symptom_map():
    with open('data/Master_clean_gideon_comparison.csv') as f:
        reader = csv.reader(f)
        reader.next()
        return dict([(row[1], row[0]) for row in reader])

def get_training_data_columns():
    with open('data/ProMED_master_clean.csv', 'rU') as f:
        reader = csv.reader(f)
        reader.next()
        return reader.next()

if __name__ == '__main__':
    DISEASES = [
    'Meningitis-bacterial',
    'Dengue',
    'Japanese Encephalitis',
    'Measles',
    'Malaria',
    'Meningitis -aseptic (viral)',
    'Nipah and Nipah-like Virus Disease',
    'Typhoid and Enteric Fever',
    'Chandipura and Vesicular stomatitis viruses',
    'Chikungunya',
    ]

    symptom_map = get_symptom_map()

    columns = get_training_data_columns()
    
    rows = [[0 for i in range(0, len(columns))] for j in range(0, len(DISEASES) + 1)]
    rows[0] = columns
    
    for disease_index in range(0, len(DISEASES)):
        rows[disease_index + 1][0] = DISEASES[disease_index]
        symptoms = [symptom_map.get(symptom) for symptom in get_disease_symptoms(DISEASES[disease_index]) if symptom in symptom_map.keys()]
        characteristics = get_disease_characteristics(DISEASES[disease_index])
        for column_index in range(0, len(columns)):
            if columns[column_index] in symptoms or columns[column_index] in characteristics:
                rows[disease_index + 1][column_index] = 1

    with open('data/Generated_master_clean_characteristics_1_0.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

