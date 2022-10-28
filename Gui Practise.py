from tkinter import *

root = Tk()
root.title("Dice Roller")

check_values = []
all_value = IntVar()
Check_all = Checkbutton(root, variable=all_value, command=lambda: all_check()).grid(row=0, column=2)


def all_check():
    if all_value.get():
        for i in range(0, check_length):
            check_values[i].set(1)
    else:
        for i in range(0, check_length):
            check_values[i].set(0)


for i in range(0, 10):                  #creating checkboxes
    value_inside = IntVar()
    value_inside.set(0)
    check = Checkbutton(root, variable=value_inside, command=lambda: check_values.append(value_inside.get()))
    check.grid(row=i+1, column=2)
    check_values.append(value_inside)
check_length = len(check_values)

drop_options = 'Sum', 'Max', 'Min'
drop_values = []

for i in range(0, 10):              #creating drop menu's
    value_inside = StringVar()
    value_inside.set(drop_options[0])
    dropmenu = OptionMenu(root, value_inside, *drop_options)
    dropmenu.grid(row=i+1, column=4)
    drop_values.append(value_inside)


def show():
    temp = []
    for i in range(0, 10):
        if check_values[i].get():
            temp.append(drop_values[i].get())
        else:
            temp.append('x')
    print(temp)
    print('-----------')


test_button = Button(root, text='test', command=lambda: show()).grid(row=0, column=4)

root.mainloop()