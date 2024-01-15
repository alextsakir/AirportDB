"""
Examples of how to export Coordinate or Airport objects to an XML-like KML file format.
This can be done with method kml(), which can be used for both classes.
In addition, Airport.kml_route() method can be called with a second Airport as parameter to save a path between them.

After creating the KML files, you can go to kml folder and open them with Google Earth to see points, airports
and routes on map.
"""

from assets import Airport, Coordinates, database

airport: Airport = database.athens  # create an object of El. Venizelos airport
airport.description = "Eleftherios Venizelos is the largest international airport in Greece."
print(airport)
# airport.kml()

another_airport: Airport = database.airport("SKU")  # create another Airport object with its IATA code
# NOTE previous line same as Airport.db(database("select * from Airport where IATA = 'SKU'").fetchone())
another_airport.description = "Skyros is the southernmost island of the Sporades, an archipelago in the Aegean Sea."
print(another_airport)
# another_airport.kml()

my_point: Coordinates = Coordinates(x=20, y=42, label="my_point")  # create a Coordinates object
print(my_point)
# my_point.kml()

# airport.kml_route(another_airport)
