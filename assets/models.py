"""
enumerations: DatetimeFormat, CoordinateType, Quarter, Day

Container, subclass of types.SimpleNamespace

abstract class DatabaseRecord

classes: Coordinates, Rectangle, Airline(DatabaseRecord), Employee(DatabaseRecord),
Airport(DatabaseRecord), Schedule(DatabaseRecord), Flight(DatabaseRecord), Gate

**NOTE: Python 3.11 required for typing.Self (PEP673), the pipe operator '|' (PEP604)
and the match-case statement (PEP634 ~ PEP636)**
"""

__all__: tuple[str] = ("DatetimeFormat", "CoordinateType", "Quarter", "Day", "Container",
                       "DatabaseRecord", "Coordinate", "Coordinates", "Rectangle", "Airline",
                       "Employee", "Airport", "Schedule", "Flight", "Gate")
__author__ = "A. Tsakiridis"
__version__ = "1.3"

from abc import abstractmethod, ABC
from datetime import datetime as _dt, date as _date, timezone as _t_zone, timedelta as _timed
from enum import Enum
from math import sin, cos, sqrt, asin, radians, degrees, atan
from random import choice as _ch, randint as _rand
from sys import version_info, stderr as standard_error
from types import SimpleNamespace
from typing import NoReturn, overload, Union, Iterator, Optional, Type, ClassVar, TypedDict
if version_info >= (3, 11):
    from typing import Self
else:
    print("Please use Python 3.11 or higher")

from assets.constants import *


class DatetimeFormat(Enum):
    """
    Members: **DATETIME, DATE, TIME**

    IMPORTANT: *The used date format is the American YYYY-MM-DD.*
    """
    DATETIME, DATE, TIME = "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%H:%M:%S"


class CoordinateType(Enum):
    """
    Members: **LATITUDINAL, LONGITUDINAL, UNKNOWN**
    """
    LATITUDINAL, LONGITUDINAL, UNKNOWN = "latitudinal", "longitudinal", "unknown"


class Quarter(Enum):
    """
    Members: **NORTH, SOUTH, EAST, WEST, UNKNOWN**

    Each member value is a tuple of three elements: **[0]** the first letter of its name, **[1]** full name
    in lowercase and **[2]** the corresponding CoordinateType member.
    """
    NORTH, SOUTH = ("N", "north", CoordinateType.LATITUDINAL), ("S", "south", CoordinateType.LATITUDINAL)
    EAST, WEST = ("E", "east", CoordinateType.LONGITUDINAL), ("W", "west", CoordinateType.LONGITUDINAL)
    UNKNOWN = ("U", "unknown", CoordinateType.UNKNOWN)

    def __iter__(self) -> Iterator[Self]:
        return iter([member for member in self.__class__])

    @classmethod
    def valid(cls) -> str:
        return str().join(member.value[0] + member.value[0].lower() for member in cls)

    @classmethod
    def get(cls, char: str) -> Self:
        if char not in cls.valid():
            raise AttributeError(f"Quarter.get() accepts only {cls.valid()} or 'north', 'south', 'east', 'west'")
        for member in cls:
            if char.upper() == member.value[0] or char.lower() == member.value[1]:
                return member
        return cls.UNKNOWN


VALID_Q: str = Quarter.valid()  # -------------------------------------------------------------------------- NsSsEeWwUu


class Day(Enum):
    """Members: **SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY**"""
    SUNDAY, MONDAY, TUESDAY, WEDNESDAY = (0, "SUN"), (1, "MON"), (2, "TUE"), (3, "WED")
    THURSDAY, FRIDAY, SATURDAY = (4, "THU"), (5, "FRI"), (6, "SAT")

    def __iter__(self):
        return iter([member for member in self.__class__])

    @classmethod
    def day(cls, number: int | _date) -> Optional[Self]:
        if isinstance(number, _date):
            number = number.weekday() + 1 if number.weekday() < 6 else 0

        if not 0 <= number <= 6:
            raise AttributeError("Day number must be from 0 to 6")
        for day in cls:
            if day.value[0] == number:
                return day
        return None

    @classmethod
    def today(cls):  # note------------------------------------------------ from official documentation
        print("today is %s" % cls(_date.today().weekday()).name)  # fixme weekday() returns 0 for Monday
        raise NotImplementedError

    @classmethod
    def every_day(cls) -> list[Self]:
        return [Day.SUNDAY, Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY, Day.SATURDAY]

    @classmethod
    def monday_to_friday(cls) -> list[Self]:
        return [Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY]

    @classmethod
    def saturday_sunday(cls) -> list[Self]:
        return [Day.SUNDAY, Day.SATURDAY]

    @classmethod
    def days_to_code(cls, days: list[Self]) -> int:
        _code = ["0" for _ in range(7)]
        for day in days:
            if day in days:
                _code[day.value[0]] = "1"
        return int(str().join(_code), 2)

    @classmethod
    def code_to_days(cls, number: int) -> list[Self]:
        _code, _out = bin(number)[2:].rjust(7, "0"), list()
        for index, digit in enumerate(_code):
            if digit == "1":
                _out.append(Day.day(index))
        return _out


class Container(SimpleNamespace):
    """
    https://docs.python.org/3/library/types.html#types.SimpleNamespace
    """


