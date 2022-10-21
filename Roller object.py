import random
import matplotlib.pyplot as plt
import numpy as np


class Settings:

    def __init__(self, max_roll=10000, stalwart_stressed=0, crit_value=1, graph_start=0, graph_end=6):       #0 - max(primary), 1 - min(primary)
        self.max_roll = max_roll
        self.stalwart_stressed = stalwart_stressed
        self.crit_value = crit_value
        self.graph_start = graph_start
        self.graph_end = graph_end


class Skills:
    skill_pool = []

    def __init__(self, cost=0, damage=0, repeat=0):             #0=no repeats, 1 is infinite
        self.cost = cost
        self.damage = damage
        self.repeat = repeat
        Skills.skill_pool.append(self)

    def skill_spend(self):
        if self.damage == 0:
            return
        if self.cost > Dice.skill_count:
            return
        else:
            if self.repeat == 0:
                Dice.sub_total += self.damage
                Dice.skill_count -= self.cost
            else:
                while self.cost <= Dice.skill_count:
                    Dice.sub_total += self.damage
                    Dice.skill_count -= self.cost

    @classmethod
    def prepare(cls):
        copy = sorted(Skills.skill_pool, key=lambda x: x.cost, reverse=True)
        Skills.skill_pool = copy

class Dice(object):
    sub_total = 0
    crit_count = 0
    skill_count = 0
    temp_roll = []
    temp_skill = []
    dice_pool = []
    dice_pool_copy = []
    check_pool = []
    s_s = []
    prepare_check = 0
    function_check = 0
    value = 0

    def __init__(self, faces, primary=0, crit_value=1, state=0, amount=1, weight=0):
        self.faces = faces
        self.primary = primary
        self.crit_value = crit_value
        self.state = state
        self.amount = amount
        self.weight = weight
        Dice.dice_pool.append(self)

    def prepare(self):
        if Dice.prepare_check != 1:
            Dice.prepare_check = 1
            Skills.prepare()
            Results.prepare()
            Dice.crit_count = 0
            Dice.check_pool.clear()
            Dice.dice_pool_copy = Dice.dice_pool.copy()             #making a copy to prevent errors
        if self.primary != 1:
            return
        else:
            self.weight = sum(self.faces)
            Dice.check_pool.append(self)
            Dice.dice_pool_copy.remove(self)
            if self.state > config.stalwart_stressed:               #!!!!!!maybe remove?!!!!!!!
                config.stalwart_stressed = self.state

    def check(self):
        if self.primary != 1:
            return
        if config.stalwart_stressed != 0:
            if Dice.function_check != 1:
                Dice.function_check = 1
                Dice.sub_total = 0
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

    def check_result(self):
        if Dice.value == -999:
            Results.misses += 1
        elif Dice.value == 999:
            temp = Dice.value
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
        else:
            if (Dice.value % 1) != 0:
                temp = (Dice.value % 1)
                Dice.skill_count += (temp * 10)
                Dice.sub_total += (Dice.value - temp)
            else:
                Dice.sub_total += Dice.value



    def roll(self):
        for y in range (-1, Dice.crit_count):
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
                    Dice.sub_total += x
        #else:
            #sum/min/max

    @classmethod
    def roll_results(cls):
        if int(Dice.sub_total) not in Results.tally:
            Results.tally[int(Dice.sub_total)] = 0
        Results.tally[int(Dice.sub_total)] += 1
        result.totalsum += Dice.sub_total


class Results:
    tally = {}
    bar_dict = {}
    misses = 0
    def __init__(self, totalsum=0, crit_chain=0, crit_count=0):
        self.totalsum = totalsum
        self.crit_chain = crit_chain
        self.crit_count = crit_count

    @classmethod
    def prepare(cls):
        for i in range(config.graph_start, config.graph_end+1):
            result.bar_dict[i] = 0
    def plot_points(self):
        for x in result.bar_dict:
            for y in result.tally.keys():
                if y >= x:
                    result.bar_dict[x] += result.tally[y]
            result.bar_dict[x] = round((result.bar_dict[x]/config.max_roll)*100, 2)
        if config.graph_start <= 0:
            result.bar_dict[0] = round((result.misses/config.max_roll)*100, 2)
    def graph(self):
        percentage = result.bar_dict.values()
        damage = result.bar_dict.keys()
        x = np.arange(len(damage))
        width = 0.8
        fig, ax = plt.subplots()
        ax.set_ylabel('% chance')
        ax.set_xlabel('n Damage or more')
        ax.set_title('Damage chart')
        ax.set_xticks(x, damage)
        ax.set_xticklabels(result.bar_dict.keys())
        pps = ax.bar(x, percentage, width, label='% chance')
        for p in pps:
            height = p.get_height()
            ax.annotate('{}'.format(height),
                        xy=(p.get_x() + p.get_width() / 2, height),
                        xytext=(0, 0),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        plt.show()




config = Settings()
result = Results()

#cost=0, damage=0, repeat=0)
skill1 = Skills(1, 0)
skill2 = Skills(2, 4)
skill3 = Skills(3, 0)
skill4 = Skills(4, 0)

#faces, primary=0, crit_value=1, state=0, amount=1, weight=0
die1 = Dice([-999, 1, 1, 2, 1.1, 999], 1)
die2 = Dice([0, 0, 0, 0.1, 1.1, 0.2])
#die3 = Dice([1, 1, 1, 2, 2, 3])
#die4 = Dice([-999, -999, -999, 2, 1.1, 999], 1)


for x in Dice.dice_pool:
    Dice.prepare(x)
copy = sorted(Dice.check_pool, key=lambda x: x.weight, reverse=True)
Dice.check_pool = copy
Dice.dice_pool = Dice.dice_pool_copy
for i in range(0, config.max_roll):
    Dice.function_check = 0
    for x in Dice.check_pool:
        Dice.check(x)
    for x in Dice.s_s:
        Dice.check_result(x)
    if Dice.value != -999:
        for x in Dice.dice_pool:
            Dice.roll(x)
        for x in Skills.skill_pool:
            Skills.skill_spend(x)
        Dice.roll_results()
result.plot_points()
result.graph()
