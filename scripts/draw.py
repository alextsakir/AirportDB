from assets import *

print(database.athens.map(database.airport("LCA")))
my_airport = database.airport("BEG")
print(my_airport.map(database.airport("MLA")))

