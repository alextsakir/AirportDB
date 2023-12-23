from assets import database

results: list[tuple] = database.table_info("Sex")

column_names = [result[1] for result in results]
print(column_names)

results = database.execute("select * from Sex").fetchall()
print(results)
