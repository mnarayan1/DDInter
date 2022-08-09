import glob
import pandas as pd
import os
import json


def load_data(data_folder):
    ddinter_filepath = os.path.join(data_folder, "ddinter_downloads_code_*.csv")
    ddinter_blob = glob.glob(ddinter_filepath)
    ddinter_df = pd.concat(map(pd.read_csv, ddinter_blob), ignore_index=True)

    # load file with scraped data
    drug_filepath = os.path.join(data_folder, 'drug_data.json')
    with open(drug_filepath) as f:
        drug_data = json.load(f)['records']

        drug_characteristics = ['chembl', 'pubchem', 'drugbank']

        for index in ddinter_df.index:
            level = ddinter_df['Level'][index]

            drug_a_id = ddinter_df['DDInterID_A'][index]
            drug_a_name = ddinter_df['Drug_A'][index]
            drug_a_index = int(drug_a_id.split('DDInter')[-1])

            drug_b_id = ddinter_df['DDInterID_B'][index]
            drug_b_name = ddinter_df['Drug_B'][index]
            drug_b_index = int(drug_b_id.split('DDInter')[-1])

            doc = {}
            doc['_id'] = drug_a_id + '_' + drug_b_id + '_' + level
            doc['level'] = level

            doc['drug_a'] = {
                'ddinterid_a': drug_a_id,
                'name': drug_a_name,
            }

            for characteristic in drug_characteristics:
                info = drug_data[drug_a_index-1][characteristic]
                if len(info) > 0:
                    doc['drug_a'][characteristic] = info

            doc['drug_b'] = {
                'ddinterid_b': drug_b_id,
                'name': drug_b_name,
            }

            for characteristic in drug_characteristics:
                info = drug_data[drug_b_index-1][characteristic]
                if len(info) > 0:
                    doc['drug_b'][characteristic] = info

            yield doc
