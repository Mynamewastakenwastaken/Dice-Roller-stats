from tkinter import *
from tkinter.ttk import Progressbar
import time
import os
import pyautogui as pg
import pickle
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = Tk()
root.title("Dice Roller")

"""GUI----START----GUI----START----GUI----START----GUI----START----GUI"""
def openLoadWindow():         #seperate window for results
    load_window = Toplevel(root)
    load_window.title("Results")
    Label(load_window, text="Rolling...").pack()
    load_window.grab_set()
    p = Progressbar(load_window, orient=HORIZONTAL, length=200, mode="determinate", takefocus=True, maximum=config.max_roll)
    p.pack()
    cancel = Button(load_window, text='cancel', command=lambda: load_window.destroy())
    cancel.pack()
    progress = 0
    for i in range(0, config.max_roll):
        Dice.function_check = 0
        Skills.depend = 0
        Dice.crit_count = 0
        if Dice.check_pool:
            for x in Dice.check_pool:
                Dice.check(x)
            for x in Dice.s_s:
                Dice.check_result(x)
            if Dice.value != -999:
                Dice.roll_lock = Dice.crit_count  # locking in amount of rolls
                for x in Dice.dice_pool:
                    Dice.roll(x)
                for x in Skills.skill_pool:
                    Skills.skill_spend(x)
            Dice.roll_results()
        else:
            for x in Dice.dice_pool:
                Dice.roll(x)
            for x in Skills.skill_pool:
                Skills.skill_spend(x)
            Dice.roll_results()
        progress += 1
        if progress >= config.max_roll/10:
            p.step(config.max_roll/10)
            load_window.update()
            progress = 0
    Dice.prepare_check = 0
    Results.format()
    Results.prepare()
    result.plot_points()
    load_window.destroy()
    openResultWindow()

def openResultWindow():
    global result_window
    result_window = Toplevel(root)
    result_window.title("Results")
    Button(result_window, text='Save Results', command=lambda: screenshot()).grid(row=3, column=0)
    result.graph()
    result.tally.clear()        #clearing results for next run
    result.misses = 0
    result.bar_dict1.clear()
    result.bar_dict2.clear()
    result.average = 0
    result.totalsum = 0
    result.crit_total = 0
    result.crit_divider = 0
    result_window.grab_set()

def screenshot():
    x, y = result_window.winfo_rootx(), result_window.winfo_rooty()
    w, h = result_window.winfo_width(), result_window.winfo_height()
    random = int(time.time())
    filename = "C:/Users/" + str(os.getlogin()) + "/Desktop/" + str(random) + ".jpg"
    ss = pg.screenshot(filename, region=(x, y, w, h))
    ss.show()
    result_window.deiconify()

Die_frame = LabelFrame(root, text="Dice", padx=8, pady=8)
Die_frame.pack(padx=10, pady=10, side=LEFT, fill=BOTH)
Skill_frame = LabelFrame(root, text="Skills", padx=8, pady=8)
Skill_frame.pack(padx=10, pady=10, side=TOP)
Options_frame = LabelFrame(root, text="Options", padx=8, pady=8)
Options_frame.pack(padx=10, pady=10, side=BOTTOM, fill=BOTH)

Select_Label = Label(Die_frame, text="Define dice").grid(row=0, column=2)
Amount_Label = Label(Die_frame, text="Amt").grid(row=0, column=3)
Crit_Label = Label(Die_frame, text="Crit value -").grid(row=11, column=2)
Crit_Label = Label(Die_frame, text="Behavior").grid(row=11, column=2, padx=(20, 0), columnspan=3)
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
            Entrybox_Widget.Amount_objects[i].configure(state=DISABLED)
        else:
            Entrybox_Widget.Face_objects[i].configure(state=NORMAL)
            Entrybox_Widget.Amount_objects[i].configure(state=NORMAL)
            if Entrybox_Widget.Amount_values[i].get() == 0:
                Entrybox_Widget.Amount_objects[i].delete(0, END)
                Entrybox_Widget.Amount_objects[i].insert(0, 1)


