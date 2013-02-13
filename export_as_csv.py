#!/usr/bin/env python

import csv

import psycopg2


URI = "dbname='green_hackathon' user='david' password='david'"

try:
    conn=psycopg2.connect("dbname='green_hackathon' user='david' password='david'")
except:
    print "I am unable to connect to the database."

cur = conn.cursor()

cur.execute("""SELECT * from source""")
source_rows = cur.fetchall()
#source_rows = [(r[0], unicode(r[1], 'UTF-8')) for r in source_rows]

query = """
SELECT zip, city.name, p.name, %s
FROM city JOIN producer p on p.id = city.producer_id"""

legend = ['PLZ', 'Stadt', 'Anbieter']

add_result = []
for r_id, typ in source_rows:
    query += '\nLEFT JOIN percent p%s ' \
             'ON p%s.producer_id=p.id and p%s.source_id=%s' \
                                                    % (r_id, r_id, r_id, r_id)
    add_result.append('p%d.percent' % r_id)
    legend.append(typ)


query = query % (', '.join(add_result))
print query
cur.execute(query)
rows = cur.fetchall()

with open('strom_mix.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(legend)
    for row in rows:
        rest = row[3:]
        if [r for r in rest if r is not None]:
            row = row[:3] + tuple(r or 0 for r in rest)
        writer.writerow(row)
