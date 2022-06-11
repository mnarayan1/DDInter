import csv
import os


def load_data(data_folder):
    with open(os.path.join(data_folder, 'ddinter_downloads_code_A.csv'), 'r') as f:
        original_data = csv.reader(f)

    print(original_data)

    for row in original_data:
        DDInterID_A = row[0]
        Drug_A = row[1]
        DDInterID_B = row[2]
        Drug_B = row[3]
        Level = row[4]

        doc = {}
        doc['_id'] = DDInterID_A+'_'+DDInterID_B+'_'+Level
        doc['drug_a'] = {'ddinterid_a': DDInterID_A, 'name': Drug_A}
        doc['drug_b'] = {'ddinterid_b': DDInterID_B, 'name': Drug_B}
        doc['level'] = Level

        yield doc


test_data = load_data('data')

print(test_data)