def enable_check_skill():
    for i in range(0, 10):
        if skill_values[i].get() == 0:
            Entrybox_Widget.Cost_objects[i].configure(state=DISABLED)
            Entrybox_Widget.Damage_objects[i].configure(state=DISABLED)
            repeat_objects[i].configure(state=DISABLED)
            initiate_objects[i].configure(state=DISABLED)
            depend_objects[i].configure(state=DISABLED)
        else:
            Entrybox_Widget.Cost_objects[i].configure(state=NORMAL)
            Entrybox_Widget.Damage_objects[i].configure(state=NORMAL)
            repeat_objects[i].configure(state=NORMAL)
            initiate_objects[i].configure(state=NORMAL)
            depend_objects[i].configure(state=NORMAL)


def initiator_switch():
    for i in range(0, 10):
        if initiate_values[i].get() == 1:
            depend_values[i].set(0)


def dependant_switch():
    for i in range(0, 10):
        if depend_values[i].get() == 1:
            initiate_values[i].set(0)


for i in range(0, 10):  # creating checkboxes
    value_inside = IntVar()
    value_inside.set(0)
    check = Checkbutton(Die_frame, variable=value_inside, command=lambda: enable_check_face())
    check.grid(row=i + 1, column=1)
    check_values.append(value_inside)
check_length = len(check_values)

Skill_value = IntVar()
Skill_check = Checkbutton(Skill_frame, variable=Skill_value, command=lambda: all_skillcheck()).grid(row=0, column=0)


def all_skillcheck():  # all-checkbox function
    if Skill_value.get():
        for i in range(0, check_length):
            skill_values[i].set(1)
    else:
        for i in range(0, check_length):
            skill_values[i].set(0)
    enable_check_skill()

def all_dropmenu_swap(*options):  # all-dropmenu function
    if drop_value_all.get() == 'Sum':
        for i in range(0, 10):
            drop_values[i].set(drop_options[0])
    if drop_value_all.get() == 'Max':
        for i in range(0, 10):
            drop_values[i].set(drop_options[1])
    if drop_value_all.get() == 'Min':
        for i in range(0, 10):
            drop_values[i].set(drop_options[2])


skill_values = []
repeat_values = []
repeat_objects = []
initiate_values = []
initiate_objects = []
depend_values = []
depend_objects = []

# Skills: Cost, Damage, Repeatable, initiator/dependant, Skill point carryover between rolls
for i in range(0, 10):  # creating skill checkboxes
    value_inside = IntVar()
    value_inside.set(0)
    check = Checkbutton(Skill_frame, variable=value_inside, command=lambda: enable_check_skill())
    check.grid(row=i + 1, column=0)
    skill_values.append(value_inside)

for i in range(0, 10):  # creating repeatable checkboxes
    value_inside = IntVar()
    value_inside.set(0)
    check = Checkbutton(Skill_frame, variable=value_inside, state=DISABLED)
    check.grid(row=i + 1, column=3, padx=(8, 0))
    repeat_objects.append(check)
    repeat_values.append(value_inside)

for i in range(0, 10):  # creating initiate checkboxes
    value_inside = IntVar()
    value_inside.set(0)
    check = Checkbutton(Skill_frame, variable=value_inside, command=lambda: initiator_switch(), state=DISABLED)
    check.grid(row=i + 1, column=4, padx=(8, 0))
    initiate_objects.append(check)
    initiate_values.append(value_inside)

for i in range(0, 10):  # creating dependant checkboxes
    value_inside = IntVar()
    value_inside.set(0)
    check = Checkbutton(Skill_frame, variable=value_inside, command=lambda: dependant_switch(), state=DISABLED)
    check.grid(row=i + 1, column=5, padx=(8, 0))
    depend_objects.append(check)
    depend_values.append(value_inside)

