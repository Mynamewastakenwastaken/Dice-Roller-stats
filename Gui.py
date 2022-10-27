from tkinter import *

root = Tk()
root.title("Dice Roller")


class Dice(object):
    dice_pool = []

    def __init__(self, faces, primary=0, crit_behavior=0, crit_value=1, state=0, amount=1, weight=0):
        self.faces = faces
        self.primary = primary
        self.crit_behavior = crit_behavior
        self.crit_value = crit_value
        self.state = state
        self.amount = amount
        self.weight = weight
        Dice.dice_pool.append(self)


die1 = Dice([])
die2 = Dice([])
die3 = Dice([])
die4 = Dice([])
# die5 = Dice([])
# die6 = Dice([])
# die7 = Dice([])
# die8 = Dice([])
# die9 = Dice([])
# die10 = Dice([])

Die_frame = LabelFrame(root, text="Dice", padx=8, pady=8)
Die_frame.pack(padx=10, pady=10)


def show():
    for val in check_values:
        print(val.get())  # Placing the inputs into the list Thruster
    return None


test_button = Button(Die_frame, text='test', command=lambda: show()).grid(row=0, column=4)
Select_Label = Label(Die_frame, text="define dice").grid(row=0, column=2)
#Active_Check0 = Checkbutton(Die_frame, text='all').grid(row=0, column=1)
check_values = []

for i in range(1, 11):
    # Variable to keep track of the option selected in OptionMenu
    value_inside = IntVar()
    # Set the default value of the variable
    value_inside.set(0)
    Check = Checkbutton(Die_frame, variable=value_inside, command=lambda x=value_inside[i]:check_values.append(i))
    Check.grid(row=i, column=1)
    check_values.append(value_inside)



Die_box1 = Entry(Die_frame, width=40).grid(row=1, column=2, padx=(16, 0))
Die_box2 = Entry(Die_frame, width=40).grid(row=2, column=2, padx=(16, 0))
Die_box3 = Entry(Die_frame, width=40).grid(row=3, column=2, padx=(16, 0))
Die_box4 = Entry(Die_frame, width=40).grid(row=4, column=2, padx=(16, 0))
Die_box5 = Entry(Die_frame, width=40).grid(row=5, column=2, padx=(16, 0))
Die_box6 = Entry(Die_frame, width=40).grid(row=6, column=2, padx=(16, 0))
Die_box7 = Entry(Die_frame, width=40).grid(row=7, column=2, padx=(16, 0))
Die_box8 = Entry(Die_frame, width=40).grid(row=8, column=2, padx=(16, 0))
Die_box9 = Entry(Die_frame, width=40).grid(row=9, column=2, padx=(16, 0))
Die_box10 = Entry(Die_frame, width=40).grid(row=10, column=2, padx=(16, 0))

Primary_Label = Label(Die_frame, text="primary").grid(row=0, column=3)
Primary_Check1 = Checkbutton(Die_frame).grid(row=1, column=3)
Primary_Check2 = Checkbutton(Die_frame).grid(row=2, column=3)
Primary_Check3 = Checkbutton(Die_frame).grid(row=3, column=3)
Primary_Check4 = Checkbutton(Die_frame).grid(row=4, column=3)
Primary_Check5 = Checkbutton(Die_frame).grid(row=5, column=3)
Primary_Check6 = Checkbutton(Die_frame).grid(row=6, column=3)
Primary_Check7 = Checkbutton(Die_frame).grid(row=7, column=3)
Primary_Check8 = Checkbutton(Die_frame).grid(row=8, column=3)
Primary_Check9 = Checkbutton(Die_frame).grid(row=9, column=3)
Primary_Check10 = Checkbutton(Die_frame).grid(row=10, column=3)

drop_options = 'Sum', 'Max', 'Min'
drop_values = []

for i in range(1, 11):
    # Variable to keep track of the option selected in OptionMenu
    value_inside = StringVar()
    # Set the default value of the variable
    value_inside.set(drop_options[0])
    question_menu = OptionMenu(Die_frame, value_inside, *drop_options)
    question_menu.grid(row=i, column=4)
    drop_values.append(value_inside)


def Dice_Correct(*args):  # function to return readable dice
    for x in args:
        if ',' in x:
            return x
        else:
            temp = list([val for val in x if val.isnumeric()])
            return "".join(temp)


def Dice_Construct(*args):
    for x in args:
        if ',' in x:
            temp = [float(e) for e in x.split(',')]
            return temp
        else:
            size = int(x)
            temp = []
            for i in range(0, size):
                temp.append(i + 1)
            return temp


root.mainloop()
