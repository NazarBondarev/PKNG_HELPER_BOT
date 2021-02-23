import requests
from config import API_TOKEN, admin
import schedule
import time




class DumpSender:    

    def send_dump(self):
        self.r = requests.Session()
        url = f"https://api.telegram.org/bot{API_TOKEN}/sendDocument"
        files = {
    'chat_id': (None, admin),
    'document': open("./data/users.json", "rb")}
        self.r.post(url, files=files)

def job():
    DumpSender().send_dump()

schedule.every().day.at("01:00").do(job)
schedule.every().day.at("13:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)