from assets import *


for index in range(95):
    query: str = (f"insert into Employee(ssn, first_name, middle_name, last_name, telephone, email, street, number,"
                  f"town, postal_code, birth_date, dept_id, sex) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    data = database.random_employee()
    print(data)
    # database(query, data)
