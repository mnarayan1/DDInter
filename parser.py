import glob
import pandas as pd
import os
import json


def load_data(data_folder):
    csv_files = os.path.join(data_folder, "ddinter_downloads_code_*.csv")
    joined_csv_files = glob.glob(csv_files)
    merged_csv = pd.concat(
        map(pd.read_csv, joined_csv_files), ignore_index=True)

    # load file with scraped data
    drug_info = os.path.join(data_folder, 'drug_data.json')
    drug_data = json.load(drug_info)['records']

    drug_characteristics = ['chembl', 'pubchem', 'drugbank']

    for index in merged_csv.index:
        DDInterID_A = merged_csv['DDInterID_A'][index]
        Drug_A = merged_csv['Drug_A'][index]
        DDInterID_A_index = int(DDInterID_A.split('DDInter')[-1])
        DDInterID_B = merged_csv['DDInterID_B'][index]
        Drug_B = merged_csv['Drug_B'][index]
        DDInterID_B_index = int(DDInterID_B.split('DDInter')[-1])
        Level = merged_csv['Level'][index]

        doc = {}
        doc['_id'] = DDInterID_A+'_'+DDInterID_B+'_'+Level
        doc['drug_a'] = {
            'ddinterid_a': DDInterID_A,
            'name': Drug_A,
        }

        for characteristic in drug_characteristics:
            info = drug_data[DDInterID_A_index-1][characteristic]
            if len(info) > 0:
                doc['drug_a'][characteristic] = info

        doc['drug_b'] = {
            'ddinterid_b': DDInterID_B,
            'name': Drug_B,
        }

        for characteristic in drug_characteristics:
            info = drug_data[DDInterID_B_index-1][characteristic]
            if len(info) > 0:
                doc['drug_b'][characteristic] = info

        doc['level'] = Level

        yield doc