class DatabaseRecord(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs) -> NoReturn:
        """
        Abstract class to be inherited by classes depicting database records that contains:

        ``db(args: tuple)``: class method used to create child-class instances by arguments in a tuple,
        at the same order they are stored in the database.

        ``headers()``: abstract static method to be implemented. It should return a string with headers for the
        instance attributes, at the order of columns in the corresponding database table.

        Class children also should implement ``__str__()``.

        *Created on 6 Nov 2023.*
        """

    __slots__: tuple[str] = ()

    @classmethod
    def db(cls, args: tuple | list) -> Self:  # TODO --------------------------------- -> __class__ ? typing.Self? ABC?
        """
        Alternative factory method for creating objects from database records.
        """
        return cls(*args)

    @abstractmethod
    def __str__(self) -> str:
        ...

    @staticmethod
    @abstractmethod
    def headers() -> str:
        ...

    class Dict:  # ----------------------------------------------------------------------------------------- DEPRECATED
        ...

    @property
    def dict(self) -> dict:
        return {_slot: getattr(self, _slot) for _slot in self.__slots__}

# =====================================================================================================================


class Coordinate:

    C_TYPE_REQUIRED: ClassVar[bool] = True

    __slots__: tuple[str] = "value", "type", "label"

    @overload  # -------------------------------------------- Coordinate(-23.12) [insufficient] or Coordinate("23.12S")
    def __init__(self, value: Union[str, float, int] = None) -> NoReturn:
        ...

    @overload  # --------------------------------------------------------------------- Coordinate(23.12, Quarter.SOUTH)
    def __init__(self, value: Union[float, int] = None, quarter: Quarter = None) -> NoReturn:
        ...

    @overload  # ----------------------------------------------------- Coordinate(-23.12, "CoordinateType.LATITUDINAL")
    def __init__(self, value: Union[float, int] = None, coord_type: CoordinateType = None) -> NoReturn:
        ...

    @overload  # -------------- Coordinate(-23.12, "coord-label") [insufficient] or Coordinate("23.12S", "coord-label")
    def __init__(self, value: Union[str, float] = None, label: str = None) -> NoReturn:
        ...

    @overload  # ------------------------------------------------------ Coordinate(23.12, Quarter.NORTH, "coord-label")
    def __init__(self, value: Union[float, int] = None, quarter: Quarter = None, label: str = None) -> NoReturn:
        ...

    def __init__(self, value: Union[str, float, int] = None, quarter: Quarter = None,
                 coord_type: CoordinateType = None, label: str = None) -> NoReturn:
        """
        Possible Callees:

        ``Coordinate(float), Coordinate(str), Coordinate(float, Quarter), Coordinate(float, CoordinateType),
        Coordinate(float, string), Coordinate(string, string), Coordinate(float, Quarter, string)``

        Usage examples:

        ``Coordinate("12.25S")`` equivalent to ``Coordinate(-12.25, CoordinateType.LATITUDINAL)``

        ``Coordinate(25.2, Quarter.EAST)`` equivalent to ``Coordinate(-25.2. CoordinateType.LONGITUDINAL)``

        *Created on Oct 9 2023.*
        """

        self.value: float = 0.0
        self.type: CoordinateType = CoordinateType.UNKNOWN
        self.label: str = label if label else str()

        if quarter and isinstance(quarter, CoordinateType):  # FIXME: ---- any Enum member passed is treated as Quarter
            quarter, coord_type = None, quarter  # FIXME: ----------- is it because quarter is first in init arguments?

        if quarter and isinstance(quarter, Quarter):
            self.type = quarter.value[2]
        elif coord_type and isinstance(coord_type, CoordinateType):
            self.type = coord_type

        if value is None:
            raise AttributeError("Cannot create Coordinate object without specified value.")
        elif isinstance(value, float | int):
            self.value = float(value)
        elif isinstance(value, str):
            value = value.replace(" ", "")
            assert value[-1] in VALID_Q
            value = self.transform(value) if "o" in value else value
            self.value = float(value[:-1])
            if Quarter.get(value[-1]) == (Quarter.SOUTH or Quarter.WEST) and self.value > 0:
                self.value = -self.value
            self.type = Quarter.get(value[-1]).value[2]
        else:
            raise AttributeError(f"value of type {type(value)} is not accepted.")

        if self.type == CoordinateType.LATITUDINAL and abs(self) > MAX_DEGREE_LAT:
            raise AttributeError(f"Degrees must be under {MAX_DEGREE_LAT}.")
        elif self.type == CoordinateType.LONGITUDINAL and abs(self) > MAX_DEGREE_LONG:
            raise AttributeError(f"Degrees must be under {MAX_DEGREE_LONG}.")
        elif self.type == CoordinateType.UNKNOWN and self.C_TYPE_REQUIRED:
            raise AttributeError("Coordinate Type not specified.")
        return

    # =============================================================================================================

    @classmethod
    def degree(cls, value: str) -> Self:
        """
        Alternative factory method: ``Coordinate.degree("23o15'20''S")``
        """
        return cls(cls.transform(value))

    @classmethod
    def empty(cls):
        return cls(value=0, quarter=Quarter.UNKNOWN)

    # =============================================================================================================

    def __str__(self) -> str:
        return " ".join([self.label + ":" if len(self.label) else str(), str(abs(self))[:8], self.quarter.value[0]])

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return self.value

    def __abs__(self) -> float:
        return abs(self.value)

    def __lt__(self, other: Self) -> bool:
        return self.value < other.value

    def __gt__(self, other: Self) -> bool:
        return self.value > other.value

    def __le__(self, other: Self) -> bool:
        return self.value <= other.value

    def __ge__(self, other: Self) -> bool:
        return self.value >= other.value

    def __eq__(self, other: Self) -> bool:
        if self.value != other.value:
            return False
        return (self.type == other.type and self.value != 0) or self.value

    def __add__(self, other: Self) -> Union[Self, float]:
        if self.type == other.type:
            return self.__class__(value=self.value + other.value, coord_type=self.type)
        return sqrt(self.value ** 2 + other.value ** 2)

    def __sub__(self, other: Self) -> Optional[Self]:
        if self.type == other.type:
            return self.__class__(value=self.value - other.value, coord_type=self.type)
        return None

    def __truediv__(self, other: Self) -> float:
        return self.value / other.value

    @property
    def is_zero(self) -> bool:
        return not bool(self.value)

    # =============================================================================================================

    @property
    def quarter(self) -> Quarter:
        if self.type == CoordinateType.LATITUDINAL:
            return Quarter.NORTH if self.value >= 0 else Quarter.SOUTH
        elif self.type == CoordinateType.LONGITUDINAL:
            return Quarter.EAST if self.value >= 0 else Quarter.WEST
        return Quarter.UNKNOWN

    @staticmethod
    def transform(coord: str) -> float:
        """
        Accepted inputs: "30o20'", "30o20'10''", "30o20'10.2''"
        """
        degree = ["" for _ in range(3)]
        if coord.endswith("''"):
            coord = coord[:-2]
            degree[2] = [element for element in coord.split("'")][1]
            coord = coord[:-len(degree[2]) - 1]
        else:
            degree[2] = "0"

        if coord.endswith("'"):
            coord = coord[:-1]
        degree[0], degree[1] = (element for element in coord.split("o"))

        if (int(degree[0]) > MAX_DEGREE_LAT or
                max(float(degree[1]), float(degree[2])) > MAX_MINUTE):
            raise ValueError("Degree's minutes must be under 60.")
        return round(int(degree[0]) + int(degree[1]) / 60 + float(degree[2]) / 3600, 6)


