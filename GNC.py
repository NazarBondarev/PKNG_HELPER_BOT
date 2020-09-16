#GET NEW CHANGES

import schedule
import time
import requests
import convertapi



def job():
    r = requests.Session()
    url = "https://www.pkng.pl.ua/images/zminy/zm.pdf"
    result = r.get(url)

    with open('./data/zm.pdf', 'wb') as write_changes:
        write_changes.write(result.content)

    convertapi.api_secret = 'cSynglLVxKDzVTtF'

    result = convertapi.convert('csv', {'File': './data/zm.pdf'})

    # save to file
    result.file.save('./data/output.csv')


schedule.every().day.at("15:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)