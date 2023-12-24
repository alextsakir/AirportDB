from assets import *


results = database.cursor.execute("select * from Flight").fetchall()
for result in results:
    print(result)