class Coordinates:

    # =================================================================================================================

    #                       Length of the equator is                        40075 kilometers
    #                       Length of the parallel is 20° is                37656 kilometers
    #                       Length of the parallel is 40° is                30708 kilometers
    #                       Length of the parallel is 60° is                20088 kilometers
    #                       Length of the parallel is 80° is                7128 kilometers

    #                       1 degree of longitude on the equator is         111.32 kilometers
    #                       1 degree of longitude at 20° is                 104 kilometers
    #                       1 degree of longitude at 40° is                 85  kilometers
    #                       1 degree of longitude at 60° is                 55  kilometers
    #                       1 degree of longitude at 80° is                 19  kilometers

    #                       1 degree of longitude at φ deg lat. is          111.32 * cos(φ) km.

    __slots__: tuple[str] = "lat", "long", "label"

    @overload
    def __init__(self, x: str = None, y: str = None):
        ...

    @overload
    def __init__(self, x: float = None, y: float = None):
        ...

    @overload
    def __init__(self, x: Coordinate = None, y: Coordinate = None):
        ...

    @overload
    def __init__(self, x: str = None, y: str = None, label: str = None):
        ...

    @overload
    def __init__(self, x: float = None, y: float = None, label: str = None):
        ...

    @overload
    def __init__(self, x: Coordinate = None, y: Coordinate = None, label: str = None):
        ...

    def __init__(self, x: Union[float, str, Coordinate] = None, y: Union[float, str, Coordinate] = None,
                 label: str = None) -> NoReturn:
        """
        Stores two attributes of type Coordinates.Coordinate. Coordinates object is subscriptable and iterable.

        Possible callees:

        ``Coordinates(float, float), Coordinates(float, float, str), Coordinates(str, str), Coordinates(str, str, str),
        Coordinates(Coordinate, Coordinate), Coordinates(Coordinate, Coordinate, str)``

        Usage examples:

        ``Coordinates(-12.5, -25.2)``

        ``Coordinates("12.25S", "25.2E")``

        ``Coordinates(coordinate_object_lat, coordinate_object_long)``

        Optional argument: label (string).

        *Created on 9 Oct 2023.*
        """
        self.lat: Optional[Coordinate] = None
        self.long: Optional[Coordinate] = None
        self.label: str = label if label else str()

        if isinstance(x, Coordinate) and isinstance(y, Coordinate):
            x.type, y.type = CoordinateType.LATITUDINAL, CoordinateType.LONGITUDINAL
            self.lat, self.long = x, y
        elif isinstance(x, Union[float, int]) and isinstance(y, Union[float, int]):
            self.lat = Coordinate(value=x, coord_type=CoordinateType.LATITUDINAL)
            self.long = Coordinate(value=y, coord_type=CoordinateType.LONGITUDINAL)
        elif isinstance(x, str) and isinstance(y, str):
            self.lat, self.long = Coordinate(value=x), Coordinate(value=y)
        else:
            raise TypeError("x, y parameters should be Coordinate, float or string")
        return

    def __iter__(self) -> Iterator:
        return iter([self.lat, self.long])

    def __str__(self) -> str:
        return ", ".join(str(coord) for coord in self)

    def __setitem__(self, key: Union[str, int], value: Union[float, str, Coordinate]) -> NoReturn:
        if not isinstance(value, Coordinate):
            value = Coordinate(value)
        if isinstance(key, int) or isinstance(key, str):
            match key:
                case 0 | "lat" | "latitude":
                    self.lat = value
                case 1 | "long" | "longitude":
                    self.long = value
                case _:
                    raise KeyError("Keys must be 0 or 1, 'lat' or 'long', 'latitude' or 'longitude'.")
        return

    def __getitem__(self, item: Union[str, int]) -> Optional[Coordinate]:  # subscriptable
        if isinstance(item, int):
            return (self.lat, self.long)[item]
        elif isinstance(item, str):
            if item == "lat" or item == "latitude":
                return self.lat
            elif item == "long" or item == "longitude":
                return self.long
        return None

    # =================================================================================================================

    @property
    def on_equator(self) -> bool:
        """
        Instance property indicating Coordinates object is on the Equator.
        """
        return self.long.is_zero

    @property
    def on_prime_meridian(self) -> bool:
        """
        Instance property indicating Coordinates object is on the Prime Meridian.
        """
        return self.lat.is_zero

    @classmethod
    def omikron(cls) -> Self:
        """
        Returns an object located on both the Equator and the Prime Meridian, in the Gulf of Guinea.
        """
        return cls(0, 0, "O")

    def relative_location(self, other: Self) -> tuple[list[list[Optional[Self]]], int, int, int, int]:
        """
        DEPRECATED, use Airport.draw() instead.

        *Created on 11 Nov 2023.*
        """
        _pts: list = [self, other, self.omikron()]
        _lat = sorted(_pts, key=lambda obj: obj.lat, reverse=True)
        _long = sorted(_pts, key=lambda obj: obj.long)
        _min_lat, _min_long = int(_lat[-1].lat), int(_long[0].long)
        _max_lat, _max_long = int(_lat[0].lat), int(_long[-1].long)
        # print(_min_lat, _min_long, _max_lat, _max_long)
        _positions: list[list] = [[None for _ in range(3)] for _ in range(3)]
        for _point in _pts:
            _positions[_lat.index(_point)][_long.index(_point)] = _point
        return _positions, _min_lat, _min_long, _max_lat, _max_long

    # =================================================================================================================

    @staticmethod
    def average(_alpha: Union[Coordinate, float], _beta: Union[Coordinate, float]) -> float:
        return (float(_alpha) + float(_beta)) / 2

    @staticmethod
    def earth_radius(latitude: float) -> float:
        """
        Returns floating point earth radius at the specified latitude, a value between 6356.8 and 6378.1 kilometers.

        *Created on 6 Nov 2023.*
        """
        if abs(latitude) > 90:
            raise AttributeError("absolute latitude must be under 90")
        return EARTH_EQUATORIAL_RADIUS - 21.3 * latitude / 90

    @staticmethod  # to be class method
    def latitude_distance_kilometers(degree: float) -> float:
        return 111.14 * degree

    @staticmethod  # to be class method
    def longitude_distance_kilometers(degree: float, latitude: float) -> float:
        return 111.14 * degree / cos(radians(latitude))

    def distance_degrees(self, other: Self) -> float:
        """
        This method takes two pairs of coordinates as input and calculates their floating point distance
        as they were be on a Cartesian plane.

        *Created on 6 Nov 2023.*
        """
        return sqrt(float(self.lat - other.lat) ** 2 + float(self.long - other.long) ** 2)

    def zep_distance_kilometers(self, other: Self) -> float:
        """*Created on 6 Nov 2023.*"""
        _latitude = self.latitude_distance_kilometers(abs(self.lat - other.lat))
        _longitude = self.longitude_distance_kilometers(abs(self.long - other.long), self.average(self.lat, other.lat))
        print("avg_latitude:", self.average(self.lat, other.lat), cos(radians(self.average(self.lat, other.lat))))
        print("zep_distance:", abs(self.lat - other.lat), _latitude, abs(self.long - other.long), _longitude)
        return sqrt(_latitude ** 2 + _longitude ** 2)

    def haversine_arc(self, other: Self) -> float:
        """
        Returns arc between two Coordinates objects on globe, using the Haversine formula.

        *Created on 7 Nov 2023.*
        """
        d_latitude, d_longitude = radians(other.lat - self.lat), radians(other.long - self.long)
        _temp = sin(d_latitude / 2) ** 2 + cos(radians(self.lat)) * cos(radians(other.lat)) * sin(d_longitude / 2) ** 2
        _theta = 2 * asin(sqrt(_temp))
        return degrees(_theta)

    def haversine_distance(self, other: Self) -> float:
        """
        Returns distance between two Coordinates objects in kilometers, using earth radius.

        *Created on 7 Nov 2023.*
        """
        return radians(self.haversine_arc(other)) * self.earth_radius(self.average(self.lat, other.lat))

    def direction(self, other: Self) -> int:
        """
        Returns direction of axis between two Coordinates objects.

        *Created on 11 Nov 2023.*
        """
        return round(degrees(atan(abs(other.lat - self.lat) / abs(other.long - self.long))))

    @classmethod
    def duration(cls, arc: float) -> str:
        """
        Takes an arc as input and after division with default aircraft velocity, returns a string depicting flight
        duration in hours and minutes, hours are omitted if necessary.

        *Created on 8 Nov 2023.*
        """
        hours, minutes = divmod(int(arc * 3600 / LAND_SPEED), 60)
        if hours > 0:
            return f"{hours} hours, {minutes} minutes"
        return f"{minutes} minutes"


