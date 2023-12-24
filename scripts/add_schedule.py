from assets import *

# print(Day.days_to_code([Day.MONDAY, Day.TUESDAY]))

for i in range(10):
    other = database.random_airport_id()
    ath = database.cursor.execute("select flight_id from Airport where IATA = 'ATH'").fetchone()[0]
    record = Schedule.random_tuple(database.random_airline_designator(), ath, other)
    print(record)
    database.cursor.execute("insert into Schedule(code, start, end, departure, arrival, days)"
                            "values (?, ?, ?, ?, ?, ?)", record)
