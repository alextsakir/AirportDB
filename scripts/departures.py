from assets import *


departures = database("select * from Flight where departure is null").fetchall()

for result in departures:
    print(result)