class Rectangle:

    _C_FLOAT: Type = Union[Coordinate, float]
    _POINT: Type = Union[Coordinates, tuple[float, float]]

    __slots__: tuple[str] = "lat", "long", "label"

    @overload
    def __init__(self, point_alpha: _POINT = None, point_beta: _POINT = None):
        ...

    @overload
    def __init__(self, point_alpha: _POINT = None, point_beta: _POINT = None,
                 label: str = None):
        ...

    @overload
    def __init__(self, min_lat: _C_FLOAT = None, max_lat: _C_FLOAT = None,
                 min_long: _C_FLOAT = None, max_long: _C_FLOAT = None):
        ...

    @overload
    def __init__(self, min_lat: _C_FLOAT = None, max_lat: _C_FLOAT = None,
                 min_long: _C_FLOAT = None, max_long: _C_FLOAT = None,
                 label: str = None):
        ...

    def __init__(self, min_lat: _C_FLOAT = None, max_lat: _C_FLOAT = None,
                 min_long: _C_FLOAT = None, max_long: _C_FLOAT = None,
                 point_alpha: _POINT = None, point_beta: _POINT = None,
                 label: str = None) -> NoReturn:
        if not min_lat and not min_long and not max_lat and not max_long and point_alpha and point_beta:
            if isinstance(point_alpha, Coordinates) and isinstance(point_beta, Coordinates):
                min_lat, max_lat = point_alpha.lat, point_alpha.lat
                min_long, max_long = point_alpha.long, point_alpha.long
            elif isinstance(point_alpha, tuple) and isinstance(point_beta, tuple):
                min_lat, max_lat = point_alpha[0], point_beta[0]
                min_long, max_long = point_alpha[1], point_beta[1]

        min_lat, max_lat, min_long, max_long = [float(coord) for coord in (min_lat, max_lat, min_long, max_long)]

        if min_lat > max_lat:
            min_lat, max_lat = max_lat, min_lat
        if min_long > max_long:
            min_long, max_long = max_long, min_long

        self.lat: tuple[float, float] = min_lat, max_lat
        self.long: tuple[float, float] = min_long, max_long
        self.label: Optional[str] = label
        return

    def __str__(self) -> str:
        return f"Rectangle of {len(self)}deg^2 area: "

    def __iter__(self) -> Iterator:
        return iter([self.lat, self.long])

    def __len__(self) -> int:
        return int((self.lat[1] - self.lat[0]) * (self.long[1] - self.long[0]))

    @overload
    def __contains__(self, item: _POINT = None) -> bool:
        ...

    @overload
    def __contains__(self, lat: _C_FLOAT = None, long: _C_FLOAT = None) -> bool:
        ...

    def __contains__(self, item: _POINT = None, lat: _C_FLOAT = None, long: _C_FLOAT = None) -> bool:
        _data: Optional[tuple[float, float]] = None
        if lat and long and not item:
            if isinstance(lat, Coordinate) and isinstance(long, Coordinate):
                lat, long = float(lat), float(long)
            _data = lat, long
        elif not lat and not long and item and isinstance(item, Coordinates):
            _data = float(item.lat), float(item.long)
        if self.lat[0] <= _data[0] <= self.lat[1] and self.long[0] <= _data[1] <= self.long[1]:
            return True
        return False


