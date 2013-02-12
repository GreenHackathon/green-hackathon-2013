#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import re

import db


YEARS = [2011]

URL = "http://www.stromkennzeichnung.ch/de/suche/powera/search/powerc/Supplier.html"


class NotFoundError(Exception):
    pass


def to_db(zip, city, year, producer, percents):
    """
    This code is really ugly, I've never used sqlalchemy before and I really
    don't get it.
    """
    session = db.Session()
    try:
        _producer = session.query(db.Producer).filter(db.Producer.name == producer).all()[0]
    except IndexError:
        _producer = db.Producer(producer, year)
        session.add(_producer)
        session.commit()

    try:
        _city = session.query(db.City).filter(db.City.name == city,
                                              db.City.zip == zip,
                                              ).all()[0]
    except IndexError:
        _city = db.City(city, zip, _producer)
        session.add(_city)
        session.commit()

    for source, percent in percents.items():
        try:
            _source = session.query(db.Source).filter(db.Source.name == source).all()[0]
        except IndexError:
            _source = db.Source(source)
            session.add(_source)
            session.commit()
        try:
            _source = session.query(db.Percent).filter(
                                        db.Percent.producer_id == _producer.id,
                                        db.Percent.source_id == _source.id
                                        ).all()[0]
        except IndexError:
            _percent = db.Percent(_producer, _source, percent)
            session.add(_percent)
            session.commit()



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
        label, percent = match.groups()
        label = re.sub('_\d+', '', label)
        return label, percent

    html = get_html(zip, city, year)
    b = BeautifulSoup(html)
    content = b.find(class_='tx-cabag-powerdeclaration')
    content = content.find(class_='results')

    if content is None:
        raise NotFoundError('no content for %s, %s, %s' % (zip, city, year))

    row = content.find_all(class_='row hoverEffect')[1]
    producer = row.find(class_='label').text
    try:
        bars = row.find(class_='barBox').find_all(class_='bar')
    except AttributeError:
        return producer, {}
    else:
        return producer, dict([match_bar(b) for b in bars])


def get_cities(file):
    cities = {}
    with open(file) as f:
        for line in f:
            fields = unicode(line, 'latin-1').split('\t')
            try:
                zip = fields[2]
                city = fields[4]
            except IndexError:
                pass
            else:
                if zip not in cities:
                    cities[zip] = city
    return sorted(cities.items(), key=lambda x: x[0])


#cities = get_cities('plz_l_20130121.txt')
#print cities[:10], len(cities)
#data = get_data(8500, 'Frauenfeld', '2011')

for year in YEARS:
    for zip, city in get_cities('plz_l_20130121.txt'):
        try:
            producer, percents = get_data(zip, city, year)
        except NotFoundError as e:
            print '>>>> ' + e.message
        else:
            print 'found data for %s, %s' % (zip, city)
            to_db(zip, city, year, producer, percents)
