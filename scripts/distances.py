from assets import *

print(database.athens, database.athens.local_time, "\n\n",
      database.athens.headers(), database.athens.measurements_headers(), sep="")

for result in database("select * from Airport where country != 'GREECE' order by long desc").fetchall():
    airport = Airport.db(result)
    print(airport, airport.local_time, database.athens.measurements(airport))

