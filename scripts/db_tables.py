import sys
sys.path.append("./")

from assets import *

# database.cursor.execute("update Schedule set arrival = ? where code = ?", (datetime(2024, 1, 1, 8, 15, 0), 'A3-240',))

results = database("select * from Airline").fetchall()
print(results)
