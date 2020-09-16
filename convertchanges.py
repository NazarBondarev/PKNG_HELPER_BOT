import tabula
import csv
import requests
from pprint import pprint
import pdftables_api
from pdftables_api import Client

import config


def download_changes_from_site():

    changes = []
    with open('./data/output.csv', 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)

        for item in reader:
            if item[2].startswith('ЗМІНИ'):
                continue
            if item[0] != '':
                changes.append('➡<b>'+item[0]+'</b>'+'\n<b>✅'+item[1]+'</b> '+' - '.join(item[2:4])+'\n❌'+' - '.join(item[4::]))
            elif item[0] == '':
                add_study = f'➡{changes[-1]}'+ '\n<b>✅'+item[1]+'</b> '+' - '.join(item[2:4])+'\n❌'+' - '.join(item[4::])
                del changes[-1]
                changes.append(add_study)

    return changes
