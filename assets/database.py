__all__: tuple[str] = "database"

from datetime import datetime as _dt, date as _date, timedelta as _timed
from enum import Enum
import sqlite3 as _sql
from random import choice as _ch, randint as _rand, shuffle as _shuf
from types import GeneratorType
from typing import ClassVar, NoReturn, Self, Union, Optional, Any

from assets.constants import DATABASE
from assets import models


class Database:
    class Tables(Enum):  # NOTE UNUSED
        pass  # ---- --------- members filled in __init__, could not use Tables.__setattr__ because Enum's immutability

    _MONTH: ClassVar[tuple[int, int]] = 2024, 2
    _DEBUG: ClassVar[bool] = False
    _PRINT_QUERIES: ClassVar[bool] = False
    _EXISTS: ClassVar[bool] = False
    _QUERY_COUNTER: ClassVar[int] = 0
    _SCHEDULE_START: ClassVar[_date] = _date(*_MONTH, 1)
    _SCHEDULE_END: ClassVar[_date] = _date(_MONTH[0], _MONTH[1] + 2, 30)

    __slots__: tuple[str] = "_name", "_connection", "_cursor"

    @property
    def athens(self) -> models.Airport:
        """Returns Athens airport object."""
        return models.Airport.db(self._cursor.execute("select * from Airport where IATA = 'ATH'").fetchone())

    def __new__(cls, *args, **kwargs) -> Optional["Database"]:
        if cls._EXISTS:  # NOTE -------------------------------- prevents the creation of more than one Database object
            raise SyntaxError(f"Only one {cls.__name__} instance should be created")
        cls._EXISTS = True
        return super().__new__(cls)

    def __init__(self, path: str, name: Optional[str] = "AIRPORT", debug: Optional[bool] = False,
                 print_queries: Optional[bool] = False) -> NoReturn:
        """
        Pass debug=True to have debugging information displayed.
        Pass print_queries=True to have queries printed.
        """
        self._name: str = name
        self._connection: _sql.Connection = _sql.Connection(path)
        self._cursor: _sql.Cursor = self._connection.cursor()
        Database.Tables = Enum("Tables", [(_table.upper(), _table) for _table in self.tables])  # NOTE ----- DEPRECATED
        Database._DEBUG = debug
        Database._PRINT_QUERIES = print_queries
        if self._DEBUG:
            print(f"{self._name} DATABASE CONNECTED")
        return

    def __str__(self) -> str:
        raise NotImplementedError

    def __enter__(self) -> Self:
        raise NotImplementedError  # TODO

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError  # TODO

    def __del__(self) -> NoReturn:
        self._connection.commit()
        if self._DEBUG:
            match self.__class__._QUERY_COUNTER:
                case 0:
                    print("NO QUERIES EXECUTED", end="")
                case 1:
                    print("1 QUERY EXECUTED", end="")
                case _:
                    print(f"{self.__class__._QUERY_COUNTER} QUERIES EXECUTED", end="")
            print("\t\tCHANGES_COMMITTED\t\tDATABASE_CLOSED")
        self._connection.close()

    def __call__(self, __sql: str, __parameters: Any = ()) -> Union[_sql.Cursor, _sql.DatabaseError]:
        """
        Calls Database._execute().
        """
        return self._execute(__sql, __parameters)

    def _execute(self, __sql: str, __parameters: Any = ()) -> Union[_sql.Cursor, _sql.DatabaseError]:
        if "drop" in __sql:
            raise AttributeError("Table deletion is not permitted")
        try:
            self._cursor.execute(__sql, __parameters)
            if self._PRINT_QUERIES:
                print("QUERY EXECUTED", __sql, "WITH PARAMETERS", __parameters)
            self.__class__._QUERY_COUNTER += 1
            return self._cursor
        except _sql.DatabaseError as error:
            print("Failed to execute query. SQLite said:", error)
            return error

    def commit_save(self) -> NoReturn:
        self._connection.commit()
        self._connection.close()
        return

    @property
    def description(self) -> tuple[tuple]:
        return self._cursor.description

    @property
    def tables(self) -> list[str]:
        _data: list = self._cursor.execute("select name from sqlite_master where type='table' order by name").fetchall()
        _tables: list[str] = [_table[0] for _table in _data]  # NOTE ------- Cursor.fetchall() returns a list of tuples
        _tables.remove("sqlite_sequence")
        return _tables

    def table_info(self, table_name: str) -> Optional[list]:
        if table_name not in self.tables:
            raise AttributeError(f"No table named {table_name} exists, check your spelling.")
        return self._cursor.execute(f"pragma table_info({table_name});").fetchall()

    @property
    def _dates(self) -> GeneratorType:
        """
        Protected generator property used by generate_scheduled_flights, yields all the dates between the period
        specified at the class variables _SCHEDULE_START and _SCHEDULE_END.

        *Created on 22 Dec 2023.*
        """
        for _ in range(int((self._SCHEDULE_END - self._SCHEDULE_START + _timed(1)).days)):
            yield self._SCHEDULE_START + _timed(_)

    @staticmethod
    def random_code(airline_designator: str) -> str:
        return airline_designator + "-" + str(_rand(100, 900))

    @classmethod
    def random_hour(cls) -> _dt:
        return _dt(*cls._MONTH, 1, _rand(0, 23), 5 * _rand(0, 11))

    def random_schedule(self, airline_designator: str, other_id: int) -> models.Schedule:
        """
        Creates and returns a Schedule record using a given airline designator and an airport id, by choosing randomly
        if it will be a departure or an arrival. The record will have a departure or arrival datetime, which
        depends on whether the home airport of Athens is at from_airport or to_airport field. This datetime has always
        the same date, set on class variable _MONTH, time is randomly generated, the same for days. Current timestamp
        is stored at modified field, boolean active field is set to 1 (True) and occurrences are initialised to 0.

        *Created on 25 Dec 2023.*
        """
        _data, _airports = [self.random_code(airline_designator)], [self.athens.id, other_id]
        if self.athens.id == other_id:
            raise AttributeError(f"{other_id} CANNOT BE USED.")
        _shuf(_airports)
        _data.extend(_airports)
        if _data[1] == self.athens.id:
            _data.extend([str(self.random_hour()), None])  # fixme
        elif _data[2] == self.athens.id:
            _data.extend([None, str(self.random_hour())])
        _data.extend([_rand(0, 127), None, 1, 0])
        return models.Schedule.db(_data)

    def airline(self, designator: str) -> Optional[models.Airline]:
        """
        Searches for an Airline record with the passed designator and returns an Airline object with its data.

        *Created on 22 Dec 2023.*
        """
        if len(designator) != 2:
            raise AttributeError(f"Airline designators have exactly two characters, {designator} is not valid.")
        return models.Airline.db(self(f"select * from Airline where designator = ?", (designator,)).fetchone())

    def airport(self, iata: str) -> Optional[models.Airport]:
        """
        Searches for an Airport record with the passed IATA code and returns an Airport object with its data.

        *Created on 26 Dec 2023.*
        """
        if len(iata) != 3:
            raise AttributeError(f"IATA codes have exactly three characters, {iata} is not valid.")
        return models.Airport.db(self(f"select * from Airport where IATA = ?", (iata,)).fetchone())

    def generate_scheduled_flights(self, flight_code: str) -> str:
        """
        Creates Flight records for a single Schedule and stores them to database, only for the days
        specified in Schedule. One Schedule record and many flight records share the same flight code.
        Flight records have different date but always the same time, also specified in Schedule.

        *Created on 22 Dec 2023.*
        """
        _report: list[str] = list()
        _data: list = list()
        _counter: int = 0
        _s = models.Schedule.db(self._cursor.execute("select * from Schedule where code = ?",
                                                     (flight_code,)).fetchone())
        if self._DEBUG:
            print("SCHEDULED FLIGHT:", _s)
        _airline = self.airline(_s.code[:2]).tuple
        _airplanes = self._cursor.execute("select * from Airplane where airline = ?", (_airline[0],)).fetchall()
        _time = _s.departure if _s.is_departure else _s.arrival
        _time = _time.hour, _time.minute

        for date in self._dates:
            current_day: models.Day = models.Day.day(date)
            if current_day in _s.days:
                if self._DEBUG:
                    _counter += 1
                    print(date, current_day, current_day in _s.days)
                _data = [_s.code, _s.from_airport, _s.to_airport]
                if _s.is_departure:
                    _data.append(_dt(date.year, date.month, date.day, *_time))
                if _s.is_arrival:
                    _data.append(_dt(date.year, date.month, date.day, *_time))
                _data.extend([None, _rand(1, 40)])  # NOTE --------------------- state column will be filled separately
                _gate = models.Gate.random()
                _data.extend([_gate.number, _gate.terminal, _ch(_airplanes)[0]])

                if self._DEBUG:
                    print(_data)

                '''
                _query = (f"insert into Flight (code, from_airport, to_airport, departure, arrival, state,"
                         f" check_in, gate_n, gate_t, airplane) values ('{_data[0]}', '{_data[1]}',"
                         f"'{_data[2]}', '{_data[3]}', '{_data[4]}', '{_data[5]}', '{_data[6]}', '{_data[7]}',"
                         f"'{_data[8]}', '{_data[9]}')")
                '''  # TODO ----------------------------------------------------------------------------- to be deleted

                departure = ("insert into Flight (code, from_airport, to_airport, departure, state, "
                             "check_in, gate_n, gate_t, airplane) values (?, ?, ?, ?, ?, ?, ?, ?, ?)")
                arrival = ("insert into Flight (code, from_airport, to_airport, arrival, state, "
                           "check_in, gate_n, gate_t, airplane) values (?, ?, ?, ?, ?, ?, ?, ?, ?)")
                _query = departure if _s.is_departure else arrival if _s.is_arrival else None
                # _query = "insert into Flight (code, from_airport, to_airport, "  # noqa
                # _query += "departure, " if _s.is_departure else "arrival, "
                # _query += "state, check_in, gate_n, gate_t, airplane) values (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                self._cursor.execute(_query, _data)

            _report.append(str(_data))
        if self._DEBUG:
            print(f"{_counter} SCHEDULED FLIGHTS CREATED")
        return "\n".join(_elem for _elem in _report)

    def update_schedule_occurrences(self) -> NoReturn:
        """
        For each Schedule record, counts Flight occurrences and stores count at Schedule.occurrences.

        *Created on 25 Dec 2023.*
        """
        _counter: int = 0
        for schedule in self._cursor.execute("select code, active, occurrences from Schedule").fetchall():
            count = self._cursor.execute("select count() from Flight where code = ?", (schedule[0],)).fetchone()[0]
            if schedule[2] != count:
                _counter += abs(count - schedule[2]) if schedule[2] is not None else count
                self._cursor.execute("update Schedule set occurrences = ? where code = ?", (count, schedule[0]))
        if self._DEBUG:
            print(f"{_counter} NEW FLIGHT OCCURRENCES DETECTED")
        return

    def states_init(self, state: str = "Scheduled") -> NoReturn:
        """
        Checks each flight record and sets state to Scheduled if it's null.
        State argument defaults to **Scheduled**.

        *Created on 24 Dec 2023.*
        """
        _counter: int = 0
        state_value = self._cursor.execute("select id from State where name = ?", (state,)).fetchone()[0]
        flights: list = self._cursor.execute("select * from Flight").fetchall()
        for flight in flights:
            if flight[6] is None:
                _counter += 1
                self._cursor.execute("update Flight set state = ? where id = ?", (state_value, flight[0]))
        if self._DEBUG:
            print(f"{_counter} FLIGHT STATES SET TO {state}")
        return

    def update_schedule_timestamp(self, flight_code: str) -> NoReturn:
        """
        Searches for the Scheduled flight with the provided code and updates its modified column.

        *Created on 25 Dec 2023.*
        """
        self._cursor.execute("update Schedule set modified = CURRENT_TIMESTAMP where code = ?", (flight_code,))
        return

    def null_rectifier(self) -> NoReturn:
        """
        Replaces None values in records with <null>.

        *Created on 25 Dec 2023.*
        """
        _counter: int = 0
        # schedules: list = self.cursor.execute("select * from Schedule").fetchall()  # TODO
        ...
        if self._DEBUG:
            print(f"{_counter} NONE VALUES WERE REPLACED WITH NULL")
        return

    def table_tuples(self, table_name: str) -> list[tuple]:
        """
        Queries all columns of the specified table and returns a list of tuples.

        *Created on 25 Dec 2023.*
        """
        return self._cursor.execute("select * from ?", (table_name,)).fetchall()

    def random_airport_id(self) -> int:
        return _ch(self.table_tuples("Airport"))[0]

    def random_airline_designator(self) -> str:
        return _ch(self.table_tuples("Airline"))[2]

    def schedules(self) -> str:
        _out: list[str] = [models.Schedule.headers()]
        _query = ("select code, A1.IATA, A2.IATA, departure, arrival, days from Schedule "
                  "join main.Airport A1 on A1.id = Schedule.to_airport "
                  "join main.Airport A2 on A2.id = Schedule.from_airport")

        schedules = self._cursor.execute(_query).fetchall()
        for schedule in schedules:
            airline = \
                self._cursor.execute(f"select name from Airline where designator = '{schedule[0][:2]}'").fetchone()[0]
            row: str = schedule[0] + " " * 6 + airline + " " * (30 - len(airline)) + schedule[1] + "   " + schedule[2]
            row += " " * 6 + str(schedule[3]) + " " * (25 - len(str(schedule[3]))) + str(schedule[4])
            row += " " * (25 - len(str(schedule[4])))
            _out.append(row + " ".join([member.value[1] for member in models.Day.code_to_days(schedule[5])]))

        return "\n".join(element for element in _out)


database: Optional[Database] = None
try:
    database = Database(DATABASE, debug=True, print_queries=True)  # NOTE -------- toggle debug info and query printing
except _sql.OperationalError:
    print(f"Couldn't find database in {DATABASE}, please check path in assets.constants.py")

if __name__ == "__main__":
    ...
