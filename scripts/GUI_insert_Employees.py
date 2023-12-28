import sys
sys.path.append("./")

from assets import *
import PySimpleGUI as sg

"""
*Created on 27 Dec 2023.*
"""


layout = [
[sg.Text('Enter the following information for a new Employee register', font=("Courier", 18))], [sg.VPush()],
[sg.Text('SSN', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
[sg.Text('First Name', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
[sg.Text('Middle Name', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
[sg.Text('Last Name', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
[sg.Text('Telephone', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
[sg.Text('Email', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
[sg.Text('Street', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
[sg.Text('Number', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
[sg.Text('Town', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
[sg.Text('Postal Code', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
# [sg.Text('Birth Date', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
# [sg.Text('Department ID', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()], 
# [sg.Text('Sex', size=(13, 1), font=("Courier", 18)), sg.InputText(font=("Courier", 18))], [sg.VPush()],           ---TODO SEPERATELY
[sg.Submit(key="-SUBMIT-", font=("Courier", 18))], [sg.VPush()]
]

window = sg.Window("Data Entry Form", layout)

event, values = window.read()

# if values[0]==None or values[1]==None or values[3]==None:
#     raise AttributeError("SSN, FirstName, LastName can't be NULL")


""" Here the GUI handles the registers and inserts them into the database """         #RUNS BUT DOESNT INSERT INTO DB
if event == "-SUBMIT-":
    if values[0]==None or values[1]==None or values[3]==None:
        raise AttributeError("SSN, FirstName, LastName can't be NULL")

    database("insert into Employee(SSN, first_name, middle_name, last_name, telephone, email, street, number, town, postal_code) values (?,?,?,?,?,?,?,?,?,?)", 
             (int(values[0]), values[1], values[2], values[3], values[4], values[5],values[6], values[7], values[8], values[9]))
    del database
window.close()