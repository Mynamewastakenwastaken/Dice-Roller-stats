import random


class Settings:

    def __init__(self, max_roll=100000, stalwart_stressed=0, crit_value=1):       #0 - max(primary), 1 - min(primary)
        self.max_roll = max_roll
        self.stalwart_stressed = stalwart_stressed
        self.crit_value = crit_value


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
            config.stalwart_stressed = 0
            Dice.crit_count = 0
            Dice.check_pool.clear()
            Dice.dice_pool_copy = Dice.dice_pool.copy()             #making a copy to prevent errors
        if self.primary != 1:
            return
        else:
            self.weight = sum(self.faces)
            Dice.check_pool.append(self)
            Dice.dice_pool_copy.remove(self)
            if self.state > config.stalwart_stressed:
                config.stalwart_stressed = self.state

    def check(self):
        if self.primary != 1:
            return
        if config.stalwart_stressed != 0:
            if Dice.function_check != 1:
                Dice.function_check = 1
                Dice.sub_total = 0
                Dice.skill_count = 0
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
            Results.totalsum += 0
            Results.tally.append(0)
        elif Dice.value == 999:
            self.crit_resolver()
        else:
            if (Dice.value % 1) != 0:
                temp = (Dice.value % 1)
                Dice.temp_skill.append(temp * 10)
                Dice.sub_total += (Dice.value - temp)
            else:
                Dice.sub_total += Dice.value

    def crit_resolver(self):
        while Dice.value == 999:
            Dice.crit_count += 1
            Dice.sub_total += self.crit_value
            Dice.value = random.choice(self.faces)
        if Dice.value == -999:
            Dice.sub_total += 0
        else:
            if (Dice.value % 1) != 0:
                temp = (Dice.value % 1)
                Dice.temp_skill.append(temp * 10)
                Dice.sub_total += (Dice.value - temp)
            else:
                Dice.sub_total += Dice.value


    def roll(self):
        Dice.temp_skill.clear()
        Dice.temp_roll.clear()
        for d in range(0, self.amount):
            face = random.choice(self.faces)
            if (face % 1) != 0:
                temp = (face % 1)
                Dice.temp_skill.append(temp * 10)
                Dice.temp_roll.append(face - temp)
            else:
                Dice.temp_roll.append(face - temp)
        self.state_resolver()

    def state_resolver(self):
        if self.state == 0:
            Dice.skill_count += sum(Dice.temp_skill)
            Dice.sub_total += sum(Dice.temp_roll)
        #else:
            #sum/min/max



    #@classmethod
    #def roll_results(cls):
        #for Dice.skill_count != 0:

        #Dice.function_check = 0

class Results:
    tally = []
    totalsum = 0



config = Settings()

skill1 = Skills(1, 0)
skill2 = Skills(2, 3)
skill3 = Skills(3, 0)
skill4 = Skills(4, 0)

die2 = Dice([1, 1, 1, 2, 2, 3])
die3 = Dice([0, 0, 0, 0.1, 1.1, 0.2])
die4 = Dice([-999, -999, -999, 2, 1.1, 999], 1)
die1 = Dice([-999, 1, 1, 2, 1.1, 999], 1)

print(len(Dice.dice_pool))
for x in Dice.dice_pool:
    Dice.prepare(x)
copy = sorted(Dice.check_pool, key=lambda x: x.weight, reverse=True)
Dice.check_pool = copy
for i in range(0, config.max_roll):
    for x in Dice.check_pool:
        Dice.check(x)