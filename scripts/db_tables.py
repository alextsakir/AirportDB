from assets import *

query = "select * from Airport"

results = database.cursor.execute(query).fetchall()

for result in results:
    print(result)