#carryover
carry_check_label = Label(Skill_frame, text="point carry-over").grid(row=11, column=1, pady=(8, 0), columnspan=2)
carry_check_value = []
carry_check_inside = IntVar()
carry_check = Checkbutton(Skill_frame, variable=carry_check_inside)
carry_check.grid(row=11, column=3, padx=(8, 0), pady=(10, 0))
carry_check_value.append(carry_check_inside)
check_auto_graph_label = Label(Options_frame, text="Auto-graph").grid(row=5, column=0)
check_auto_graph_inside = IntVar()
check_auto_graph_value = []
check_auto_graph = Checkbutton(Options_frame, variable=check_auto_graph_inside)
check_auto_graph.grid(row=5, column=1)
check_auto_graph_value.append(check_auto_graph_inside)
check_auto_graph_value[0].set(1)
check_graph1_label = Label(Options_frame, text="Graph 'n' or more").grid(row=6, column=0)
check_graph1_inside = IntVar()
check_graph1_value = []
check_graph1 = Checkbutton(Options_frame, variable=check_graph1_inside)
check_graph1.grid(row=6, column=1)
check_graph1_value.append(check_graph1_inside)
check_graph1_value[0].set(1)
check_graph2_label = Label(Options_frame, text="Graph real").grid(row=7, column=0)
check_graph2_inside = IntVar()
check_graph2_value = []
check_graph2 = Checkbutton(Options_frame, variable=check_graph2_inside)
check_graph2.grid(row=7, column=1)
check_graph2_value.append(check_graph2_inside)
check_graph2_value[0].set(0)
def save():                 #save and load function for dice entry-boxes
    savefile = {}
    for i in range(0, 10):
        if Entrybox_Widget.Face_values[i].get():
            savefile["entry" + str(i)] = Entrybox_Widget.Face_values[i].get()
    with open("saved_settings.dat", "wb") as pickle_file:
        pickle.dump(savefile, pickle_file, pickle.HIGHEST_PROTOCOL)
    print(savefile)

def load():
    with open("saved_settings.dat", "rb") as pickle_file:
        savefile = pickle.load(pickle_file)
    for i in range(0, 10):
        if savefile.get("entry" + str(i)):
            Entrybox_Widget.Face_values[i].set(savefile.get("entry" + str(i)))


def char_length(i):  # limit only numbers and set max character limit
    if len(i) == 0:
        return True
    elif len(i) < 4 and i.isdigit():
        return True
    else:
        return False


def char_numeric(i):  # limit only numbers
    if len(i) < 8 and i.isdigit() and int(i) >= 1:
        return True
    else:
        return False


#entrybox validations
clcmd = (root.register(char_length), '%P')
cncmd = (root.register(char_numeric), '%P')

#labels
Cost_Label = Label(Skill_frame, text="cost   -").grid(row=0, column=1, padx=(8, 0))
Damage_Label = Label(Skill_frame, text="value").grid(row=0, column=2)
Repeat_Label = Label(Skill_frame, text="∞").grid(row=0, column=3, padx=(5, 0))
Initiator_Label = Label(Skill_frame, text="1").grid(row=0, column=4)
Dependant_Label = Label(Skill_frame, text="0").grid(row=0, column=5)
Repeat_Label = Label(Options_frame, text="Rolls:").grid(row=2, column=0, padx=(0, 40))
Graph_Label = Label(Options_frame, text="Graph range:").grid(row=4, column=0)
Cost_values = []


