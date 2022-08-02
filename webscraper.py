from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

import requests


def getDrugInfo():
    ddinter = 1
    url_exists = True
    while url_exists:
        URL = f"http://ddinter.scbdd.com/ddinter/drug-detail/DDInter{ddinter}/"
        if requests.get(URL).status_code == 200:
            # get html
            page = urlopen(URL)
            html = page.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')

            links = soup.find_all('a')

            drug_bank_id = ""
            chembl_id = ""
            pubchem_id = ""

            for link in links:
                link_content = link['href']
                if 'chembl' in link_content:
                    chembl_id = link_content.split(
                        'https://www.ebi.ac.uk/chembl/compound_report_card/')[-1]
                if 'drugbank' in link_content:
                    drug_bank_id = link_content.split(
                        'https://go.drugbank.com/drugs/')[-1]
                if 'pubchem' in link_content:
                    pubchem_id = link_content.split(
                        'https://pubchem.ncbi.nlm.nih.gov/compound/')[-1]

            drug_info = {
                'ddinter': ddinter,
                'drugbank': drug_bank_id,
                'chembl': chembl_id,
                'pubchem': pubchem_id
            }
            ddinter += 1
            yield drug_info
        else:
            url_exists = False
            break


drug_info = getDrugInfo()

data = {'records': []}

for drug in drug_info:
    data['records'].append(drug)
    print(drug)

with open('drug_data.json', 'w') as f:
    json.dump(data, f)
