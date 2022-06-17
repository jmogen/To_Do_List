from asyncio.windows_events import NULL
from enum import auto
from textwrap import fill
import PySimpleGUI as sg
import sqlite3 as sql


conn = sql.connect('items.db')

t = conn.cursor()

# tasks.execute("""CREATE TABLE tasks(
#     title text,
#     description text,
#     due_date integer,
#     status text
# )""")

t.execute("SELECT * FROM tasks")
items = t.fetchall() 


conn.commit()
#conn.close()


sg.theme('Black')  # please make your windows colorful

col_actions = [[sg.Text('Due Date'),sg.Text('Status') ]]
layout = [[sg.Text('UPCOMING'), sg.Button('Add'),sg.Button('Edit')],
[sg.Text('TASKS'), sg.Column(col_actions, element_justification='right')]]

layout += [[sg.Text(f'{i}. '), sg.Text(f'{items[i][0]}'), sg.Text(f'{items[i][2]}'), sg.Checkbox('', default=items[i][3]=='true')] for i in range(0,2)]
        

window = sg.Window('TASKS', layout, resizable=True)

def popup_prediction():

    col_layout = [[sg.Button('Save')]]
    layout = [
        [sg.Text("Task:       "), sg.Input()],
        [sg.Text("Description:"), sg.Multiline(size=(None,5))],
        [sg.Text("Due Date:   "), sg.Input()],
        [sg.Column(col_layout, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Prediction", layout, use_default_focus=False, finalize=True, modal=True)
    #block_focus(window)
    event, values = window.read()
    window.close()
    return None

while True:  # Event Loop
    event, values = window.read()
    #print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Add':
        popup_prediction()

window.close()