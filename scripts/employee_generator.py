from assets import *


for index in range(5):
    # query: str = (f"insert into Employee(ssn, first_name, middle_name, last_name, telephone,
    # email, street, number, town, postal_code) values"
    # database.execute()
    ...

# print(Employee.random_tuple())
# print(Employee.random())

emp = Employee()
emp.name.first, emp.name.middle, emp.name.last = "Alexandros", "Marios", "Tsakiridis"
emp.contact = Employee.Contact("email here with spaces")

print(dir(emp))
