with MyTable as (select Airplane.type, Airplane.airline, Flight.code, Flight.to_airport, Flight.departure from Flight
join Airplane on Flight.airplane = Airplane.id
where departure > date() and departure < date('now','+1 month')),
AnotherTable as (select * from Airport)
select Airline.name, MyTable.type, AnotherTable.name, MyTable.code, MyTable.departure from MyTable
join Airline on MyTable.airline = Airline.id
join AnotherTable on MyTable.to_airport = AnotherTable.id;

select Flight.code, Flight.departure, FromAirport.name as from_airport, ToAirport.name as to_airport from Flight
join Airport as FromAirport on Flight.from_airport = FromAirport.id
join Airport as ToAirport on Flight.to_airport = ToAirport.id
where from_airport = 0 order by Flight.departure;

select count(Flight.id) as flight_count, Flight.code, ToAirport.name as to_airport from Flight
join Airport as ToAirport on Flight.to_airport = ToAirport.id
where from_airport = 0 group by ToAirport.name;
