import sqlite3

connection = sqlite3.Connection("../airport.sqlite")
cursor = connection.cursor()

connection.execute("delete from Sex where id = 3;")

connection.commit()
connection.close()
