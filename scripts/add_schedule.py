from assets import *

'''
for i in range(10):
    other = database.random_airport_id()
    ath = database.cursor.execute("select id from Airport where IATA = 'ATH'").fetchone()[0]
    record = Schedule.random_tuple(database.random_airline_designator(), ath, other)
    print(record)
    database.cursor.execute("insert into Schedule(code, from_airport, to_airport, departure, arrival, days)"
                            "values (?, ?, ?, ?, ?, ?)", record)
'''

other = database.cursor.execute("select id from Airport where IATA = 'CTA'").fetchone()[0]
record = database.random_schedule("A3", other)
print(record)
database.cursor.execute("insert into Schedule(code, from_airport, to_airport, departure, arrival, days, modified, "
                        "active, occurrences) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (record.code, record.from_airport, record.to_airport, record.departure, record.arrival,
                         record.days, record.modified, record.active, record.occurrences))
