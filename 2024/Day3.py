""" Day 3
https://adventofcode.com/2024/day/3

Part I
For example, consider the following section of corrupted memory:
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

Only the four highlighted sections are real mul instructions.
mul(2,4)
mul(5,5)
mul(11,8)
mul(8,5)

Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions.
What do you get if you add up all of the results of the multiplications?


Part II
There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions


Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

This corrupted memory is similar to the example from before
, but this time the mul(5,5) and mul(11,8) instructions are disabled
because there is a don't()instruction before them. T
he other mul instructions function normally
, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

"""

import re

from get_data import countdown_str, deadline, SAVE_LOC

print(countdown_str)
print(deadline)

day = 3 #current_day()
cache_loc = SAVE_LOC / f"day{day}.txt"
with open(cache_loc, "r") as file:
    daily_input = file.read()
    # df = pd.read_csv(cache_loc, header=None, sep=" ")
daily_input

example = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

pattern = "mul\(\d{1,3},\d{1,3}\)"


def decode(string):
    return sum([(int(xy[0])*int(xy[1])) for xy in [re.findall("\d{1,3}",mul) for mul in re.findall("mul\(\d{1,3},\d{1,3}\)", string)]])


################################
######### Part II ##############
################################

example = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

example[::-1]

data = daily_input

x = 0
dont = data.split("don't()")

x+=decode(dont[0])
x+=decode(''.join([''.join(good) for good in [do[1:] for do in [do.split("do()") for do in dont[1:]]]]))
x