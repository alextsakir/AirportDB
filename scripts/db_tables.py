from assets import *

results = database.cursor.execute("select * from Airline")
for result in results:
    print(result)
