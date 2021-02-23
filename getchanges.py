from pdf2image import convert_from_path
import requests


class GetChanges:
    def __init__(self, r=None, url=None):
        self.r = requests.Session()
        self.url = "https://www.pkng.pl.ua/images/zminy/zm.pdf"
    
    def get_changes(self):

        with open("./data/zm.pdf", "wb") as get:
            get.write(self.r.get(self.url).content)

        pages = convert_from_path('./data/zm.pdf', 0)
        pages[0].save('./data/zm.jpg', 'JPEG')

        return True

GetChanges().get_changes()