""" Day N
https://adventofcode.com/2024/day/N

Part I

Part II

"""

import re
import pandas as pd
import numpy as np

from get_data import SAVE_LOC, working_day

# working_day = 'N'

cache_loc = SAVE_LOC / f"day{working_day}.txt"
with open(cache_loc, "r") as file:
    daily_input = file.read()
    # df = pd.read_csv(cache_loc, header=None, sep=" ")

example = """..X..."""


print('\n')