class Airline(DatabaseRecord):

    __slots__: tuple[str] = "id", "name", "designator"

    def __init__(self, airline_id: int, name: str, designator: str) -> NoReturn:
        super().__init__()
        self.id: int = airline_id
        self.name: str = name
        self.designator: str = designator
        pass

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def headers() -> str:
        pass


class Employee(DatabaseRecord):

    class Composite(ABC):

        __slots__: tuple[str] = ()

        @abstractmethod
        def __str__(self) -> str:
            ...

        @property
        def is_full(self) -> bool:
            for _slot in self.__slots__:
                print(_slot)
            return True

    class Name(Composite):

        def __init__(self, first: Optional[str] = None, middle: Optional[str] = None,
                     last: Optional[str] = None) -> NoReturn:
            # super().__init__()  # TODO ---------------------------------------------------------------- to be removed
            self.first: str = first
            self.middle: str = middle
            self.last: str = last
            return

        def __str__(self) -> str:
            out: str = self.first
            out += " " * (14 - len(out)) + self.middle
            return out + " " * (28 - len(out)) + self.last

    class Contact(Composite):

        def __init__(self, telephone: Optional[str] = None, email: Optional[str] = None) -> NoReturn:
            # super().__init__()  # TODO ---------------------------------------------------------------- to be removed
            self.telephone: str = telephone
            self.email: str = email
            return

        def __str__(self) -> str:
            return self.telephone + " " * 5 + self.email

    class Address(Composite):

        def __init__(self, street: Optional[str] = None, number: Optional[int] = None,
                     town: Optional[str] = None, postal_code: Optional[int] = None) -> NoReturn:
            # super().__init__()  # TODO ---------------------------------------------------------------- to be removed
            self.street: str = street
            self.number: int = number
            self.town: str = town
            self.postal_code: int = postal_code
            return

        def __str__(self) -> str:
            out: str = self.street + " " * (25 - len(self.street)) + str(self.number)
            return out + " " * (30 - len(out)) + self.town + " " * (20 - len(self.town)) + str(self.postal_code)

    # =================================================================================================================

    DOMAINS: tuple[str] = "aia.gr", "yahoo.com", "gmail.com", "hotmail.com", "outlook.com", "proton.me", "aol.com"
    YEAR_RANGE: tuple[int] = 1955, 1995
    FIRST_NAMES: list[str] = []; LAST_NAMES: list[str] = []; STREETS: list[str] = []; COMMON_WORDS: list[str] = []
    TOWNS: list[str] = []
    _TEXT_PATH: str = "E:/text/"
    _LOADED_NAMES: bool = False

    @classmethod
    def _load_files(cls) -> int:
        """*Created on 9 Nov 2023.*"""
        if cls._LOADED_NAMES:
            return 0

        try:
            _F: list[str] = open(cls._TEXT_PATH + "english_names.txt").readlines()  # --------------------- FIRST_NAMES
            _L: list[str] = open(cls._TEXT_PATH + "english_last_names_usa.txt").readlines()  # ------------- LAST_NAMES
            _S: list[str] = open(cls._TEXT_PATH + "english_streets_patras.txt").readlines()  # ---------------- STREETS
            _C: list[str] = open(cls._TEXT_PATH + "english_words_common.txt").readlines()  # ------------- COMMON_WORDS
            _T: list[str] = open(cls._TEXT_PATH + "greek_towns.txt").readlines()  # ----------------------------- TOWNS

            _P = (_F, cls.FIRST_NAMES), (_L, cls.LAST_NAMES), (_S, cls.STREETS), (_C, cls.COMMON_WORDS), (_T, cls.TOWNS)
            for pair in _P:
                for _name in pair[0]:
                    pair[1].append(_name.replace("\n", str()))
            cls._LOADED_NAMES = True
        except FileNotFoundError or OSError:
            print(f"THERE IS NO {cls._TEXT_PATH} IN YOUR COMPUTER.", file=standard_error)
            return -1
        return len(cls.FIRST_NAMES + cls.LAST_NAMES + cls.STREETS + cls.COMMON_WORDS + cls.TOWNS)

    # =================================================================================================================

    @classmethod
    def random(cls) -> Optional[Self]:
        """Alternative factory method, creates and returns random Employee object."""
        random_tuple: tuple = cls.random_tuple()
        return cls(*random_tuple) if random_tuple is not None else None

    def __init__(self, ssn: Optional[int] = None,
                 first: Optional[str] = None, middle: Optional[str] = None, last: Optional[str] = None,
                 telephone: Optional[str] = None, email: Optional[str] = None,
                 street: Optional[str] = None, number: Optional[int] = None,
                 town: Optional[str] = None, postal_code: Optional[int] = None,
                 birth_date: Union[str, _date, None] = None, dept_id: Optional[int] = None,
                 sex: Optional[int] = None) -> NoReturn:
        """*Created on 7 Nov 2023.*"""
        self.ssn: int = ssn
        self.name: Employee.Name = Employee.Name(first, middle, last)
        self.contact: Employee.Contact = Employee.Contact(telephone, email)
        self.address: Employee.Address = Employee.Address(street, number, town, postal_code)
        # _format: str = DatetimeFormat.DATE.value if len(birth_date) == 10 else DatetimeFormat.DATETIME.value  #  NOTE
        _format: str = DatetimeFormat.DATE.value
        self.birth_date: Optional[_date] = None
        if birth_date:
            self.birth_date = birth_date if isinstance(birth_date, _date) else _dt.strptime(birth_date, _format)
        self.dept_id: int = dept_id
        self.sex: int = sex

        if len(str(ssn)) != 9:
            raise AttributeError(f"SSN must have exactly 9 digits, {ssn} has {len(str(ssn))}, fix it and try again.")
        return

    def __str__(self) -> str:
        out: str = str(self.ssn) + " " * 5 + str(self.name) + " " * (40 - len(str(self.name)))
        out += str(self.contact) + " " * (58 - len(str(self.contact))) + str(self.address)
        out += " " * (175 - len(out)) + str(self.birth_date) + " " * 6 + str(self.dept_id)
        return out + " " * (200 - len(out)) + str(self.sex)

    @staticmethod
    def headers() -> str:
        out: str = "=" * 2 + " SSN " + "=" * 6 + " FIRST NAME " + "=" * 2 + " MIDDLE NAME " + "="
        out += " LAST NAME " + "=" * 5 + " TELEPHONE " + "=" * 11 + " EMAIL ADDRESS " + "=" * 22
        out += " STREET " + "=" * 12 + " NO. " + "====" + " TOWN " + "=" * 7 + " POSTAL CODE " + "==="
        return out + " BIRTH DATE " + "====" + " DEPT " + "=" * 3 + " SEX"

    def __dir__(self):
        _dir: list = dir(self.__class__)  # TODO
        for attr in _dir:
            if attr in dir(object):
                _dir.remove(attr)
        return _dir

    def tuple(self) -> tuple:
        print(self.__dir__())  # TODO
        return tuple()

    @staticmethod
    def _random_ssn() -> int:
        return int(str().join([str(_rand(1, 9)) for _ in range(9)]))

    @classmethod
    def generate_email(cls, first: str, last: str, birth_date: _date) -> str:
        """*Created on 9 Nov 2023.*"""
        _choice, _user, first, last = _rand(1, 9), str(), first.lower(), last.lower()
        _user = first[:-_rand(1, len(first) - 2)] + _ch(["_", "-", ".", ""]) + last[:-_rand(1, len(last) - 2)]
        match _choice:
            case 1 | 2: _user += str().join([str(_rand(0, 9)) for _ in range(_rand(1, 3))])
            case 3 | 4 | 5: _user += str(birth_date.year)
            case 6 | 7: _user = _ch(cls.COMMON_WORDS) + _ch(["_", "-", ".", ""]) + _user
        return _user + "@" + _ch(cls.DOMAINS) if len(_user) > 10 else cls.generate_email(first, last, birth_date)

    @classmethod
    def random_tuple(cls) -> Optional[tuple]:
        """*Created on 9 Nov 2023.*"""
        if cls._load_files() == -1:
            print(f"COULD NOT GENERATE RANDOM TUPLE", file=standard_error)
            return
        _data = [cls._random_ssn(), _ch(cls.FIRST_NAMES), _ch(cls.FIRST_NAMES), _ch(cls.LAST_NAMES)]
        _telephone: str = "+30 694 " + str().join([str(_rand(0, 9)) for _ in range(3)]) + " "
        _telephone += str().join([str(_rand(0, 9)) for _ in range(4)])
        _birth = _date(_rand(*cls.YEAR_RANGE), _rand(1, 12), _rand(1, 28))
        _data.extend([_telephone, cls.generate_email(_data[1], _data[3], _birth), _ch(cls.STREETS), _rand(1, 75)])
        _data.extend([_ch(cls.TOWNS), _rand(10_000, 19_900), str(_birth), 0, 2])
        return tuple(_data)


