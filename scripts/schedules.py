from assets import *

QUERY = ("select code, A2.IATA, A.IATA, departure, arrival, days from Schedule "
         "join main.Airport A on A.id = Schedule.to_airport "
         "join main.Airport A2 on A2.id = Schedule.from_airport")

data = database(QUERY).fetchall()
for schedule in data:
    airline = database(f"select name from Airline where designator = '{schedule[0][:2]}'").fetchone()[0]
    print(schedule[0], airline, schedule[1], schedule[2], schedule[3], schedule[4], sep="    ", end="    ")
    print("  ".join([member.value[1] for member in Day.code_to_days(schedule[5])]))
