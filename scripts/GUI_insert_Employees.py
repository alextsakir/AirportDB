"""
*Created on 27 Dec 2023.*
"""

import sys

from assets.constants import DATABASE

sys.path.append("./")

import PySimpleGUI as sg  # noqa E402
import sqlite3

from assets import *  # noqa E402

SIZE = 13, 1
FONT = ("Courier", 18)


departments = [element[0] for element in database("select id from Department").fetchall()]
sexes = [element[0] for element in database("select id from Sex").fetchall()]  # TODO


layout = [[sg.Text("Enter the following information for a new Employee record:", font=FONT)], [sg.VPush()]]
print(Employee().columns[:10])
for column in Employee().columns[:10]:
    layout.extend([[sg.Text(column.capitalize(), size=SIZE, font=FONT), sg.InputText(font=FONT)], [sg.VPush()]])


# [sg.Text('Birth Date', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
# [sg.Text('Department ID', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
# [sg.Text('Sex', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()],TODO SEPARATELY
layout.extend([[sg.Submit(key="-SUBMIT-", font=FONT)], [sg.VPush()]])


window = sg.Window("Data Entry Form", layout)
print("LAYOUT:", len(layout))

event, values = window.read()
values = list(values.values())
window.close()
""" Here the GUI handles the registers and inserts them into the database """         # RUNS BUT DOESNT INSERT INTO DB
if event == "-SUBMIT-":
    if values[0] is None or values[1] is None or values[3] is None:
        raise AttributeError("SSN, FirstName, LastName can't be NULL")

    emp = Employee(*values)
    print(emp)
    print(emp.tuple)

    database("insert into Employee(SSN, first_name, middle_name, last_name, telephone, email, street, number,"
             "town, postal_code, birth_date, dept_id, sex) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
             emp.tuple)

    '''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("insert into Employee(SSN, first_name, middle_name, last_name, telephone, email, street, number,"
                   "town, postal_code, birth_date, dept_id, sex) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   emp.tuple)
    db.commit()
    db.close()'''

print("got here")
