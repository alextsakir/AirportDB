"""
*Created on 27 Dec 2023.*
"""

import sys
sys.path.append("./") # DO NOT TOUCH OTHERWISE VSCODE USERS CRYY :( 

from assets.constants import DATABASE

import PySimpleGUI as sg  # noqa E402
import sqlite3

from assets import *  # noqa E402

SIZE = 13, 1
FONT = ("Courier", 18)


departments = [element[0] for element in database("select id from Department").fetchall()]
sexes = [element[0] for element in database("select id from Sex").fetchall()]  # TODO


sg.theme("Black")
layout = [[sg.Text("Enter the following information for a new Employee record:", font=FONT)], [sg.VPush()]]
print(Employee().columns[:9]) # 9 without birthdate (separate handling)
for column in Employee().columns[:9]:
    layout.extend([[sg.Text(column.capitalize(), size=SIZE, font=FONT), sg.InputText(font=FONT)], [sg.VPush()]])


"""
*Created on 29 Dec 2023.*   
"""
layout.extend([[sg.CalendarButton('Birth Date', font=FONT, format='%Y-%m-%d', close_when_date_chosen=True, target='Birth Date', location=(0,0), no_titlebar=True),
               [sg.Input(key='Birth Date', size=(13, 1), font=("Courier", 18))]]]) # TODO DATE HANDLING
layout.extend([[sg.Text('Department ID', size=SIZE, font=FONT), sg.Combo(departments, font=FONT)], [sg.VPush()]])
layout.extend([[sg.Text('Sex', size=SIZE, font=FONT), sg.Combo(sexes, font=FONT)], [sg.VPush()]])
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
