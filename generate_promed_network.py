from glob import glob
import re, json, csv

symptoms = []
diseases = []
matched_symptoms = set([])
matched_diseases = set([])

def _find_symptoms_and_diseases(text_to_search):
    if len(diseases) < 1:
        _load_matrix_data()

    text_symptoms = set()
    text_diseases = set()

    for symptom in symptoms:
        if symptom[1].search(text_to_search):
            text_symptoms.add(symptom[0])
    for disease in diseases:
        if disease[1].search(text_to_search):
            text_diseases.add(disease[0])

    return ([symptom for symptom in text_symptoms], [disease for disease in text_diseases])


def _load_matrix_data():
    with open('data/Matrix_symp_dis_v3.csv', 'rU') as f:
        reader = csv.reader(f)
        
        global diseases, symptoms
        diseases = [(disease.lower(), re.compile(disease, flags=re.IGNORECASE)) for disease in reader.next()[1:]]

        symptoms = [(row[0], re.compile(row[0], flags=re.IGNORECASE)) for row in reader]
    

def generate_promed_network():

    REPORT_PATH = 'data/promed/'
    files = glob('%s/*.txt' % REPORT_PATH)

    report_id_regex = re.compile('\d{8}\.\d+')
    label_regex = re.compile('>.*?Archive Number')
    source_regex = re.compile('Source:.*?  ')

    promed_ids = []
    nodes = []
    edges = []
    links = []
    for file in files:
        with open(file) as f:
            report = f.read()
            report_ids = report_id_regex.findall(report)

            if report_ids:
                match = label_regex.search(report)
                if match:
                    label = match.group(0)[1:-14].strip()
                else:
                    label = ''

                disease = label.split('update')[0].split(' - ')[0].strip()

                temp = label.split(' - ')
                if len(temp) > 1:
                    location = temp[1].split('(')[0].strip()
                else:
                    location = ''

                source_match = source_regex.search(report)
                if source_match:
                    source = source_match.group(0)[7:-1].strip()
                else:
                    source = ''

                text_to_search = report
                try:
                    see_also_start = report.index('See Also')
                except ValueError as e:
                    # no see alsos in report
                    see_also_start = len(report)
                text_to_search = report[0:see_also_start]
                matched_symptoms, matched_diseases = _find_symptoms_and_diseases(text_to_search)

                promed_ids.append(report_ids[0])
                nodes.append({'promed_id': report_ids[0], 'title': label, 'disease': disease, 'location': location, 'source_organization': source, 'symptoms': matched_symptoms, 'diseases': matched_diseases, 'symptom_count': len(matched_symptoms), 'disease_count': len(matched_diseases)})
                for report_id in report_ids[1:]:
                    edges.append((report_ids[0], report_id))

    for edge in edges:
        if edge[0] in promed_ids and edge[1] in promed_ids:
            links.append({'source': edge[0], 'target': edge[1]})

    return {'nodes': nodes, 'links': links}

if __name__ == '__main__':
    print json.dumps(generate_promed_network())



