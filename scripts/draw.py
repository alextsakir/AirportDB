from assets import *

ath: Airport = Airport.db(database.cursor.execute("select * from Airport where IATA = 'ATH'").fetchone())
other: Airport = Airport.db(database.cursor.execute("select * from Airport where IATA = 'LCA'").fetchone())
print(ath.map(other))
