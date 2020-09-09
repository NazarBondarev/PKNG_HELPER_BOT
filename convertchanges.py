import tabula
import csv
import requests
from pprint import pprint

def download_changes_from_site():
    r = requests.Session()
    url = "https://www.pkng.pl.ua/images/zminy/zm.pdf"
    result = r.get(url)

    with open('./data/zm.pdf', 'wb') as write_changes:
        write_changes.write(result.content)

    try:
        tabula.convert_into('./data/zm.pdf', "./data/output.csv", output_format="csv", pages='all')
    except UnicodeDecodeError:
        pass

    with open('output.csv', 'r') as file:
        reader = csv.reader(file)

        changes = []
        try:

            for item in reader:
                if item[0] != '':
                    changes.append('➡<b>'+item[0]+'</b>'+'\n<b>✅'+item[1]+'</b> '+' - '.join(item[2:4])+'\n❌'+' - '.join(item[4::]))
                elif item[0] == '':
                    add_study = f'➡{changes[-1]}'+ '\n<b>✅'+item[1]+'</b> '+' - '.join(item[2:4])+'\n❌'+' - '.join(item[4::])
                    del changes[-1]
                    changes.append(add_study)

            return changes
        except UnicodeDecodeError:
            pass
