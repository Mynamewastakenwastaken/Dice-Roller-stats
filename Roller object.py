from tkinter import *
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
class Settings:

    def __init__(self, max_roll=1000, graph_start=0, graph_end=15):           #0 - max(primary), 1 - min(primary)
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

    @classmethod
    def prepare(cls):                           #sorting skill pool so more expensive/initiator skills are used first
        Skills.skill_pool = sorted(Skills.skill_pool, key=lambda x: x.damage, reverse=True)
        copy = sorted(Skills.skill_pool, key=lambda x: x.initiator, reverse=True)
        Skills.skill_pool = copy


class Dice(object):
    stressed = 1
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
            Skills.prepare()                                #also preparing skills and results
            Results.prepare()
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
    def check(self):                                #rolling primary dice
        if self.primary != 1:
            return
        if Dice.stressed != 0:
            if Dice.function_check != 1:
                Dice.function_check = 1
                Dice.sub_total = 0
               # Dice.skill_count = 0
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
              #  Dice.skill_count = 0
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
    bar_dict = {}
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
        for i in range(config.graph_start, config.graph_end + 1):
            result.bar_dict[i] = 0

    def plot_points(self):                      #preparing plot points for bar graph
        for x in result.bar_dict:
            if result.state == 0:
                for y in result.tally.keys():
                    if y >= x:
                        result.bar_dict[x] += result.tally[y]
                result.bar_dict[x] = round((result.bar_dict[x] / config.max_roll) * 100, 2)
                if config.graph_start <= 0:
                    result.bar_dict[0] = round((result.misses / config.max_roll) * 100, 2)
            if result.state == 1:
                for y in result.tally.keys():
                    if y == x:
                        result.bar_dict[x] = result.tally[y]
                result.bar_dict[x] = round((result.bar_dict[x] / config.max_roll) * 100, 2)


    @classmethod                             #preparing results
    def format(cls):
        cls.average = round(result.totalsum / (config.max_roll - result.misses), 2)
        if result.crit_divider != 0:
            cls.crit_average = round(result.crit_total/result.crit_divider, 2)

    def graph(self):                         #outputing bar graph
        percentage = result.bar_dict.values()
        damage = result.bar_dict.keys()
        x = np.arange(len(damage))
        width = 0.8
        fig, ax = plt.subplots()
        ax.set_ylabel('% chance')
        ax.set_xlabel('n Damage or more')
        ax.set_title('Damage chart')
        ax.set_xticks(x, damage)
        #ax.set_xticklabels(result.bar_dict.keys())
        pps = ax.bar(x, percentage, width, label='% chance')
        for p in pps:
            height = p.get_height()
            ax.annotate('{}'.format(height), xy=(p.get_x() + p.get_width() / 2, height), xytext=(0, 0),
                        textcoords="offset points", ha='center', va='bottom', fontsize=9)
        #plt.show()
        chart_type = FigureCanvasTkAgg(fig, root)
        chart_type.get_tk_widget().pack()


# max_roll=100000, graph_start=0, graph_end=10
config = Settings()
result = Results()

# cost=0, damage=0, repeat=0, dependant=0, initiator=0

skill1 = Skills(1, 2, 1, 1, 0)
skill2 = Skills(2, 4, 0, 0, 1)
skill3 = Skills(3, 0)
skill4 = Skills(4, 0)
skill5 = Skills(5, 0)

#!!! if primary dice are used, its crit behavior is always used !!!

# faces, primary=0, crit_behavior=0, crit_value=1, state=0, amount=1, weight=0        -> state: 0 sum, 1 max, 2 min <-
die1 = Dice([-999, 1, 1, 2, 1.1, 999], 1, 0, 1, 0, 1)              # attack die A: [-999, 1, 1, 2, 1.1, 999]   Z: [-999, -999, -999, 2, 1.1, 999]
die2 = Dice([0, 0, 0, 0.1, 1.1, 0.2], 0, 0, 0, 0, 1)               # phys_attack die B: [0, 1, 1, 1, 2, 2]      C: [1, 1, 1, 2, 2, 3]
#die3 = Dice([0, 0, 0, 0.1, 1.1, 0.2])                             # mag_attack die D: [0, 0, 0, 0.1, 1.1, 0.2] E: [0, 1, 1.1, 0.1, 0.2, 0.2]
#die4 = Dice([-999, -999, -999, 2, 1.1, 999], 1)

#for i in range(0, 10):
    #Dice.dice_pool.append(Dice([0]))

#Dice.dice_pool[0].faces = [1.0, 2.0, 3, 4, 5, 6, 7, 8]

def set_dice(self, **kwargs):            #Dice attribute setter
    for x, y in kwargs.items():
        set_dice(self, x, y)



Dice.prepare()
Dice.they_see_me_rollin()           #rolling
Dice.prepare_check = 0

Results.format()                    #preparing results

print('the average is: ' + str(Results.average))
print('highest streak is: ' + str(result.crit_chain) + ' at ' + str((max(Results.tally))))
result.plot_points()                #preparing graph plot points
result.graph()                      #output graph

mainloop()