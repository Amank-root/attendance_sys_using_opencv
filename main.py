import tkinter as tk
import ttkbootstrap as ttk
import csv, time
from train import genesis_train, add_data
from test import recognize

# Variables
row = []

with open('attendance.csv', 'r') as file:
	reader = csv.reader(file)
	for i in reader:
		row.append(i)

def run(path, gen):
	if path.strip() == '':
		print('Path is empty')
		text.set('Path is empty')
		return
	if gen:
		print('Training Genesis')
		genesis_train(True, path.strip())
	else:
		print('Adding Data')
		add_data(path.strip(), sID=True)
	text.set('')

	


def btn_test_realtime():
	print('Testing')
	data = recognize()
	if data:
		print('Attendance Taken')
		text.set('Attendance Taken')
	text.set('')


app = ttk.Window(themename='superhero')
app.title('Attendance System Dashboard')
app.geometry('1200x720')

# Title
title = ttk.Label(master=app, text='Attendance System Dashboard', font=('Arial', 30))
title.pack(pady=20)

# creating a frame
frame = ttk.Frame(master=app)
entry_str = tk.StringVar()
entry_input = ttk.Entry(master=frame, textvariable=entry_str, font=('Arial', 20))
btn_gen = ttk.Button(master=frame, text='Train Genesis', command=lambda: run(entry_str.get(), gen=True))
btn_add = ttk.Button(master=frame, text='Add Student', command=lambda: run(entry_str.get(), gen=False))
btn_test = ttk.Button(master=frame, text='Test', command=btn_test_realtime)
entry_input.pack()
btn_gen.pack(side="left", pady=20, padx=6, ipadx=5, ipady=5)
btn_add.pack(side="left", pady=20, padx=6, ipadx=5, ipady=5)
btn_test.pack(side="left", pady=20, padx=6, ipadx=8, ipady=5)
frame.pack(pady=20)

# text
text = tk.StringVar()
label = ttk.Label(master=app, textvariable=text, font=('Arial', 8))
label.pack(pady=5)


# Todays Attendance
todays_attendance = ttk.Label(master=app, text='Attendance', font=('Arial', 30))
todays_attendance.pack(pady=10)

colunm = tuple(i for i in row[0])
table = ttk.Treeview(master=app, columns=colunm, show='headings')

for i in colunm:
	table.heading(i, text=i.capitalize())
row.pop(0)


for index, data in enumerate(row):
	# print(index, data)
	da = [x if data.index(x) != 1 else x[1:6] for x in data]
	# print(da)
	table.insert(parent='', index=tk.END, values=da)
table.pack(fill='both', padx=30)


app.mainloop()

