""" Day 1
https://adventofcode.com/2023/day/1

On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

"""

import pandas as pd
from get_data import countdown_str, deadline, SAVE_LOC

print(countdown_str)
print(deadline)

day = 1 #current_day()
cache_loc = SAVE_LOC / f"day{day}.txt"
with open(cache_loc, "r") as file:
    daily_input = file.read()


inputURL = "https://adventofcode.com/2023/day/1/input"

col = f"day{day}"

def get_bookends(mylist):
    if len(mylist) > 0:
        return mylist[0], mylist[-1]
    return None

def get_first(mylist):
    if len(mylist) > 0:
        return mylist[0]
    return None

def get_nonna(mytuple):
    if mytuple is not None:
        return [x for x in mytuple if x != ''][0]
    return None


def get_loc(digit:str, string:str):
    return string.find(digit)

data = pd.read_csv(cache_loc, header=None).rename(columns={0:col})

data['intF'] = data[col].str.findall('(\d)').apply(get_bookends).apply(lambda x: x[0])
data['intL'] = data[col].str.findall('(\d)').apply(get_bookends).apply(lambda x: x[1])
#data['SumD'] = (data['intF'] + data['intL']).astype(int)
#answer = (data['intF'] + data['intL']).astype(int).sum()
#


#https://adventofcode.com/2023/day/1#part2

nums = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
smun = [num[::-1] for num in nums]

nums_pat = "|".join([f"({num})" for num in nums])
smun_pat = "|".join([f"({smu})" for smu in smun])

data.head()

data["1yad"] = data["day1"].str[::-1]

data['numF'] = data[col].str.findall(nums_pat).apply(get_first).apply(get_nonna)
data['numL'] = data["1yad"].str.findall(smun_pat).apply(get_first).apply(get_nonna)

data['intFloc'] = data.apply(lambda row: row['day1'].find(row['intF']), axis=1)
data['intLloc'] = data.apply(lambda row: row['1yad'].find(row['intL']), axis=1)

data['numFloc'] = data.apply(lambda row: row['day1'].find(row['numF']) if row['numF'] is not None else None, axis=1)
data['numLloc'] = data.apply(lambda row: row['1yad'].find(row['numL']) if row['numL'] is not None else None, axis=1)

data['F'] = data.apply(lambda row: row[row[['intFloc', 'numFloc']].idxmin()[:3] + "F"], axis=1)
data['L'] = data.apply(lambda row: row[row[['intLloc', 'numLloc']].idxmin()[:3] + "L"], axis=1)


numdict = {num: d+1 for d, num in enumerate(nums)} |  {num: d+1 for d, num in enumerate(smun)}

data['F'] = data['F'].map(numdict).fillna(data['F']).astype(int).astype(str)
data['L'] = data['L'].map(numdict).fillna(data['L']).astype(int).astype(str)
data['Summm'] = data['F'] + data['L']

data[[col,'Summm']].sample(10)

answer = data['Summm'].astype(int).sum()

print(answer)


