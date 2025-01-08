""" Day 4
https://adventofcode.com/2024/day/4

Part I
This word search allows words to be
horizontal, vertical, diagonal, written backwards, or even overlapping other words.
It's a little unusual, though, as you don't merely need to find one instance of XMAS -
you need to find all of them.
Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....

How many times does XMAS appear?


Part II


you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

"""
import re
import pandas as pd
import numpy as np

from get_data import countdown_str, deadline, SAVE_LOC

print(countdown_str)
print(deadline)

day = 4 #current_day()
cache_loc = SAVE_LOC / f"day{day}.txt"
with open(cache_loc, "r") as file:
    daily_input = file.read()
    # df = pd.read_csv(cache_loc, header=None, sep=" ")

example = """..X...
.SAMX.
.A..A.
XMAS.S
.X...."""

e1 = """....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX"""

e2 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

def roll(ser, num, axis=0):
    return pd.Series(np.roll(ser,num,axis), ser.index)

def shift_n_keep(df, direction=1):
    sdf = pd.concat([df, pd.DataFrame(data='.',index=df.index, columns=df.columns)])
    return sdf.apply(lambda x: roll(x, direction*x.name, axis=0))

def ws_to_df(puzzle_input):
    return  pd.DataFrame(puzzle_input.split('\n'))[0].str.split('', expand=True).shift(-1, axis=1).iloc[:,:-2]

def df_to_ws(search_df):
    return  '\n'.join(search_df.apply(lambda x: ''.join(x), axis=1))


def ws_horizontal(pattern, search_string):
    return len(re.findall(pattern, search_string))

def ws_vertical(pattern, search_df):
    return search_df.apply(lambda x: ''.join(x)).apply(lambda x: len(re.findall(pattern, x))).sum()

def ws_diagonal(pattern, search_df):
    # bottom left to top right
    diag_pos = df_to_ws(shift_n_keep(search_df, 1))
    # top left to bottom right
    diag_neg = df_to_ws(shift_n_keep(search_df, -1))
    return ws_horizontal(pattern, diag_pos) + ws_horizontal(pattern, diag_neg)

def solve_day_four(puzzle_input, pattern="XMAS"):
    nrettap = pattern[::-1]
    search_df = ws_to_df(puzzle_input)
    horizontal = ws_horizontal(pattern, puzzle_input) + ws_horizontal(nrettap, puzzle_input)
    vertical = ws_vertical(pattern, search_df) + ws_vertical(nrettap, search_df)
    diagonal = ws_diagonal(pattern, search_df) + ws_diagonal(nrettap, search_df)
    total = horizontal + vertical + diagonal
    return total


solve_day_four(daily_input)



########################
###### Part II #########
########################

ee1 = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
.........."""

ee2 = e2

puzzle_input = daily_input
puzzle_width = len(puzzle_input.split('\n')[0])
pattern_param_a = puzzle_width-2
pattern_param_b = puzzle_width-1

pattern =r'(M|(S))(?=\N(\1|((?(2)M|S)))([\w.\n]{pattern_param_a})\N(A)([\w.\n]{pattern_param_b})((?(4)\1|(?(2)M|S)))\N((?(4)\3|\8)))'

pattern = r"(M|(S))(?=[^\n](\1|((?(2)M|S)))([\w.\n]{138})[^\n](A)([\w.\n]{139})((?(4)\1|(?(2)M|S)))[^\n]((?(4)\3|\8)))"

re.compile(pattern)
print(len(re.findall(pattern, daily_input)))


