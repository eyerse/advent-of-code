""" Day 5
https://adventofcode.com/2024/day/4

Part I

The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.

For example:

47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47


The first section specifies the page ordering rules, one per line.
The first rule, 47|53, means that if an update includes both page number 47 and page number 53
, then page number 47 must be printed at some point before page number 53.
(47 doesn't necessarily need to be immediately before 53;
other pages are allowed to be between them.)

The second section specifies the page numbers of each update.

In the above example, the first update (75,47,61,53,29) is in the right order:

75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
53 is correctly fourth because it is before page number 29 (53|29).
29 is the only page left and so is correctly last.

The second and third updates are also in the correct order according to the rules.
Like the first update, they also do not include every page number


For some reason, the Elves also need to know the middle page number of each update being printed.
Because you are currently only printing the correctly-ordered updates
, you will need to find the middle page number of each correctly-ordered update.
In the above example, the correctly-ordered updates are:

75,47,61,53,29
97,61,53,29,13
75,29,13

These have middle page numbers of 61, 53, and 29 respectively.
Adding these page numbers together gives 143.

Determine which updates are already in the correct order.
What do you get if you add up the middle page number from those correctly-ordered updates?

"""

import re
import pandas as pd
import numpy as np

from get_data import countdown_str, deadline, SAVE_LOC, current_day

print(countdown_str)
print(deadline)

day = 5 #current_day()
cache_loc = SAVE_LOC / f"day{day}.txt"
with open(cache_loc, "r") as file:
    daily_input = file.read()
    # df = pd.read_csv(cache_loc, header=None, sep=" ")

example = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

puzzle_input = example

def check_updates(puzzle_input):
    order, pages = [pinput.split('\n') for pinput in puzzle_input.split('\n\n')]
    order = pd.DataFrame([row.split('|') for row in order]).sort_values(by=[0,1]).reset_index(drop=True)
    pages = pd.DataFrame([update.split(',') for update in pages])
    def check_pages(update: pd.Series):
        comp = order.merge(update.to_frame('page').reset_index(), how='inner', left_on=0, right_on='page').merge(update.to_frame('page').reset_index(), how='inner', left_on=1, right_on='page')
        return min(comp.index_x < comp.index_y)
    return pages[pages.apply(check_pages, axis=1)]


def solve_day_five(puzzle_input):
    return check_updates(puzzle_input).apply(lambda x: x[(x.dropna().count())/2 -0.5] , axis=1).astype(int).sum()

#########################
###### Part II ##########
#########################

def check_updates_ii(puzzle_input):
    order, pages = [pinput.split('\n') for pinput in puzzle_input.split('\n\n')]
    order = pd.DataFrame([row.split('|') for row in order]).sort_values(by=[0,1]).reset_index(drop=True)
    pages = pd.DataFrame([update.split(',') for update in pages])
    def check_pages(update: pd.Series):
        comp = order.merge(update.to_frame('page').reset_index(), how='inner', left_on=0, right_on='page').merge(update.to_frame('page').reset_index(), how='inner', left_on=1, right_on='page')
        return min(comp.index_x < comp.index_y)
    pages['ordered'] = pages.apply(check_pages, axis=1)
    return pages[~pages.apply(check_pages, axis=1)]

def index_swaps(idxa: int, idxb: int, ser: pd.Series):
    ser[idxa], ser[idxb] = ser[idxb], ser[idxa]

def reorder_updates(update: pd.Series, order):
    comp = order.merge(update.to_frame('page').reset_index(), how='inner', left_on=0, right_on='page').merge(update.to_frame('page').reset_index(), how='inner', left_on=1, right_on='page')
    swaps = comp[~(comp.index_x < comp.index_y)][['index_x', 'index_y']]
    if swaps.shape[0] > 0:
        index_swaps(swaps.iloc[0,0], swaps.iloc[0,1], update)
        if swaps.shape[0] > 1:
            reorder_updates(update, order)
    return int(update[(update.dropna().count())/2 -0.5])


def solve_day_five_ii(puzzle_input):
    order = pd.DataFrame([row.split('|') for row in puzzle_input.split('\n\n')[0].split('\n')]).sort_values(by=[0,1]).reset_index(drop=True)
    new_order = check_updates_ii(puzzle_input).drop(columns='ordered')
    middle = new_order.apply(reorder_updates, order=order, axis=1)
    return middle.sum()

solve_day_five_ii(example)

solve_day_five_ii(daily_input)




