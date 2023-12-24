from os.path import dirname, abspath
from typing import Final

PROJECT: Final[str] = dirname(dirname(abspath(__file__)))
DATABASE: Final[str] = PROJECT + "/airport.sqlite"

CRUISE_SPEED: Final[int] = 400
LAND_SPEED: Final[int] = 320

EARTH_EQUATORIAL_RADIUS: Final[float] = 6378.1
EARTH_MEAN_RADIUS: Final[int] = 6371
EARTH_POLAR_RADIUS: Final[float] = 6356.8

MAX_DEGREE_LAT: Final[int] = 90
MAX_DEGREE_LONG: Final[int] = 180
MAX_MINUTE: Final[int] = 60