class Entrybox_Widget():
    Face_objects = []
    Amount_objects = []
    Cost_objects = []
    Damage_objects = []
    Face_values = []
    Amount_values = []
    Crit_value = []
    Cost_values = []
    Damage_values = []
    Repeat_value = []
    Graph_value = []

    def add_face_entry(self):  # defining all entryboxes
        value_inside = StringVar()
        entry = Entry(Die_frame, width=40, textvariable=value_inside, state=DISABLED)
        entry.grid(row=i + 1, column=2, padx=(2, 4))
        entry.insert(0, '')
        Entrybox_Widget.Face_objects.append(entry)
        Entrybox_Widget.Face_values.append(value_inside)

    def add_amount_entry(self):
        value_inside = IntVar()
        entry = Entry(Die_frame, width=4, validate="key", validatecommand=clcmd, textvariable=value_inside,
                      state=DISABLED)
        entry.grid(row=i + 1, column=3, padx=(2, 4))
        Entrybox_Widget.Amount_objects.append(entry)
        Entrybox_Widget.Amount_values.append(value_inside)

    def add_cost_entry(self):
        value_inside = IntVar()
        entry = Entry(Skill_frame, width=4, validate="key", validatecommand=clcmd, textvariable=value_inside,
                      state=DISABLED)
        entry.grid(row=i + 1, column=1)
        Entrybox_Widget.Cost_objects.append(entry)
        Entrybox_Widget.Cost_values.append(value_inside)

    def add_damage_entry(self):
        value_inside = IntVar()
        entry = Entry(Skill_frame, width=4, validate="key", validatecommand=clcmd, textvariable=value_inside,
                      state=DISABLED)
        entry.grid(row=i + 1, column=2, padx=5)
        Entrybox_Widget.Damage_objects.append(entry)
        Entrybox_Widget.Damage_values.append(value_inside)

    def add_crit_entry(self):
        value_inside = IntVar()
        value_inside.set(1)
        entry = Entry(Die_frame, width=4, validate="key", validatecommand=clcmd, textvariable=value_inside)
        entry.grid(row=12, column=2)
        Entrybox_Widget.Crit_value.append(value_inside)

    def add_rolls_entry(self):
        value_inside = IntVar()
        value_inside.set(100000)
        entry = Entry(Options_frame, width=8, validate="key", validatecommand=cncmd, textvariable=value_inside)
        entry.grid(row=2, column=1, pady=5, padx=(38, 0))
        Entrybox_Widget.Repeat_value.append(value_inside)

    def add_graph_entry(self):
        value_inside = IntVar()
        value_inside.set(i*10)
        entry = Entry(Options_frame, width=4, validate="key", validatecommand=clcmd, textvariable=value_inside)
        entry.grid(row=4, column=i+1, columnspan=2)
        Entrybox_Widget.Graph_value.append(value_inside)


for i in range(0, 10):  # creating entryboxes
    Entrybox_Widget.add_face_entry(i)
    Entrybox_Widget.add_amount_entry(i)
    Entrybox_Widget.add_cost_entry(i)
    Entrybox_Widget.add_damage_entry(i)
    if i < 2:
        Entrybox_Widget.add_graph_entry(i)
    if i < 1:
        Entrybox_Widget.add_crit_entry(i)
        Entrybox_Widget.add_rolls_entry(i)

load_button = Button(Die_frame, text='Load Dice', command=lambda: load()).grid(row=12, column=4)
save_button = Button(Die_frame, text='Save Dice', command=lambda: save()).grid(row=14, column=4, pady=(20, 0))

crit_options = '∞', '2x'
crit_value_type = StringVar()
crit_behavior = []

critmenu = OptionMenu(Die_frame, crit_value_type, *crit_options)
crit_value_type.set(crit_options[0])
critmenu.grid(row=12, column=2, padx=(20, 0), columnspan=3)
crit_behavior.append(crit_value_type)

drop_options = 'Sum', 'Max', 'Min'
drop_values = []

for i in range(0, 10):  # creating drop menu's
    value_inside = StringVar()
    value_inside.set(drop_options[0])
    dropmenu = OptionMenu(Die_frame, value_inside, *drop_options)
    dropmenu.configure(width=5)
    dropmenu.grid(row=i + 1, column=4)
    drop_values.append(value_inside)

drop_value_all = StringVar()
drop_value_all.set(drop_options[0])
all_dropmenu = OptionMenu(Die_frame, drop_value_all, *drop_options)
all_dropmenu.configure(width=5)
all_dropmenu.grid(row=0, column=4)
drop_value_all.trace('w', lambda x, y, z: all_dropmenu_swap())    #trace needs 3 arguments, xyz are dummies


test_button = Button(Options_frame, text='Start', width=8, height=1, command=lambda: execute()).grid(row=7, column=5, rowspan=3)