class Airport(DatabaseRecord):

    class Runway:

        __slots__: tuple[str] = "id", "name", "length", "airport_id"

        def __init__(self, runway_id: int, name: str, length: int, airport_id: int) -> NoReturn:
            self.id: int = runway_id
            self.name: str = name
            self.length: int = length
            self.airport_id: int = airport_id
            return

        @property
        def direction(self) -> int:
            """
            Returns runway direction in deca-degrees, as declared in its name.
            """
            return min(self._direction_tuple())

        def _direction_tuple(self) -> tuple[int, int]:
            _temp = self.name
            for character in _temp:
                if character.isalpha():
                    _temp = _temp.replace(character, "")
            _temp = _temp.split("/")
            _temp = int(_temp[0]), int(_temp[1])
            if max(_temp) != min(_temp) + 18:
                raise ValueError
            return _temp

    # =================================================================================================================

    _CHECK_COORDINATES: ClassVar[bool] = True
    _CHECK_IATA: ClassVar[bool] = True
    _CHECK_TIMEZONE: ClassVar[bool] = True

    __slots__: tuple[str] = "id", "iata", "country", "timezone", "name", "description", "location", "runways"

    class Dict(TypedDict):  # NOTE ----------------------------------------------------------------------------- UNUSED
        """
        KEYS: flight_id, iata, country, timezone, name, description, location, runways
        """
        id: int
        iata: str
        timezone: _t_zone
        name: str
        description: str
        location: Coordinates
        runways: list["Airport.Runway"]

    def __init__(self, airport_id: int, iata: str, country: str, timezone: int,
                 name: str, lat: float = None, long: float = None) -> NoReturn:
        self.id: int = airport_id
        self.iata: str = iata
        self.country: str = country  # --------------------------------------------------------------- TODO enumeration
        self.timezone: _t_zone = _t_zone(_timed(hours=timezone))
        self.name: str = name
        self.description: str = str()
        self.location: Optional[Coordinates] = Coordinates(lat, long, iata)
        self.runways: list[Airport.Runway] = list()
        if self.__class__._CHECK_COORDINATES and (lat > MAX_DEGREE_LAT or long > MAX_DEGREE_LONG):
            raise AttributeError("Values (0, 0) are invalid for Airport latitude and longitude.")
        if self.__class__._CHECK_IATA and len(self.iata) != 3:
            raise AttributeError(f"Invalid IATA code ({iata}), there must be exactly three (3) characters.")
        if self.__class__._CHECK_TIMEZONE and abs(timezone) > 12:
            raise AttributeError(f"Timezone value {timezone} is invalid, should be between -12 and +12.")
        return

    @classmethod
    def _omikron(cls) -> Self:
        return cls(-1, "-O-", "", 0, "", 0, 0)

    def __str__(self) -> str:
        _out: str = self.name + " " * (55 - len(self.name)) + str(self.location.lat) + "   " + str(self.location.long)
        _out += " " * (85 - len(_out)) + self.iata + " " * 7 + self.country
        return _out + " " * (110 - len(_out)) + str(self.timezone) + " " * 6 + self.description

    @staticmethod
    def headers() -> str:
        _out: str = "=" * 20 + " AIRPORT " + "=" * 25 + " LATITUDE " + "====" + " LONGITUDE " + "===="
        return _out + " IATA " + "====" + " COUNTRY " + "=" * 6 + " TIMEZONE " + "=" * 12 + " LOCAL TIME " + "=" * 6

    def measurements(self, other: Self) -> str:
        _out: str = " " * 8 + f"{round(self.distance_degrees(other), 6)}"
        _out += " " * (24 - len(_out)) + f"{round(self.distance_kilometers(other), 4)}"
        return _out + " " * (40 - len(_out)) + f"{self.duration(other)}"

    @staticmethod
    def measurements_headers() -> str:
        _out: str = "=" * 8 + " DEGREES " + "=" * 7 + " KILOMETERS " + "=" * 8 + " DURATION " + "=" * 8
        return _out

    @property
    def local_time(self) -> str:
        return _dt.now(self.timezone).strftime('%a %d %b %Y, %H:%M')

    def draw(self, other: Self) -> str:
        """
        Returns a small map with the relative position of the given Airport objects.
        The intersection of **Equator** and **Prime Meridian** will be included as a reference point.

        *Created on 11 Nov 2023.*
        """
        _points: list = [self, other, self._omikron()]  # -------------------------------- three airports will be drawn
        _lat: list[Self] = sorted(_points, key=lambda obj: obj.location.lat, reverse=True)  # ------ sorted by latitude
        _long: list[Self] = sorted(_points, key=lambda obj: obj.location.long)  # ----------------- sorted by longitude
        assert len(_points) == len(_lat) == len(_long)  # ---------------------------------------------- logic checking

        _min_long, _max_long = int(_long[0].location.long), int(_long[-1].location.long)  # -- will be used for padding

        _size, _char = 100, "#"  # -------------------------------------------------- set line size and frame character
        _pad: int = (_size + _min_long - _max_long) // 2 - 2  # -------------------------------------- set line padding
        _empty: str = 2 * _char + " " * (_size - 4) + 2 * _char  # ----------------------------------------- empty line
        _table: list[str] = [_char * _size, _empty, _empty]  # ------------------ upper frame and first two empty lines

        for g in range(3):  # -------------------------------------------------------- draw three airport points on map
            if g > 0:  # --------------------------------------------- space between first and second, second and third
                _space: int = int(_lat[g - 1].location.lat - _lat[g].location.lat) // 8 + 1
                _table.extend([_empty for _ in range(_space)])  # ------------------ empty lines between airport points
            _line: str = 2 * _char + " " * (_pad + int(_lat[g].location.long) - 2) + f"[{_lat[g].iata}]"
            _table.append(_line + " " * (_size - 2 - len(_line)) + 2 * _char)  # ------------------------ airport point

        _table.extend([_empty, _empty, _char * _size])  # ------------------------ two more empty lines and lower frame

        _index: int = 0  # ----------------------------------------------- find Omikron indices on map: O(_index, _pos)
        for _index, element in enumerate(_table):
            if "[-O-]" in element:  # --------------------------------------------------------------------- find _index
                break
        _pos: int = _table[_index].find("O")  # ------------------------------------------------------------- find _pos

        _temp: str = _table[_index][:_pos - 8] + "-" * 8 + "O" + "-" * 8 + _table[_index][_pos + 9:]
        _table[_index] = _temp  # ------------------------------------- edit Omikron line, create Equator axis on map

        for g in (-2, -1, 1, 2):  # ------------- edit lines above and below Omikron, create Prime Meridian axis on map
            _temp: str = _table[_index + g][:_pos] + "|" + _table[_index + g][_pos + 1:]
            _table[_index + g] = _temp

        return "\n".join(_elem for _elem in _table)  # ------- make string from list of strings, separated by new lines

    def map(self, other: Self) -> str:
        """
        Returns a string with presentation of two Airports, their local time and the map created by Airport.draw()
        """
        _out: str = self.headers() + "\n" + str(self) + self.local_time + "\n" + str(other) + other.local_time
        return _out + "\n\n\n" + self.draw(other)

    def distance_degrees(self, other: Self) -> float:
        return self.location.haversine_arc(other.location)

    def distance_kilometers(self, other: Self) -> float:
        return self.location.haversine_distance(other.location)

    def duration(self, other: Self) -> str:
        return self.location.duration(self.distance_degrees(other))

    def direction(self) -> int:
        raise NotImplementedError

    @staticmethod
    def smart_duration(arc: float) -> str:
        raise NotImplementedError


