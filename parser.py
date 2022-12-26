import glob
import pandas as pd
import os
import json
import urllib.request
from string import ascii_uppercase as alc


def load_data(data_folder):
    # download all DDInter csv files
    print("getting records")
    for i in alc:
        try:
            file = f"ddinter_downloads_code_{i}.csv"
            url = f"http://ddinter.scbdd.com/static/media/download/{file}"
            filepath = os.path.join(data_folder, file)
            urllib.request.urlretrieve(url, filepath)
        except Exception:
            pass

    # merge DDInter records from all csv files into one csv
    csv_files = os.path.join(data_folder, "ddinter_downloads_code_*.csv")
    joined_csv_files = glob.glob(csv_files)
    merged_csv = pd.concat(
        map(pd.read_csv, joined_csv_files), ignore_index=True)

    # load file with scraped data
    drug_info_file = os.path.join(data_folder, 'drug_data.json')
    drug_info = open(drug_info_file)
    drug_data = json.load(drug_info)['records']

    drug_characteristics = ['chembl', 'pubchem', 'drugbank']

    ids = []

    for index in merged_csv.index:
        DDInterID_A = merged_csv['DDInterID_A'][index]
        Drug_A = merged_csv['Drug_A'][index]
        DDInterID_A_index = int(DDInterID_A.split('DDInter')[-1])
        DDInterID_B = merged_csv['DDInterID_B'][index]
        Drug_B = merged_csv['Drug_B'][index]
        DDInterID_B_index = int(DDInterID_B.split('DDInter')[-1])
        Level = merged_csv['Level'][index]
        id = DDInterID_A+'_'+DDInterID_B+'_'+Level

        if id not in ids:
            doc = {}
            doc['_id'] = id
            doc['drug_a'] = {
                'ddinterid': DDInterID_A,
                'name': Drug_A,
            }

            for characteristic in drug_characteristics:
                info = drug_data[DDInterID_A_index-1][characteristic]
                if len(info) > 0:
                    doc['drug_a'][characteristic] = info

            doc['drug_b'] = {
                'ddinterid': DDInterID_B,
                'name': Drug_B,
            }

            for characteristic in drug_characteristics:
                info = drug_data[DDInterID_B_index-1][characteristic]
                if len(info) > 0:
                    doc['drug_b'][characteristic] = info

            doc['level'] = Level

            ids.append(id)
            print(doc)
            yield doc
        else:
            continue


records = load_data('./test')

for record in records:
    print(record)
