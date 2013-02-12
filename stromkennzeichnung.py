#?/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import re

import db

YEARS = [2011]

URL = "http://www.stromkennzeichnung.ch/de/suche/powera/search/powerc/Supplier.html"

def to_db(zip, city, year, producer, percent):
    try:
        pass
    except:
        pass


def get_html(zip, city, year):
    dct = {
        'tx_cabagpowerdeclaration_powerlisting[zip]': '%s, %s' % (zip, city),
        'tx_cabagpowerdeclaration_powerlisting[sortbyYear]': year
    }
    r = requests.post(URL, dct)
    return r.text

def get_data(zip, city, year):
    def match_bar(html_code):
        match = re.search(r"OverTooltip\('([^']+)', '([\d.]+)%", unicode(html_code))
        return match.groups()

    html = get_html(zip, city, year)
    b = BeautifulSoup(html)
    content = b.find(class_='tx-cabag-powerdeclaration')
    content = content.find(class_='results')

    producer = content.find_all(class_='hoverEffect')[1].find(class_='label').text
    bars = content.find(class_='barBox').find_all(class_='bar')
    return producer, dict([match_bar(b) for b in bars])

def get_cities(file):
    cities = []
    with open(file) as f:
        for line in f:
            print line
    return cities


#data = get_data(8500, 'Frauenfeld', '2011')
for year in YEARS:
    for zip, city in get_cities('cities.csv'):
        producer, percent = get_data(zip, city, year)
        to_db(zip, city, year, producer, percent)
