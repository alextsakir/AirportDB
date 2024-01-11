from assets import *


departures = database("select * from Flight where departure is not null").fetchall()

for result in departures:
    print(result)
