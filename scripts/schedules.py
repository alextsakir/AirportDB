from assets import *

QUERY = ("select code, A2.IATA, A.IATA, departure, arrival, days from Schedule "
         "join main.Airport A on A.flight_id = Schedule.end "
         "join main.Airport A2 on A2.flight_id = Schedule.start")

data = database(QUERY).fetchall()
for schedule in data:
    airline = database(f"select name from Airline where designator = '{schedule[0][:2]}'").fetchone()[0]
    print(schedule[0], airline, schedule[1], schedule[2], schedule[3], schedule[4], end="    ")
    print(" ".join([member.value[1] for member in Day.code_to_days(schedule[5])]))
