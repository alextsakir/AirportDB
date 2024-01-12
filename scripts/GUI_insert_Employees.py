"""
Opens a form to fill in personal information for a new Employee record.

*Created on 27 Dec 2023.*
"""

from sys import path
path.append("./")  # DO NOT TOUCH OTHERWISE VSCODE USERS CRY :( ----------------------------------------- IT'S PATHETIC

from ctypes import windll  # noqa E402
import sqlite3  # noqa E402

import PySimpleGUI as gui  # noqa E402

from assets import *  # noqa E402
from assets.constants import DATABASE  # noqa E402

SCREEN = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)
PAD_X, PAD_Y = SCREEN[0] // 5, SCREEN[1] // 10  # NOTE parameterize window dimensions to match to any screen resolution
WINDOW_SIZE, WINDOW_LOCATION = (SCREEN[0] - 2 * PAD_X, SCREEN[1] - 2 * PAD_Y), (PAD_X, PAD_Y)  # NOTE - align to center
SIZE, FONT = (13, 1), ("Courier", 18)

#  NOTE ------------------------------------------- user friendlier, obtain the Department and Sex names instead of ids
departments = [element[0] for element in database("select name from Department").fetchall()]
sexes = [element[0] for element in database("select name from Sex").fetchall()]

gui.theme("Black")

layout = [[gui.Text("Enter the following information for a new Employee record:", font=FONT)], [gui.VPush()]]
print(Employee().columns[:10])  # 9 without birthdate (separate handling) NOTE ----------------- you forgot postal_code
for column in Employee().columns[:10]:
    layout.extend([[gui.Text(column.capitalize(), size=SIZE, font=FONT), gui.InputText(font=FONT)], [gui.VPush()]])

layout.extend([[gui.CalendarButton('Birth Date', font=FONT, format='%Y-%m-%d', default_date_m_d_y=(1, 1, 1980),
                                   target='Birth Date', location=(PAD_X * 1.2, PAD_Y * 7)),
               [gui.Input(key='Birth Date', size=SIZE, font=FONT)]]])  # TODO DATE HANDLING

layout.extend([[gui.Text('Department ID', size=SIZE, font=FONT), gui.Combo(departments, font=FONT)], [gui.VPush()]])
'''
layout.extend([[gui.Text('Department ID', size=SIZE, font=FONT),
                gui.Slider(font=FONT, orientation="horizontal", range=(departments[0], departments[-1]),
                           default_value=departments[0])],
               [gui.VPush()]])'''  # NOTE replace Department Combo component with an alternative nice horizontal slider

layout.extend([[gui.Text('Sex', size=SIZE, font=FONT), gui.Combo(sexes, font=FONT)], [gui.VPush()]])
layout.extend([[gui.Submit(key="-SUBMIT-", font=FONT)], [gui.VPush()]])

''' :param right_click_menu:            A list of lists of Menu items to show when this element is right clicked.
    :type right_click_menu:             List[List[ List[str] | str ]] '''  # -------------------- copied from docstring
CONTEXT_MENU: list[list[list[str] | str]] = [["first"], ["second"], ["third"]]  # FIXME
window = gui.Window("Data Entry Form", location=WINDOW_LOCATION, size=WINDOW_SIZE, element_justification="center",
                    right_click_menu=CONTEXT_MENU, layout=layout, finalize=True)
window.bind('<F1>', 'Birth Date')

# print("LAYOUT:", len(layout))

event, values = window.read()

try:
    if "Birth Date" in values and "Birth Date0" in values:  # NOTE --------------------------------------- bad solution
        values.pop("Birth Date0")
except KeyError:
    pass

try:  # NOTE ---------------------------------------- obtain the corresponding ids for Department and Sex chosen values
    if values[10] is not None:
        values[10] = database("select id from Department where name = ?", (values[10],)).fetchone()[0]
    if values[11] is not None:
        values[11] = database("select id from Sex where name = ?", (values[11],)).fetchone()[0]
except TypeError:
    print("there was a problem at Department, Sex parsing, never mind")

values = list(values.values())
window.close()

# Here the GUI handles the registers and inserts them into the database TODO ----------------- RUNS BUT DOES NOT INSERT
if event == "-SUBMIT-":
    if (not values[0] or not values[1] or not values[3]) and False:  # ---------------- remove 'and False' to enable it
        raise AttributeError("SSN, FirstName, LastName can't be NULL")

    emp = Employee(*values)
    print(values, "\n", emp, "\n", emp.tuple)

    '''
    database("insert into Employee(SSN, first_name, middle_name, last_name, telephone, email, street, number,"
             "town, postal_code, birth_date, dept_id, sex) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
             emp.tuple)'''  # NOTE ------------------------------------------------ surprisingly, it's not working here

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("insert into Employee(SSN, first_name, middle_name, last_name, telephone, email, street, number,"
                   "town, postal_code, birth_date, dept_id, sex) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   emp.tuple)
    db.commit()
    db.close()

print("got here")
