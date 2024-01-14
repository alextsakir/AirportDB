from assets import *

flight_codes = [element[0] for element in database("select code from Schedule where active = 1 and occurrences = ? "
                                                   "and modified > datetime('2024-01-01') ",
                                                   (0,)).fetchall()]
# print(len(flight_codes))

for flight_code in flight_codes:
    print(flight_code)
    # database.generate_scheduled_flights(flight_code)
