from assets import *

print(athens, athens.local_time, "\n\n", athens.headers(), athens.measurements_headers(), sep="")

for result in database.execute("select * from Airport where country != 'GREECE' order by long desc").fetchall():
    airport = Airport.db(result)  # NOTE ----------------------------------------------- equivalent to Airport(*result)
    print(airport, airport.local_time, athens.measurements(airport))