#faces, primary=0, crit_behavior=0, crit_value=1, state=0, amount=1, weight=0
def show():  # test function
    for i in range(0, 10):
        if check_values[i].get() and Entrybox_Widget.Face_values[i].get():
            die = Dice((Dice_Construct(Dice_Correct(Entrybox_Widget.Face_values[i].get()))))
        else:
            pass
    #print(Dice.dice_pool[0].faces)
    for i in Dice.dice_pool:
        print(i.faces)

#faces, primary=0, crit_behavior=0, crit_value=1, state=0, amount=1, weight=0
def fill_dicepool():            #create dice where checkbox = 1 and entry is not empty
    if crit_behavior[0].get() == '∞':
        critb = 0
    else:
        critb = 1
    for i in range(0, 10):
        if check_values[i].get() and Entrybox_Widget.Face_values[i].get():
            if drop_values[i].get() == 'Sum':
                state = 0
            elif drop_values[i].get() == 'Max':
                state = 1
            else:
                state = 2
            die = Dice((Dice_Construct(Dice_Correct(Entrybox_Widget.Face_values[i].get()))),
                       0, critb, Entrybox_Widget.Crit_value[0].get(), state, Entrybox_Widget.Amount_values[i].get())
        else:
            pass

# Skills: Cost, Damage, Repeatable, dependant, initiator
def fill_skillpool():
    Skills.skill_pool.clear()
    for i in range(0, 10):
        if skill_values[i].get():
            skill = Skills(Entrybox_Widget.Cost_values[i].get(), Entrybox_Widget.Damage_values[i].get(),
                           repeat_values[i].get(), depend_values[i].get(), initiate_values[i].get())
def config_settings():
    global result
    result = Results()
    global config
    config = Settings(Entrybox_Widget.Repeat_value[0].get(), Entrybox_Widget.Graph_value[0].get(),
                      Entrybox_Widget.Graph_value[1].get())

def execute():              #any dice that can miss become primary
    Dice.dice_pool.clear()
    fill_dicepool()
    for i in Dice.dice_pool:
        for x in i.faces:
            if x == -999:
                i.primary = 1
            else:
                pass
    fill_skillpool()
    config_settings()
    Dice.prepare()
    #print(Dice.dice_pool)
    #print(Dice.check_pool[0].faces)
    openLoadWindow()


def Dice_Correct(*args):  # function to return readable dice
    for x in args:
        if ',' in x:
            return x
        else:
            temp = list([val for val in x if val.isnumeric()])
            return "".join(temp)


def Dice_Construct(*args):        #function to turn numbers into dice. removing trailing commas and empty entries.
    for x in args:
        if ',' in x:
            stripped = x.strip(',')
            temp = [float(e) for e in stripped.split(',') if not e == ""]
            return temp
        else:
            size = int(x)
            temp = []
            for i in range(0, size):
                temp.append(i + 1)
            return temp

"""GUI----END----GUI----END----GUI----END----GUI----END----GUI"""

class Settings:

    def __init__(self, max_roll=10000, graph_start=0, graph_end=15):           #0 - max(primary), 1 - min(primary)
        self.max_roll = max_roll
        self.graph_start = graph_start
        self.graph_end = graph_end


class Skills:
    skill_pool = []
    depend = 0

    def __init__(self, cost=0, damage=0, repeat=0, dependant=0, initiator=0):
        self.cost = cost                #0=no repeats, 1 is infinite, if dependant=1, then only activates via initiator
        self.damage = damage
        self.repeat = repeat
        self.dependant = dependant
        self.initiator = initiator
        Skills.skill_pool.append(self)

    def skill_spend(self):                              #spend skill points
        if self.cost > Dice.skill_count:
            return
        if self.damage != 0 or self.initiator != 0:
            if self.initiator != 0:
                Skills.depend = 1
            if self.dependant != 1:
                if self.repeat == 0:
                    Dice.sub_total += self.damage
                    Dice.skill_count -= self.cost
                else:
                    while self.cost <= Dice.skill_count:
                        Dice.sub_total += self.damage
                        Dice.skill_count -= self.cost
            else:
                if Skills.depend != 0:
                    if self.repeat == 0:
                        Dice.sub_total += self.damage
                        Dice.skill_count -= self.cost
                    else:
                        while self.cost <= Dice.skill_count:
                            Dice.sub_total += self.damage
                            Dice.skill_count -= self.cost
                else:
                    return

    @classmethod
    def prepare(cls):                           #sorting skill pool so more expensive/initiator skills are used first
        Skills.skill_pool = sorted(Skills.skill_pool, key=lambda x: x.damage, reverse=True)
        copy = sorted(Skills.skill_pool, key=lambda x: x.initiator, reverse=True)
        Skills.skill_pool = copy


