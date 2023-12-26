import csv

from assets import database

file = csv.reader(open("airplanes.csv"), delimiter=';')

airline_dict: dict[str, int] = {}
for airline in database(f"select * from Airline").fetchall():
    airline_dict[airline[1]] = airline[0]

print(airline_dict)

for index, data in enumerate(file):
    if index == 0: continue
    print(index, data)
    airline_id: int = airline_dict[data[2]]
    print(airline_id)
    database(f"insert into Airplane (type, airline) values ('{data[1]}', {airline_id})")
