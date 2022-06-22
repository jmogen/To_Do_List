import PySimpleGUI as sg
import sqlite3 as sql
import os.path
import random
import math

conn = sql.connect('items.db')

t = conn.cursor()
path_to_file = 'C:/Users/jmoge/Documents/GitHub/To-Do/items.db'

# if os.path.exists(path_to_file) == False:
# t.execute("""CREATE TABLE tasks(
#     title text,
#     description text,
#     due_date integer,
#     status text,
#     id integer
#     )""")

class Task:

    def __init__(self,title,description,due_date,status,id):
        self.title=title
        self.description=description
        self.due_date=due_date
        self.status=False
        if status == 'true':
            self.status == True
        else:
            self.status == False
        self.id = id


    def __repr__(self):
        return f"{self.id} Task:{self.title}, Due Date:{self.due_date}"

def startup():
    t.execute("SELECT * FROM tasks ORDER BY due_date")
    #t.execute("INSERT INTO tasks VALUES ('Unique Task', 'Unique Text For Filler', '3', 'true')")
    items = t.fetchall()

    conn.commit()
    #conn.close()
    tasks = []
    i = 0
    for x in items:
        tasks.append(Task(x[0], x[1], x[2], x[3], x[4]))
        i += 1
    return tasks
tasks = startup()

sg.theme('Black')  # please make your windows colorful
col_actions = [[sg.Text('Due Date'),sg.Text('Status') ]]
layout = [[sg.Text('UPCOMING'), sg.Button('Add'), sg.Button('Edit', key=lambda: edit_prediction(values['list'] ))],
    [sg.Text('TASKS'), sg.Column(col_actions, element_justification='right')],
    [sg.Listbox(tasks, size=(59,6), key='list')]
    ]

#layout += [[sg.Text(f'{i+1}. '), sg.Text(f'{items[i][0]}'), sg.Text(f'{items[i][2]}'),sg.Text(f'{items[i][3]}'), sg.Checkbox('', default=items[i][3]=='true'), sg.Button('Edit', key=lambda: edit_prediction(items[i][0], items[i][1], items[i][2]))] for i in range(0,len(items))]
            

window = sg.Window('TASKS', layout, resizable=True)


def add_prediction():

    col_layout = [[sg.Button('Save',key=lambda: add_entry(values[0], values[1], values[2] ))]]
    layout = [
        [sg.Text("Task:       "), sg.Input()],
        [sg.Text("Description:"), sg.Multiline(size=(None,5))],
        [sg.Text("Due Date:   "), sg.Input()],
        [sg.Column(col_layout, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Prediction", layout, use_default_focus=False, finalize=True, modal=True)
    #block_focus(window)
    event, values = window.read()
    if callable(event):
        event()
    window.close()
    return None

def delete_entry(title):
    return None

def unique_id():
    digits = [i for i in range(0, 10)]
    id = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        id += str(digits[index])
    return id

def add_entry(ta, de, dd):
    id = unique_id()
    search = t.execute("SELECT id FROM tasks WHERE id = ?", (id,))
    print (search)
    while search == id:
        id = unique_id()
        search = t.execute("SELECT id FROM tasks WHERE id id ?", (id,))
        
   
    t.execute("INSERT INTO tasks VALUES (?, ?, ?, 'true', ?)", (ta, de, dd, id))
    #items = t.fetchall() 
    conn.commit()
    print("success !:", ta, de, dd, id)
    return None

def edit_prediction(title):
    id = title[0]
    id = int(str(id)[0:6])
    print('TEST:', id)
    t.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    item = t.fetchone()
    conn.commit()
    col_layout = [[sg.Button('Save')]]
    print('ITEM:', item)
    layout = [
        [sg.Text("Task:       "), sg.Input(f'{item[0]}')],
        [sg.Text("Description:"), sg.Multiline(f'{item[1]}',size=(None,5))],
        [sg.Text("Due Date:   "), sg.Input(f'{item[2]}')],
        [sg.Column(col_layout, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Prediction", layout, use_default_focus=False, finalize=True, modal=True)
    #block_focus(window)
    event, values = window.read()
    window.close()
    return None



while True:  # Event Loop
    #update_window()
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if callable(event):
        event()
    elif event == 'Add':
        add_prediction()
    window['list'].update(startup()) #update listbox entries
  

window.close()