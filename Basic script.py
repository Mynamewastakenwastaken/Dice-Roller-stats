import random

rolls = 100000      #rolling n times

totalSum = 0
success = 0
crit_streak = 0
max_damage = 0
total_crit = 0
crit_divider = 0
floor_count = 0
skill_points = 0
skill_point_total = 0
skill_floor_count = 0

stalwart_stressed = 0               #stawart = 1, stressed = 2 supersress = 3
damage_floor = 2                    #the chance to get n or higher
skill_floor = 3
skill_damage1 = 0
skill_damage2 = 4
skill_damage3 = 6
skill_damage4 = 8

a_die = [-1, 1, 1, 2, 1.1, 6]               #define dice values, 0.1 = skill, -1 = miss, 6 = crit. ONLY a_die can crit!
b_die = [0, 0, 0, 0.1, 1.1, 0.2]                #[-1, 1, 1, 2, 2, 6]    [0, 1, 1, 1, 2, 2]      [1, 1, 1, 2, 2, 3]
c_die = [0, 0, 0, 0, 0, 0]                 #[0, 0, 0, 0.1, 1.1, 0.2]     [0, 1, 1, 2, 2, 3]    [0, 1, 1.1, 0.1, 0.2, 0.2]
stress_die = [-1, -1, -1, 2, 1.1, 6]        #[0, 0, 0, 0, 0, 0]     [-1, 0, 0, 0, 1, 6]
for i in range(0, rolls):
    crit_count = 0
    skill_count = 0
    die1 = random.choice(a_die)
    die2 = random.choice(b_die)
    die3 = random.choice(c_die)
    crit = 0
    if stalwart_stressed == 1:
        ss_die1 = random.choice(a_die)
        stalwart = [die1, ss_die1]
        die1 = max(stalwart)
    if stalwart_stressed == 2:
        ss_die1 = die1
        ss_die2 = random.choice(stress_die)
        stalwart = [ss_die1, ss_die2]
        die1 = min(stalwart)
    if stalwart_stressed == 3:
        ss_die1 = random.choice(stress_die)
        ss_die2 = random.choice(stress_die)
        stalwart = [ss_die1, ss_die2]
        die1 = min(stalwart)
    if die1 == -1:
        totalSum += 0
        b = 0
        if b >= damage_floor:
            floor_count += 1
        if skill_count >= skill_floor:
            skill_floor_count += 1
    elif die1 == 6:
        while die1 == 6:
            crit_count += 1
            crit += 1
            skill_count += ((die2 % 1) + (die3 % 1)) * 10
            skill_points += skill_count
            skill_point_total += skill_count
            die2 -= (die2 % 1)
            die3 -= (die3 % 1)
            die1 = random.choice(a_die)
            die2 += random.choice(b_die)
            die3 += random.choice(c_die)
        if die1 < 0:
            crit += 0
        else:
            skill_count += (die1 % 1) * 10
            skill_points += skill_count
            skill_point_total += skill_count
            die1 -= (die1 % 1)
            crit += die1
        skill_count += ((die2 % 1) + (die3 % 1)) * 10
        skill_points += skill_count
        skill_point_total += skill_count
        die2 -= (die2 % 1)
        die3 -= (die3 % 1)
        a = [crit, die2, die3]
        b = sum(a)
        totalSum += b
        if skill_count >= skill_floor:
            skill_floor_count += 1
        while skill_count >= 4 and skill_damage4 > 0:
            totalSum += skill_damage4
            b += skill_damage4
            skill_count -= 4
        while skill_count >= 3 and skill_damage3 > 0:          #"while" for repeatable skills, "if" for one-use
            totalSum += skill_damage3
            b += skill_damage3
            skill_count -= 3
        while skill_count >= 2 and skill_damage2 > 0:
            totalSum += skill_damage2
            b += skill_damage2
            skill_count -= 2
        while skill_count >= 1 and skill_damage1 > 0:
            totalSum += skill_damage1
            b += skill_damage1
            skill_count -= 1
        total_crit += b
        crit_divider += 1
        if b > max_damage:
            max_damage = b
        if crit_count > crit_streak:
            crit_streak = crit_count
        if b >= damage_floor:
            floor_count += 1
    else:
        skill_count += ((die1 % 1) + (die2 % 1) + (die3 % 1)) * 10
        skill_points += skill_count
        skill_point_total += skill_count
        die1 -= (die1 % 1)
        die2 -= (die2 % 1)
        die3 -= (die3 % 1)
        a = [die1, die2, die3]
        b = sum(a)
        totalSum += b
        success += 1
        if skill_count >= skill_floor:
            skill_floor_count += 1
        while skill_count >= 3 and skill_damage3 > 0:           #"while" for repeatable skills, "if" for one-use
            totalSum += skill_damage3
            b += skill_damage3
            skill_count -= 3
        while skill_count >= 2 and skill_damage2 > 0:
            totalSum += skill_damage2
            b += skill_damage2
            skill_count -= 2
        while skill_count >= 1 and skill_damage1 > 0:
            totalSum += skill_damage1
            b += skill_damage1
            skill_count -= 1
        if b >= damage_floor:
            floor_count += 1

expected = totalSum/rolls
expected_skill = skill_point_total/rolls
average = totalSum/(success + crit_divider)
average_skill = skill_point_total/(success + crit_divider)       #counting all successful hits
crit_average = total_crit/crit_divider
crit_chance = 100 * (crit_divider/rolls)
value_realchance = 100 * (floor_count/rolls)
value_chance = 100 * (floor_count/(success + crit_divider))
real_skill = 100 * (skill_floor_count/rolls)
skill_chance = 100 * (skill_floor_count/(success + crit_divider))
fixed_result = '{0:.3g}'.format(expected)                       #rounding the end results
fixed_skill_result = '{0:.3g}'.format(expected_skill)
fixed_average = '{0:.3g}'.format(average)
fixed_average_skill = '{0:.3g}'.format(average_skill)
fixed_crit = '{0:.3g}'.format(crit_average)
fixed_critchance = '{0:.3g}'.format(crit_chance)
fixed_realvalue = '{0:.3g}'.format(value_realchance)
fixed_value = '{0:.3g}'.format(value_chance)
fixed_realskill = '{0:.3g}'.format(real_skill)
fixed_skill = '{0:.3g}'.format(skill_chance)
print("Expected damage is: " + str(fixed_result) + " and expected skill points are: " + str(fixed_skill_result))
print("Average damage is: " + str(fixed_average) + " and average skill points are: " + str(fixed_average_skill))
print("Average crit is: " + str(fixed_crit) + " at " + str(fixed_critchance) + "%")
(print("Real chance of dealing " + str(damage_floor) + " or more: " + str(fixed_realvalue) + "% - On a success: "
+ str(fixed_value) + "%"))
(print("Real chance of getting " + str(skill_floor) + " skill points or more: " + str(fixed_realskill)
+ "% - On a success: " + str(fixed_skill) + "%"))
print("Highest crit streak was " + str(crit_streak) + " and highest damage was " + str(max_damage) + "!")