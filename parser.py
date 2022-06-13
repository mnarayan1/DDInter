import glob
import pandas as pd
import os


def load_data(data_folder):

    # merging the files
    joined_files = os.path.join(data_folder, "ddinter_downloads_code_*.csv")

    # A list of all joined files is returned
    joined_list = glob.glob(joined_files)

    df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)

    for index in df.index:
        DDInterID_A = df['DDInterID_A'][index]
        Drug_A = df['Drug_A'][index]
        DDInterID_B = df['DDInterID_B'][index]
        Drug_B = df['Drug_B'][index]
        Level = df['Level'][index]

        doc = {}
        doc['_id'] = DDInterID_A+'_'+DDInterID_B+'_'+Level
        doc['drug_a'] = {'ddinterid_a': DDInterID_A, 'name': Drug_A}
        doc['drug_b'] = {'ddinterid_b': DDInterID_B, 'name': Drug_B}
        doc['level'] = Level

        yield doc
