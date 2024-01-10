from assets import *

data = database("select code from Schedule where occurrences = ?", (0,)).fetchall()
data = [element[0] for element in data]
print(data)

for flight_code in data:
    airline = database("select id, name, airplanes from Airline where designator = ?", (flight_code[:2],)).fetchall()
    print(airline)
    if airline[0][2] == 0:
        continue

    # database.generate_scheduled_flights(flight_code)

# database.states_init()
# database.null_rectifier()
database.update_schedule_occurrences()
