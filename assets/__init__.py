# __all__: tuple[str] = "constants", "database", ...

from sqlite3 import OperationalError
from typing import Optional

from assets.constants import DATABASE
from assets.database import Database
from assets.models import *

database: Optional[Database] = None
try:
    database = Database(DATABASE, debug=True)  # NOTE ----------------------------------------------- toggle debug info
except OperationalError:
    print(f"Couldn't find database in {DATABASE}, please check path in assets.constants.py")