class Schedule(DatabaseRecord):

    __slots__: tuple[str] = ("code", "from_airport", "to_airport", "departure", "arrival", "_days",
                             "modified", "active", "occurrences")

    def __init__(self, code: Optional[str] = None,
                 from_airport: Optional[int] = None, to_airport: Optional[int] = None,
                 departure: Optional[Union[_dt, str]] = None,
                 arrival: Optional[Union[_dt, str]] = None, days: Optional[int] = None,
                 modified: Optional[Union[_dt, str]] = None, active: Optional[int] = None,
                 occurrences: Optional[int] = None) -> None:
        self.code: str = code
        self.from_airport: int = from_airport
        self.to_airport: int = to_airport
        _f: str = DatetimeFormat.DATETIME.value
        self.departure: Optional[_dt] = None
        self.arrival: Optional[_dt] = None
        if departure is not None:
            self.departure = departure if isinstance(departure, _dt) else _dt.strptime(departure, _f)
        if arrival is not None:
            self.arrival = arrival if isinstance(arrival, _dt) else _dt.strptime(arrival, _f)
        self._days: int = days
        self.modified: Optional[_dt] = modified if isinstance(modified, _dt) else _dt.strptime(modified, _f)
        self.active: bool = bool(active)
        self.occurrences: int = occurrences
        return

    def __str__(self) -> str:
        _out: str = self.code + " " * (12 - len(self.code)) + str(self.from_airport) + " " * 5 + str(self.to_airport)
        _out += " " * (30 - len(_out)) + str(self.departure) + " " * 5 + str(self.arrival)
        return _out + " " * (66 - len(_out)) + " " * 10 + str(self.days_repr)

    @staticmethod
    def headers() -> str:
        raise NotImplementedError

    @property
    def days(self) -> list[Day]:
        return Day.code_to_days(self._days)

    @property
    def days_repr(self) -> list[str]:
        return [day.value[1] for day in self.days]

    @property
    def is_departure(self) -> bool:
        return self.departure is not None and self.arrival is None

    @property
    def is_arrival(self) -> bool:
        return self.departure is None and self.arrival is not None