class Dice(object):
    sub_total = 0
    roll_repeats = 0
    roll_lock = 0
    crit_count = 0
    skill_count = 0
    temp_roll = []
    dice_pool = []
    dice_pool_copy = []
    check_pool = []
    s_s = []
    prepare_check = 0
    function_check = 0
    value = 0

    def __init__(self, faces, primary=0, crit_behavior=0, crit_value=1, state=0, amount=1, weight=0):
        self.faces = faces
        self.primary = primary
        self.crit_behavior = crit_behavior
        self.crit_value = crit_value
        self.state = state
        self.amount = amount
        self.weight = weight
        Dice.dice_pool.append(self)

    @classmethod
    def prepare(cls):
        for x in Dice.dice_pool:
            Dice.sort(x)
        copy = sorted(Dice.check_pool, key=lambda x: x.weight, reverse=True)        #sorting check pool by highest face-values first
        Dice.check_pool = copy
        Dice.dice_pool = Dice.dice_pool_copy                    #copying back the dice pool without check dice

    def sort(self):                                      #preparing once for entire rolling process
        if Dice.prepare_check != 1:
            Dice.prepare_check = 1
            Skills.prepare()                                #also preparing skills
            Dice.crit_count = 0
            Dice.check_pool.clear()
            Dice.dice_pool_copy = Dice.dice_pool.copy()     #making a copy to prevent errors
        if self.primary != 1:
            return
        else:                                               #filling the check pool with primary dice
            self.weight = sum(self.faces)
            Dice.check_pool.append(self)
            Dice.dice_pool_copy.remove(self)

    @classmethod                                        #the rolling function
    def they_see_me_rollin(cls):
        for i in range(0, config.max_roll):
            Dice.function_check = 0
            Skills.depend = 0
            Dice.crit_count = 0
            if Dice.check_pool:
                for x in Dice.check_pool:
                    Dice.check(x)
                for x in Dice.s_s:
                    Dice.check_result(x)
                if Dice.value != -999:
                    Dice.roll_lock = Dice.crit_count             #locking in amount of rolls
                    for x in Dice.dice_pool:
                        Dice.roll(x)
                    for x in Skills.skill_pool:
                        Skills.skill_spend(x)
                Dice.roll_results()
            else:
                for x in Dice.dice_pool:
                    Dice.roll(x)
                for x in Skills.skill_pool:
                    Skills.skill_spend(x)
                Dice.roll_results()
        p.step()
        load_window.update()
    def check(self):                                #rolling primary dice
        if self.primary != 1:
            return
        if self.state == 2:
            if Dice.function_check != 1:
                Dice.function_check = 1
                Dice.sub_total = 0
                if carry_check_value[0].get() == 0:
                    Dice.skill_count = 0
                Dice.crit_count = 0
                Dice.s_s.clear()
                Dice.s_s.append(self)
                Dice.value = 999
            for d in range(0, self.amount):
                min_value = random.choice(self.faces)
                if min_value < Dice.value:
                    Dice.value = min_value
                    Dice.s_s.clear()
                    Dice.s_s.append(self)
        else:
            if Dice.function_check != 1:
                Dice.function_check = 1
                Dice.sub_total = 0
                if carry_check_value[0].get() == 0:
                    Dice.skill_count = 0
                Dice.crit_count = 0
                Dice.s_s.clear()
                Dice.s_s.append(self)
                Dice.value = -999
            for d in range(0, self.amount):
                max_value = random.choice(self.faces)
                if max_value > Dice.value:
                    Dice.value = max_value
                    Dice.s_s.clear()
                    Dice.s_s.append(self)

    def check_result(self):                     #check for primary crits/misses
        if Dice.value == -999:
            result.misses += 1
            Dice.sub_total = 0
        elif Dice.value == 999:
            self.crit_resolver()
        else:
            if (Dice.value % 1) != 0:
                temp = (Dice.value % 1)
                Dice.skill_count += (temp * 10)
                Dice.sub_total += (Dice.value - temp)
            else:
                Dice.sub_total += Dice.value

    def roll(self):
        Dice.crit_action()                      #decide what happens for crits
        for y in range(-1, Dice.roll_repeats):
            Dice.temp_roll.clear()
            for d in range(0, self.amount):
                Dice.temp_roll.append(random.choice(self.faces))
            self.state_resolver()

    def state_resolver(self):
        if self.state == 0:                     #sum of all rolled values
            for x in Dice.temp_roll:
                if (x % 1) != 0:
                    temp = (x % 1)
                    Dice.skill_count += (temp * 10)
                    Dice.sub_total += (x - temp)
                else:
                    if x == 999:
                        Dice.value = x
                        self.crit_resolver()
                    else:
                        Dice.sub_total += x
        if self.state == 1:                     #max of all rolled values
            max_value = max(Dice.temp_roll)
            if (max_value % 1) != 0:
                temp = (max_value % 1)
                Dice.skill_count += (temp * 10)
                Dice.sub_total += (max_value - temp)
            else:
                if max_value == 999:
                    Dice.value = max_value
                    self.crit_resolver()
                else:
                    Dice.sub_total += max_value
        if self.state == 2:                     #min of all rolled values
            min_value = min(Dice.temp_roll)
            if (min_value % 1) != 0:
                temp = (min_value % 1)
                Dice.skill_count += (temp * 10)
                Dice.sub_total += (min_value - temp)
            else:
                if min_value == 999:
                    Dice.value = min_value
                    self.crit_resolver()
                else:
                    Dice.sub_total += min_value

    @classmethod
    def crit_action(cls):
        if Dice.check_pool:
            Dice.roll_repeats = Dice.roll_lock      #rolling dice dependant on primary behavior
        else:
            Dice.roll_repeats = 0                   #rolling once without primary dice

    def crit_resolver(self):
        temp = Dice.value
        if self.crit_behavior == 0:                 #rerolling crits until no crit
            while temp == 999:
                Dice.crit_count += 1
                Dice.sub_total += self.crit_value
                temp = random.choice(self.faces)
            if Dice.crit_count > result.crit_chain:
                result.crit_chain = Dice.crit_count
            if temp == -999:
                Dice.sub_total += 0
            else:
                if (temp % 1) != 0:
                    temp2 = (temp % 1)
                    Dice.skill_count += (temp2 * 10)
                    Dice.sub_total += (temp - temp2)
                else:
                    Dice.sub_total += temp
        if self.crit_behavior == 1:                 #rerolling once on crit
            Dice.crit_count += 1
            Dice.sub_total += self.crit_value
            temp = random.choice(self.faces)
            if Dice.crit_count > result.crit_chain:
                result.crit_chain = Dice.crit_count
            if temp == -999:
                Dice.sub_total += 0
            elif temp == 999:
                Dice.sub_total += self.crit_value
            else:
                if (temp % 1) != 0:
                    temp2 = (temp % 1)
                    Dice.skill_count += (temp2 * 10)
                    Dice.sub_total += (temp - temp2)
                else:
                    Dice.sub_total += temp


    @classmethod
    def roll_results(cls):                                  #finalizing roll results
        if round(Dice.sub_total, 2) not in Results.tally:
            Results.tally[round(Dice.sub_total, 2)] = 0
        Results.tally[round(Dice.sub_total, 2)] += 1
        result.totalsum += Dice.sub_total
        if Dice.crit_count != 0:
            result.crit_total += Dice.sub_total
            result.crit_divider += 1
        Dice.sub_total = 0


