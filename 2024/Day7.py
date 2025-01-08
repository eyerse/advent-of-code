""" Day 7
https://adventofcode.com/2024/day/7

Part I

Each line represents a single equation.
The test value appears before the colon on each line;
it is your job to determine whether the remaining numbers
can be combined with operators to produce the test value.

Operators are always evaluated left-to-right
, not according to precedence rules. Furthermore
, numbers in the equations cannot be rearranged.
Glancing into the jungle, you can see elephants
holding two different types of operators
: add (+) and multiply (*).


190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20



Only three of the above equations can be made true by inserting operators:

190: 10 19 has only one position that accepts an operator: between 10 and 19.
    Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
3267: 81 40 27 has two positions for operators.
    Of the four possible configurations of the operators
    , two cause the right side to match the test value:
    81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.
    The engineers just need the total calibration result
    , which is the sum of the test values from just the equations that could possibly be true.
    In the above example, the sum of the test values for the three equations listed above is 3749.

Part II

"""

import re
import pandas as pd
import numpy as np
import itertools
from itertools import combinations, chain

from get_data import SAVE_LOC, working_day

# working_day = 'N'

cache_loc = SAVE_LOC / f"day{working_day}.txt"
with open(cache_loc, "r") as file:
    daily_input = file.read()
    # df = pd.read_csv(cache_loc, header=None, sep=" ")

example = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def format_input(puzzle_input: str):
    puzzle = pd.DataFrame([calc.split(': ') for calc in puzzle_input.split('\n')]).rename(columns={0:'test'}).set_index('test')
    puzzle.index = puzzle.index.astype(int)
    puzzle = puzzle[1].str.split(' ', expand=True).astype(float)
    return puzzle


## think odd x even?
# o+o = e
# e+e = e
# o+e = o

# o*o = o
# e*e = e
# e*o = e


def is_even(val):
    if np.isnan(val):
        return None
    return val % 2 == 0

def convert_to_mod_2(val):
    return int(val % 2)

def split_list(data, n):
    "return all combinations which split a list into n partitions"
    for splits in combinations(range(1, len(data)), n-1):
        result = []
        prev = None
        for split in chain(splits, [None]):
            result.append(data[prev:split])
            prev = split
        yield result

def combine_partition(elements: list):
    "combine partitioned array"
    

def is_even_possible(ser: pd.Series):
    # e+e o+e
    # e*o e*e
    n = ser.size
    oes = ser.apply(convert_to_mod_2)
    for i in range(2, n):
        splits = split_list(oes.values, i)
        for split in splits:

    return True


def check_even(ser: pd.Series, target: float):
    pass

def check_odd(ser: pd.Series, target: float):
    pass


def is_odd_possible(ser: pd.Series):
    # e+o
    # o*o
    oes = ser.apply(convert_to_mod_2)
    return True

def check_row(ser: pd.Series):
    ser = ser.dropna()
    target = ser.name
    if is_even(target):
        if is_even_possible(ser):
            return check_even(ser, target)
        else:
            return False
    if is_odd_possible(ser):
        return check_odd(ser, target)
    else:
        return False


def solve_day_seven(puzzle_input):
    puzzle = format_input(puzzle_input)
    checked = puzzle.apply(check_row, axis=1)
    return checked


solve_day_seven(example)
solve_day_seven(daily_input)


def binomial_expansion(ser: pd.Series):
    ser = ser.dropna()
    i = 2
    n = ser.size
    target = ser.name
    if ser.product() == target:
        return True
    if ser.sum() == target:
        return True
    s1 = ser.iloc[:i]
    s2 = ser.iloc[i:]
    test = s1.sum()

    # one partition
    while (not s2.empty):
        test = s1.sum() * s2.product()
        if test == target:
            return True
        test = s1.sum() + s2.product()
        if test == target:
            return True
        test = s1.product() * s2.sum()
        if test == target:
            return True
        test = s1.product() + s2.sum()
        if test == target:
            return True
        i += 1
        s1 = ser.iloc[:i]
        s2 = ser.iloc[i:]
    i = 2
    j = 3
    s1 = ser.iloc[:i]
    s2 = ser.iloc[i:j]
    s3 = ser.iloc[j:]
    test = s1.sum()
    # two partitions
    while (not s3.empty):
        test = s1.product() + s2.sum() * s3.product()
        if test == target:
            return True
        test = s1.product() * s2.sum() * s3.product()
        if test == target:
            return True
        test = s1.product() * s2.sum() + s3.product()
        if test == target:
            return True

        test = s1.sum() + s2.product() * s3.sum()
        if test == target:
            return True
        test = s1.sum() * s2.product() * s3.sum()
        if test == target:
            return True
        test = s1.sum() * s2.product() + s3.sum()
        if test == target:
            return True

        i += 1
        s1 = ser.iloc[:i]
        s2 = ser.iloc[i:]


    return False


print('\n')