class Flight(DatabaseRecord):

    __slots__: tuple[str] = ("flight_id", "code", "from_airport", "to_airport",
                             "departure", "arrival", "state", "check_in",
                             "gate_number", "gate_terminal", "airplane")

    def __init__(self, flight_id: int, code: str, from_airport: int, to_airport: int,
                 departure: _dt, arrival: _dt, state: int,
                 check_in: int, gate_n: int, gate_t: str, airplane: int) -> NoReturn:
        self.flight_id: int = flight_id
        self.code: str = code
        self.from_airport: int = from_airport
        self.to_airport: int = to_airport
        self.departure: _dt = departure
        self.arrival: _dt = arrival
        self.state: int = state
        self.check_in: int = check_in
        self.gate_number: int = gate_n
        self.gate_terminal: str = gate_t
        self.airplane: int = airplane  # TODO foreign
        return

    def __str__(self) -> str:
        raise NotImplementedError

    @staticmethod
    def headers() -> str:
        raise NotImplementedError


class Gate:

    _DATA = (("A", 1, 23), ("B", 1, 31), ("C", 15, 40))  # NOTE ------------------------- according to official website

    def __init__(self, number: int, terminal: str) -> NoReturn:
        self.number: int = number
        self.terminal: str = terminal
        return

    def __str__(self) -> str:
        return self.terminal + str(self.number)

    @classmethod
    def random(cls) -> Self:
        _choice = _rand(0, len(cls._DATA) - 1)
        return cls(_rand(*cls._DATA[_choice][1:]), cls._DATA[_choice][0])


if __name__ == "__main__":
    gamma = Coordinate(0, CoordinateType.LATITUDINAL)
    alpha = Coordinate(0, CoordinateType.LATITUDINAL)
    print(gamma.quarter)
