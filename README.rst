Data scraping of http://www.stromkennzeichnung.ch/
--------------------------------------------------

part of http://zurich.greenhackathon.com/

We prepared the commune borders (gis data from bfs). In german "Gemeindegrenzen":
https://www.google.com/fusiontables/data?docid=1MONckRl1jpicYQLdD4DEY-WbM5675HaMElIP3vY#rows:id=1

Then we scaped all the data from `stromkennzeichnung.ch`:
https://www.google.com/fusiontables/DataSource?docid=18OLJxgKhK-LDKcaJlJyQ-Uf3gMj4VhrGvldY3Ks

and then we merged these fusiontables:
https://www.google.com/fusiontables/data?docid=1HVvgnnPIYuBzRit4R4B4Au1sxtsvVH0ExEyUoaw#map:id=3

As you can see, some communes have no data (red). The default display is how
much nuclear power (percent of use) a commune uses. You can see that in the
mountains and in the french and italian speaking parts nuclear energy is much
less used than in the "Mittelland".
