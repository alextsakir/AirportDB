from assets import *

other = database("select id from Airport where IATA = 'LCA'").fetchone()[0]
record = database.random_schedule("FR", other)
print(record)
database("insert into Schedule(code, from_airport, to_airport, departure, arrival, days, modified, "
         "active, occurrences) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
         (record.code, record.from_airport, record.to_airport, record.departure, record.arrival,
          Day.days_to_code(record.days), record.modified, record.active, record.occurrences))
