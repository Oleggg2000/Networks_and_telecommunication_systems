import requests
from bs4 import BeautifulSoup
import time

DOLLAR_RUB = "https://is.gd/5IndWR"
EURO_RUB = "https://is.gd/qCZ8I7"
JPY_RUB = "https://is.gd/e2pjdU"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

def check_currency(Currency):
    full_page = requests.get(Currency, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span", {"class": "DFlfde SwHCTb"})
    return float((convert[0].text).replace(",", "."))