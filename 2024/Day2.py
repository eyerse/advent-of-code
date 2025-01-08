""" Day 2
https://adventofcode.com/2024/day/2

Part I

This example data contains six reports each containing five levels
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9

So, a report only counts as safe if both of the following are true:

- The levels are either all increasing or all decreasing.
- Any two adjacent levels differ by at least one and at most three.



In the example list above, the pairs and distances would be as follows:
7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.

Analyze the unusual data from the engineers. How many reports are safe?


Part II

safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!


"""

import pandas as pd
import numpy as np
from get_data import countdown_str, deadline, SAVE_LOC

print(countdown_str)
print(deadline)

day = 2 #current_day()
cache_loc = SAVE_LOC / f"day{day}.txt"
with open(cache_loc, "r") as file:
    # daily_input = file.read()
    df = pd.read_csv(cache_loc, header=None, sep=" ")

example = pd.DataFrame([row.split(' ') for row in """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""".split('\n')]).astype(int)


df1 = df[(df.diff(axis=1).abs().max(axis=1) < 4)].copy()
df2 = df1[(df1.diff(axis=1).abs().min(axis=1) > 0)].copy()
df3 = df2[~((df2.diff(axis=1).min(axis=1) < 0) & (df2.diff(axis=1).max(axis=1) > 0))]

df[(df.diff(axis=1).abs().max(axis=1) < 4) & (df.diff(axis=1).abs().min(axis=1) > 0) & ~((df.diff(axis=1).min(axis=1) < 0) & (df.diff(axis=1).max(axis=1) > 0))]



################################
######### Part II ##############
################################

# max diff is 3
# min diff is 1
# diff has same polarity

og_df = df
# df = example
# safe reports from part I
def safe_levels(df):
    return df[(df.diff(axis=1).abs().max(axis=1) < 4) & (df.diff(axis=1).abs().min(axis=1) > 0) & ~((df.diff(axis=1).min(axis=1) < 0) & (df.diff(axis=1).max(axis=1) > 0))]

def justify(df):
    return df.apply(lambda x: pd.Series(sorted(x, key=pd.isnull)), 1, )

safe = safe_levels(df)

safe_set = set(safe.index) # 663

# bad reports from part I
b0 = df.drop(index=safe.index)


############# test first criteria ##############
# min diff is 1
# drop rhs duplicate
# find rows with only one duplicate level
m1 = (b0.diff(axis=1)[b0.diff(axis=1)==0].apply(pd.notna, axis=1).sum(axis=1) ==1)

# drop rhs duplicate
m1r = b0[m1].mask(b0[m1].diff(axis=1) == 0, pd.NA)

pass_1a = safe_levels(justify(m1r))
safe_set = safe_set.union(pass_1a.index)
print(len(safe_set))

# drop lhs duplicate
m1l = b0[m1].mask(b0[m1].diff(periods=-1, axis=1) == 0, pd.NA)
pass_1b = safe_levels(justify(m1r))
safe_set = safe_set.union(pass_1b.index)
print(len(safe_set))

# bad reports from part1 and fail min diff 1 removal
b1 = df.drop(index=safe_set)


############# test second criteria ##############
# max diff is 3
# find rows with only one failed level
m2 = b1.diff(axis=1)[b1.diff(axis=1).abs()>3].apply(pd.notna, axis=1).sum(axis=1) ==1
b1[m2]

# drop rhs fail
m2r = b1[m2].mask(b1[m2].diff(axis=1).abs() > 3, pd.NA)
pass_2a = safe_levels(justify(m2r))
safe_set = safe_set.union(pass_2a.index)
print(len(safe_set))

# drop lhs fail
m2l = b1[m2].mask(b1[m2].diff(periods=-1, axis=1).abs() > 3, pd.NA)
pass_2b = safe_levels(justify(m2l))

safe_set = safe_set.union(pass_2b.index)
print(len(safe_set))


# bad reports from part1 and fail min diff 1 removal and max diff 3 removal
b2 = df.drop(index=safe_set)


############# test third criteria ##############
# diff has same polarity

# find rows with only two failed pairs
b2p = b2[(b2.diff(axis=1).min(axis=1) < 0) & (b2.diff(axis=1).max(axis=1)>0)].copy()
m3 = b2p.diff(axis=1).apply(np.sign).apply(pd.value_counts, axis=1)[[-1,1]].min(axis=1) == 1
b2p.loc[m3]

b2p.loc[m3].diff(axis=1)

# drop wrong polarity rhs
polr= b2p.loc[m3].diff(axis=1).apply(np.sign).apply(pd.value_counts, axis=1)[[-1,1]].idxmin(axis=1)
m3pr = b2p.loc[m3].mask(np.sign(b2p.loc[m3].diff(axis=1)).eq(polr, axis='index'), pd.NA)
pass_3a = justify(m3pr)
safe_set = safe_set.union(safe_levels(pass_3a).index)
print(len(safe_set))

# drop wrong polarity lhs
poll= b2p.loc[m3].diff(periods=-1, axis=1).apply(np.sign).apply(pd.value_counts, axis=1)[[-1,1]].idxmin(axis=1)
m3pl = b2p.loc[m3].mask(np.sign(b2p.loc[m3].diff(axis=1, periods=-1)).eq(poll, axis='index'), pd.NA)
pass_3b = justify(m3pl)
safe_set = safe_set.union(safe_levels(pass_3b).index)
print(len(safe_set))


df.loc[list(safe_set)]



# 722 too high