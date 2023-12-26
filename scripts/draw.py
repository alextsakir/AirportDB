from assets import *

ath: Airport = Airport.db(database("select * from Airport where IATA = 'ATH'").fetchone())
other: Airport = Airport.db(database("select * from Airport where IATA = 'LCA'").fetchone())
print(ath.map(other))