class Results:
    tally = {}
    bar_dict1 = {}
    bar_dict2 = {}
    average = 0
    crit_average = 0

    def __init__(self, totalsum=0, misses=0, crit_chain=0, crit_total=0, crit_divider=0, state=0):  #state 0 = 'chance of n or higher', 1 = 'n exactly'
        self.totalsum = totalsum
        self.misses = misses
        self.crit_chain = crit_chain
        self.crit_total = crit_total
        self.crit_divider = crit_divider
        self.state = state

    @classmethod                                #preparing plot points for bar graph
    def prepare(cls):
        if check_auto_graph_value[0].get():
            start = min(Results.tally)
            stop = max(Results.tally)
            for i in range(int(start), int(stop+1)):
                result.bar_dict1[i] = 0
                result.bar_dict2[i] = 0
        else:
            for i in range(config.graph_start, config.graph_end + 1):
                result.bar_dict1[i] = 0
                result.bar_dict2[i] = 0

    def plot_points(self):                      #preparing plot points for bar graph
        if check_graph1_value[0].get():
            for x in result.bar_dict1:
                for y in result.tally.keys():
                    if y >= x:
                        result.bar_dict1[x] += result.tally[y]
                result.bar_dict1[x] = round((result.bar_dict1[x] / config.max_roll) * 100, 2)
                if min(Results.tally) <= 0:
                    result.bar_dict1[0] = round((result.misses / config.max_roll) * 100, 2)
        if check_graph2_value[0].get():
            for a in result.bar_dict2:
                for b in result.tally.keys():
                    if b == a:
                        result.bar_dict2[a] = result.tally[b]
                result.bar_dict2[a] = round((result.bar_dict2[a] / config.max_roll) * 100, 2)


    @classmethod                             #preparing results
    def format(cls):
        cls.average = round(result.totalsum / (config.max_roll - result.misses), 2)
        if result.crit_divider != 0:
            cls.crit_average = round(result.crit_total/result.crit_divider, 2)

    def graph(self):                         #outputing bar graph 1
        if check_graph1_value[0].get():
            percentage = result.bar_dict1.values()
            damage = result.bar_dict1.keys()
            x = np.arange(len(damage))
            width = 0.8
            fig, ax = plt.subplots()
            ax.set_ylabel('% chance')
            ax.set_xlabel('n or more')
            #ax.set_title('Damage chart')
            ax.set_xticks(x, damage)
            pps = ax.bar(x, percentage, width, label='% chance')
            for p in pps:
                height = p.get_height()
                ax.annotate('{}'.format(height), xy=(p.get_x() + p.get_width() / 2, height), xytext=(0, 0),
                            textcoords="offset points", ha='center', va='bottom', fontsize=9)
            chart_type = FigureCanvasTkAgg(fig, result_window)
            chart_type.get_tk_widget().grid(row=1, column=0)

        if check_graph2_value[0].get():        #outputing bar graph 2
            print(result.bar_dict1)
            print(result.bar_dict2)
            percentage2 = result.bar_dict2.values()
            damage2 = result.bar_dict2.keys()
            x2 = np.arange(len(damage2))
            width2 = 0.8
            fig2, ax2 = plt.subplots()
            ax2.set_ylabel('% chance')
            ax2.set_xlabel('real')
            #ax.set_title('Damage chart')
            ax2.set_xticks(x2, damage2)
            pps2 = ax2.bar(x2, percentage2, width2, label='% chance')
            for p in pps2:
                height = p.get_height()
                ax2.annotate('{}'.format(height), xy=(p.get_x() + p.get_width() / 2, height), xytext=(0, 0),
                            textcoords="offset points", ha='center', va='bottom', fontsize=9)
            chart_type2 = FigureCanvasTkAgg(fig2, result_window)
            chart_type2.get_tk_widget().grid(row=1, column=1)


load()

mainloop()
