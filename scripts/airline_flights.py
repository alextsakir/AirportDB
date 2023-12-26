from assets import *


results = database("select * from Flight").fetchall()
for result in results:
    print(result)
