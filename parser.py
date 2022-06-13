import glob
import pandas as pd
import os


def load_data(data_folder):
    csv_files = os.path.join(data_folder, "ddinter_downloads_code_*.csv")
    joined_csv_files = glob.glob(csv_files)
    merged_csv = pd.concat(
        map(pd.read_csv, joined_csv_files), ignore_index=True)

    for index in merged_csv.index:
        DDInterID_A = merged_csv['DDInterID_A'][index]
        Drug_A = merged_csv['Drug_A'][index]
        DDInterID_B = merged_csv['DDInterID_B'][index]
        Drug_B = merged_csv['Drug_B'][index]
        Level = merged_csv['Level'][index]

        doc = {}
        doc['_id'] = DDInterID_A+'_'+DDInterID_B+'_'+Level
        doc['drug_a'] = {'ddinterid_a': DDInterID_A, 'name': Drug_A}
        doc['drug_b'] = {'ddinterid_b': DDInterID_B, 'name': Drug_B}
        doc['level'] = Level

        yield doc
