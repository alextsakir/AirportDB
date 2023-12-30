"""
*Created on 27 Dec 2023.*
"""

from sys import path
path.append("./")  # DO NOT TOUCH OTHERWISE VSCODE USERS CRY :( ---------------------------------------------- PATHETIC

import PySimpleGUI as gui  # noqa E402

from assets import *  # noqa E402

SIZE, FONT = (13, 1), ("Courier", 18)

departments = [element[0] for element in database("select id from Department").fetchall()]
sexes = [element[0] for element in database("select id from Sex").fetchall()]  # TODO


gui.theme("Black")
layout = [[gui.Text("Enter the following information for a new Employee record:", font=FONT)], [gui.VPush()]]
print(Employee().columns[:10])  # 9 without birthdate (separate handling)
for column in Employee().columns[:10]:
    layout.extend([[gui.Text(column.capitalize(), size=SIZE, font=FONT), gui.InputText(font=FONT)], [gui.VPush()]])

layout.extend([[gui.CalendarButton('Birth Date', font=FONT, format='%Y-%m-%d', close_when_date_chosen=True,
                                   target='Birth Date', location=(550, 700)),
               [gui.Input(key='Birth Date', size=SIZE, font=FONT)]]])  # TODO DATE HANDLING
layout.extend([[gui.Text('Department ID', size=SIZE, font=FONT), gui.Combo(departments, font=FONT)], [gui.VPush()]])
layout.extend([[gui.Text('Sex', size=SIZE, font=FONT), gui.Combo(sexes, font=FONT)], [gui.VPush()]])
layout.extend([[gui.Submit(key="-SUBMIT-", font=FONT)], [gui.VPush()]])


window = gui.Window("Data Entry Form", location=(450, 100), size=(1020, 800), element_justification="center",
                    titlebar_background_color="#4A4A4A", layout=layout)
# print("LAYOUT:", len(layout))

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
