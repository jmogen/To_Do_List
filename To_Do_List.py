from genericpath import exists
import PySimpleGUI as sg
import sqlite3 as sql
import os.path
import random
import math

conn = sql.connect('items.db')

t = conn.cursor()
path_to_file = 'C:/Users/jmoge/Documents/GitHub/To-Do/items.db'

# create sql table if file does not already exist
# if os.path.exists(path_to_file) == False:
# t.execute("""CREATE TABLE tasks(
#     title text,
#     description text,
#     due_date integer,
#     status text,
#     id integer
#     )""")

# format sql table data for display
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

# startup function to format data for display
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
layout = [[sg.Text('UPCOMING'), sg.Button('Add'), sg.Button('Edit'), sg.Button('Delete')],
    [sg.Text('TASKS'), sg.Column(col_actions, element_justification='right')],
    [sg.Listbox(tasks, size=(59,6), key='list')]
    ]           

window = sg.Window('TASKS', layout, resizable=True)

# popup logic for adding another entry
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

# delete entry (placeholder for now)
def delete_entry(title):
    id = title[0]
    id = int(str(id)[0:6])
    t.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    return None

# generate unique task id
def unique_id():
    digits = [i for i in range(0, 10)]
    id = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        id += str(digits[index])
    return id

# add entry 
def add_entry(ta, de, dd):
    id = unique_id()
    search = t.execute("SELECT id FROM tasks WHERE id = ?", (id,))
    print (search)
    while search == id:
        id = unique_id()
        search = t.execute("SELECT id FROM tasks WHERE id = ?", (id,))
        
   
    t.execute("INSERT INTO tasks VALUES (?, ?, ?, 'true', ?)", (ta, de, dd, id))
    #items = t.fetchall() 
    conn.commit()
    print("success !:", ta, de, dd, id)
    return None

# update entry data
def update_entry(ta, de, dd, id):
    t.execute("UPDATE tasks SET title = ?, description = ?, due_date = ? WHERE id = ?", (ta, de, dd, id,))
    conn.commit()

# popup logic for an edit of a task
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
    if event == 'Save':
        update_entry(values[0], values[1], values[2], id)
    window.close()
    return None


# Event Loop
while True:  
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Edit' and values['list']:
        edit_prediction(values['list'])
    if event == 'Delete' and values['list']:
        delete_entry(values['list'])    
    # if callable(event):
    #     event()
    elif event == 'Add':
        add_prediction()
    window['list'].update(startup()) #update listbox entries while window is active
  

window.close()