import tkinter as tk
import ttkbootstrap as ttk
import csv
from train import genesis_train, add_data
from test import recognize

# Global variables for data persistence and access
global table, row

def run(path, gen):
    if path.strip() == '':
        print('Path is empty')
        # text.set('Path is empty')
        return
    if gen:
        print('Training Genesis')
        genesis_train(True, path.strip())
    else:
        print('Adding Data')
        add_data(path.strip(), sID=True)
    # text.set('')
    update_treeview()

# Function to initialize the Treeview, populate it with initial data,
# and handle real-time attendance marking upon button click
def initialize_treeview():
    global table, row, tab_frame

    # Read initial data from CSV
    with open('attendance.csv', 'r') as file:
        reader = csv.reader(file)
        row = []
        for i in reader:
            row.append(i)

    # Get column names
    columns = tuple(i for i in row[0])
    # Creating Frame and Scrollbar
    tab_frame = ttk.Frame(master=app)
    tab_frame.pack(padx=30)
    tab_scroll = ttk.Scrollbar(master=tab_frame)
    tab_scroll.pack(side='right', fill='y')
    tab_scroll = ttk.Scrollbar(master=tab_frame, orient='horizontal')
    tab_scroll.pack(side='bottom', fill='x')
    # Create and configure Treeview
    table = ttk.Treeview(master=tab_frame, xscrollcommand=tab_scroll.set, yscrollcommand=tab_scroll.set, columns=columns, show='headings')
    table.pack()
    # Configure scrollbar
    tab_scroll.config(command=table.yview)
    tab_scroll.config(command=table.xview)

    # Set column headings
    for col in columns:
        table.heading(col, text=col.capitalize())

    # Skip the header row when inserting data
    row.pop(0)

    # Insert data into Treeview
    for index, data in enumerate(row):
        da = [x if data.index(x) != 1 else x[1:6] for x in data]  # Adjust for data structure if needed
        table.insert(parent='', index=tk.END, values=da)

    # Button click handler for real-time attendance marking
    def btn_test_realtime():
        print('Testing')
        recognize()
        data = True  # Replace with real-time data
        if data:
            print('Updating Treeview')
            update_treeview() 
            data = False

    # Configure button command
    btn_test.config(command=btn_test_realtime)


# Function to clear and re-read the CSV data, update the Treeview
# with new data (including new columns), and handle errors
def update_treeview():
    global table, row

    try:
        # Clear existing data
        table.delete(*table.get_children())

        # Read updated data from CSV
        with open('attendance.csv', 'r') as file:
            reader = csv.reader(file)
            row = []
            for i in reader:
                row.append(i)

        # Get updated column names
        columns = tuple(i for i in row[0])

        # Update Treeview columns and headings
        table.configure(columns=columns)
        for col in columns:
            table.heading(col, text=col.capitalize())

        # Skip the header row when inserting data
        row.pop(0)

        # Insert new data with the new column
        for index, data in enumerate(row):
            da = [x if data.index(x) != 1 else x[1:6] for x in data]  # Adjust for data structure if needed
            table.insert(parent='', index=tk.END, values=da)

    except FileNotFoundError:
        print("Error: File 'attendance.csv' not found.")
    except PermissionError:
        print("Error: Insufficient permissions to access 'attendance.csv'.")
    except Exception as e:
        print(f"Error during data reading: {e}")

# Create the Tkinter window and set up the main GUI
app = ttk.Window(themename='superhero')
app.title('Attendance System Dashboard')
app.geometry('1200x720')

# ... Create title, entry/button controls, and labels as in previous responses ...
title = ttk.Label(master=app, text='Attendance System Dashboard', font=('Arial', 30))
title.pack(pady=20)

frame = ttk.Frame(master=app)
entry_str = tk.StringVar()
entry_input = ttk.Entry(master=frame, textvariable=entry_str, font=('Arial', 20))
btn_gen = ttk.Button(master=frame, text='Train Genesis', command=lambda: run(entry_str.get(), gen=True))
btn_add = ttk.Button(master=frame, text='Add Student', command=lambda: run(entry_str.get(), gen=False))
btn_test = ttk.Button(master=frame, text='Test')
entry_input.pack()
btn_gen.pack(side="left", pady=20, padx=6, ipadx=5, ipady=5)
btn_add.pack(side="left", pady=20, padx=6, ipadx=5, ipady=5)
btn_test.pack(side="left", pady=20, padx=6, ipadx=8, ipady=5)
frame.pack(pady=20)
# Initialize the attendance Treeview
initialize_treeview()

app.mainloop()
