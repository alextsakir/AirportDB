__all__: tuple[str] = "database", "athens"

import datetime as _datetime
import random
from enum import Enum
import sqlite3 as _sqlite
from random import choice
from typing import NoReturn, Self, Union, Optional, ClassVar

from assets.constants import DATABASE
from assets.models import Airport, Day, Flight, Gate, Schedule


class Database:
    class Tables(Enum):  # NOTE UNUSED
        pass  # ---- --------- members filled in __init__, could not use Tables.__setattr__ because Enum's immutability

    _DEBUG: ClassVar[bool] = False
    _EXISTS: ClassVar[bool] = False
    _SCHEDULE_START: ClassVar[_datetime.date] = _datetime.date(2024, 2, 1)
    _SCHEDULE_END: ClassVar[_datetime.date] = _datetime.date(2024, 4, 30)

    def __new__(cls, *args, **kwargs) -> Optional["Database"]:
        if cls._EXISTS:  # NOTE ------------------------------- prevents the creation of more than one Database objects
            raise SyntaxError("Only one Database instance should be created")
        cls._EXISTS = True
        return super().__new__(cls)

    def __init__(self, path: str, name: Optional[str] = "AIRPORT", debug: Optional[bool] = False) -> NoReturn:
        """
        Pass debug=True to have debugging information printed
        """
        self.name: str = name
        self.connection: _sqlite.Connection = _sqlite.Connection(path)
        self.cursor: _sqlite.Cursor = self.connection.cursor()
        Database.Tables = Enum("Tables", [(_table.upper(), _table) for _table in self.tables])  # NOTE
        Database._DEBUG = debug
        if self._DEBUG:
            print(f"DATABASE {self.name} CONNECTED")
        return

    def __str__(self) -> str:
        raise NotImplementedError

    def __enter__(self) -> Self:
        raise NotImplementedError  # return self.__init__()  TODO

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError  # del self TODO

    def __del__(self) -> NoReturn:
        self.connection.commit()
        if self._DEBUG:
            print("CHANGES_COMMITTED\t\tDB_CLOSED")
        self.connection.close()

    def __call__(self, *args):
        return self.execute(args)  # TODO

    def execute(self, *args) -> Union[_sqlite.Cursor, _sqlite.Error]:  # TODO ----- __sql: str, __parameters: Any = ...
        if "drop" in args[0]:
            raise AttributeError("You are not allowed to delete tables")  # TODO ----------------------------- check it
        try:
            return self.cursor.execute(*args)  # FIXME -------------------------------- raises _sqlite.ProgrammingError
        except _sqlite.Error as error:
            print("Failed to execute the above query", error)
            return error

    @property
    def tables(self) -> list[str]:
        _data: list = self.cursor.execute("select name from sqlite_master where type='table' order by name").fetchall()
        _tables: list[str] = [_table[0] for _table in _data]  # NOTE ------- Cursor.fetchall() returns a list of tuples
        _tables.remove("sqlite_sequence")
        return _tables

    def table_info(self, table_name: str) -> Optional[list]:
        if table_name not in self.tables:
            raise AttributeError(f"No table named {table_name} exists, check your spelling.")
        return self.cursor.execute(f"pragma table_info({table_name});").fetchall()

    @property
    def _dates(self) -> iter:
        for _date in range(int((self._SCHEDULE_END - self._SCHEDULE_START + _datetime.timedelta(1)).days)):
            yield self._SCHEDULE_START + _datetime.timedelta(_date)

    def airline(self, designator: str) -> tuple:
        if len(designator) != 2:
            raise AttributeError(f"Airline designators have exactly two characters, {designator} is not valid.")
        return self.cursor.execute(f"select * from Airline where designator like '%{designator}%'").fetchone()

    def generate_scheduled_flights(self, flight_code: str) -> str:
        _report: list[str] = list()
        _s = Schedule.db(self.cursor.execute("select * from Schedule where code = ?", (flight_code,)).fetchone())
        if self._DEBUG:
            print("SCHEDULED FLIGHT:", _s)
        _airline = self.airline(_s.code[:2])
        _airplanes = self.cursor.execute(f"select * from Airplane where airline = {_airline[0]}").fetchall()


        for date in self._dates:
            current_day: Day = Day.day(date)  # NOTE ------- create Flight only for the days specified in Schedule.days
            if current_day in _s.days:
                if self._DEBUG:
                    print(date, current_day, current_day in _s.days)
                data: list = [_s.code, _s.from_airport, _s.to_airport]
                if _s.departure is not None:
                    time = _s.departure.hour, _s.departure.minute
                    data.append(_datetime.datetime(date.year, date.month, date.day, *time))
                else:
                    data.append(None)
                if _s.arrival is not None:
                    time = _s.arrival.hour, _s.arrival.minute
                    data.append(_datetime.datetime(date.year, date.month, date.day, *time))
                else:
                    data.append(None)
                data.extend([None, random.randint(1, 40)])  # NOTE ------------------ state column will be filled later
                _gate = Gate.random()
                data.extend([_gate.number, _gate.terminal, choice(_airplanes)[0]])

                if self._DEBUG:
                    print(data)

                query = (f"insert into Flight (code, from_airport, to_airport, departure, arrival, state,"
                         f" check_in, gate_n, gate_t, airplane) values ('{data[0]}', '{data[1]}',"
                         f"'{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}', '{data[7]}',"
                         f"'{data[8]}', '{data[9]}')")  # FIXME an einai dynaton tetoio syntax

                # self.cursor.execute(query)

            # _report.append(str(Flight))

        return "\n".join(_elem for _elem in _report)

    def table_tuples(self, table_name: str) -> list[tuple]:
        return self.cursor.execute(f"select * from {table_name}").fetchall()

    def random_airport_id(self) -> int:
        return choice(self.table_tuples("Airport"))[0]

    def random_airline_designator(self) -> str:
        return choice(self.table_tuples("Airline"))[2]

    def schedules(self) -> str:
        _out: list[str] = ["headers..."]
        _query = ("select code, A2.IATA, A.IATA, departure, arrival, days from Schedule "
                  "join main.Airport A on A.id = Schedule.end "
                  "join main.Airport A2 on A2.id = Schedule.start")

        schedules = self.cursor.execute(_query).fetchall()
        for schedule in schedules:
            airline = \
                self.cursor.execute(f"select name from Airline where designator = '{schedule[0][:2]}'").fetchone()[0]
            row: str = schedule[0] + " " * 6 + airline + " " * (30 - len(airline)) + schedule[1] + "   " + schedule[2]
            row += " " * 6 + str(schedule[3]) + " " * (25 - len(str(schedule[3]))) + str(schedule[4])
            row += " " * (25 - len(str(schedule[4])))
            _out.append(row + " ".join([member.value[1] for member in Day.code_to_days(schedule[5])]))

        return "\n".join(element for element in _out)


database: Optional[Database] = None

try:
    database = Database(DATABASE, debug=True)  # NOTE ----------------------------------------------- toggle debug info
except _sqlite.OperationalError:
    print(f"Couldn't find database in {DATABASE}, please check path in assets.constants.py")

athens: Airport = Airport.db(database.execute("select * from Airport where IATA = 'ATH'").fetchone())
"""Home airport"""

if __name__ == "__main__":
    print(database.schedules())
