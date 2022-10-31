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
Die_frame.pack(padx=10, pady=10, side=LEFT)
Crit_frame = LabelFrame(root, text="Crits", padx=8, pady=8)
Crit_frame.pack(padx=0, pady=0, side=TOP)
Skill_frame = LabelFrame(root, text="Skills", padx=8, pady=8)
Skill_frame.pack(padx=10, pady=10, side=TOP)

Select_Label = Label(Die_frame, text="define dice").grid(row=0, column=2)
Crit_Label = Label(Crit_frame, text="Crit value -").grid(row=0, column=0)
Crit_Label = Label(Crit_frame, text="Behavior").grid(row=0, column=1)
check_values = []
all_value = IntVar()
Check_all = Checkbutton(Die_frame, variable=all_value, command=lambda: all_check()).grid(row=0, column=1)


def all_check():
    if all_value.get():
        for i in range(0, check_length):
            check_values[i].set(1)
    else:
        for i in range(0, check_length):
            check_values[i].set(0)
    enable_check_face()

def enable_check_face():
    for i in range(0, 10):
        if check_values[i].get() == 0:
            Entrybox_Widget.Face_objects[i].configure(state=DISABLED)
        else:
            Entrybox_Widget.Face_objects[i].configure(state=NORMAL)

def enable_check_skill():
    for i in range(0, 10):
        if skill_values[i].get() == 0:
            Entrybox_Widget.cost_objects[i].configure(state=DISABLED)
            Entrybox_Widget.damage_objects[i].configure(state=DISABLED)
        else:
            Entrybox_Widget.cost_objects[i].configure(state=NORMAL)
            Entrybox_Widget.damage_objects[i].configure(state=NORMAL)


for i in range(0, 10):                  #creating checkboxes
    value_inside = IntVar()
    value_inside.set(0)
    check = Checkbutton(Die_frame, variable=value_inside, command=lambda : enable_check_face())
    check.grid(row=i+1, column=1)
    check_values.append(value_inside)
check_length = len(check_values)


Skill_value = IntVar()
Skill_check = Checkbutton(Skill_frame, variable=Skill_value, command=lambda: all_skillcheck()).grid(row=0, column=0)
def all_skillcheck():               #all-checkbox function
    if Skill_value.get():
        for i in range(0, check_length):
            skill_values[i].set(1)
    else:
        for i in range(0, check_length):
            skill_values[i].set(0)
    enable_check_skill()


skill_values = []
#Skills: Cost, Damage, Repeatable, initiator/dependant, Skill point carryover between rolls
for i in range(0, 10):                  #creating checkboxes
    value_inside = IntVar()
    value_inside.set(0)
    check = Checkbutton(Skill_frame, variable=value_inside, command=lambda : enable_check_skill())
    check.grid(row=i+1, column=0)
    skill_values.append(value_inside)

def char_length(S):             #limit only numbers and set max character limit
    if len(S) == 0:
        return True
    elif len(S) < 4 and S.isdigit():
        return True
    else:
        return False



clcmd = (root.register(char_length), '%P')
Cost_Label = Label(Skill_frame, text="cost").grid(row=0, column=1)
Cost_values = []


class Entrybox_Widget():
    Face_objects = []
    cost_objects = []
    damage_objects = []
    Face_values = []
    Crit_value = []
    Cost_values = []
    Damage_values = []

    def add_face_entry(self):
        value_inside = StringVar()
        entry = Entry(Die_frame, width=40, textvariable=value_inside, state=DISABLED)
        entry.grid(row=i + 1, column=2, padx=(2, 4))
        entry.insert(0, '')
        Entrybox_Widget.Face_objects.append(entry)
        Entrybox_Widget.Face_values.append(value_inside)
    def add_cost_entry(self):
        value_inside = IntVar()
        entry = Entry(Skill_frame, width=4, validate="key", validatecommand=clcmd, textvariable=value_inside, state=DISABLED)
        entry.grid(row=i + 1, column=1)
        Entrybox_Widget.cost_objects.append(entry)
        Entrybox_Widget.Cost_values.append(value_inside)

    def add_damage_entry(self):
        value_inside = IntVar()
        entry = Entry(Skill_frame, width=4, validate="key", validatecommand=clcmd, textvariable=value_inside, state=DISABLED)
        entry.grid(row=i + 1, column=2, padx=5)
        Entrybox_Widget.damage_objects.append(entry)
        Entrybox_Widget.Damage_values.append(value_inside)
    def add_crit_entry(self):
        value_inside = IntVar()
        entry = Entry(Crit_frame, width=4, validate="key", validatecommand=clcmd, textvariable=value_inside)
        entry.grid(row=1, column=0)
        Entrybox_Widget.Crit_value.append(value_inside)



for i in range(0, 10):                  #creating entryboxes
    Entrybox_Widget.add_face_entry(i)
    Entrybox_Widget.add_cost_entry(i)
    Entrybox_Widget.add_damage_entry(i)
    if i < 1:
        Entrybox_Widget.add_crit_entry(i)



drop_options = 'Sum', 'Max', 'Min'
drop_values = []

for i in range(0, 10):      #creating drop menu's
    value_inside = StringVar()
    value_inside.set(drop_options[0])
    dropmenu = OptionMenu(Die_frame, value_inside, *drop_options)
    dropmenu.grid(row=i+1, column=3)
    drop_values.append(value_inside)

test_button = Button(Skill_frame, text='test', command=lambda: show3()).grid(row=0, column=4)

def show():                 #test function
    temp = []
    for i in range(0, 10):
        if check_values[i].get():
            temp.append(drop_values[i].get())
        else:
            temp.append('x')
    print(temp)
    print('-----------')

def show2():
    temp = []
    for i in range(0, 10):
        temp.append(Entrybox_Widget.Face_objects[i])
    print(temp)
    #for i in range(0, 10):
        #temp.append(Entrybox_Widget.Cost_values[i].get())
    #print(temp)
def show3():
    temp = []
    for i in range(0, 10):
        if check_values[i].get():
            temp.append(Entrybox_Widget.Face_values[i].get())
        else:
            temp.append('x')
    print(temp)
    print('-----------')

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

#for i in range(0, 10):
    #Entrybox_Widget.enable_check(Entrybox_Widget.Face_objects[i], check_values[i].get())

#for i in check_values:
    #Entrybox_Widget.enable_check(Entrybox_Widget.Face_objects[check_values.index(i)], i.get())

root.mainloop()
