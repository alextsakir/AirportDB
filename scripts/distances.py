from assets.models import Airport
from assets import *


ath: Airport = Airport.db(database.execute("select * from Airport where IATA = 'ATH'").fetchone())
print(ath, ath.local_time, "\n\n", ath.headers(), ath.measurements_headers(), sep="")

for result in database.execute("select * from Airport where country != 'GREECE' order by long desc").fetchall():
    airport = Airport.db(result)  # ---------------------------------------------------- equivalent to Airport(*result)
    print(airport, airport.local_time, ath.measurements(airport))

