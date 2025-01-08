"""get data from aoc

find your AoC session from your cookies (I hit f12 and go to Application > Cookies)
"""

from datetime import datetime, timedelta, timezone
from math import floor
from pathlib import Path
from aocd import get_data

working_day = 7 #current_day()

AOC_TZ = tz=timezone(timedelta(hours=-5))
aoc_now = datetime.now(tz=AOC_TZ)

def current_day():
    """
    Most recent day, if it's during the Advent of Code. Happy Holidays!
    Day 1 is assumed, otherwise.
    """
    day = min(aoc_now.day, 25)
    return day

def count_down():
    """time until next day drops
        returns:
            countdown:          datetime.timedelta(seconds, microseconds)
            countdown string    hours, mins
            mytime              datetime.time(hours, mins, ...)
    """
    aoc_next = datetime(2023, 12, current_day()+1, tzinfo=AOC_TZ)

    _countdown = aoc_next - aoc_now
    hours = floor(_countdown.seconds / 3600)
    mins = floor(_countdown.seconds / 60) - hours*60
    mytime_raw = (datetime.now() + _countdown).time()
    mytime = mytime_raw.strftime("%H:%M:%S")

    return _countdown, f"{hours} hours, {mins} mins", mytime


SAVE_LOC = Path(r"C:\Users\ElizabethEyers\Documents\Advent of Code\2024\data")

input_data = get_data(session="53616c7465645f5f64d5057c811ce5fc28ad3418e5deafdf06c7c6926f34ecd8015578c505cb0038b640d8511adcb595bd66e2a3cbac919aa2db7e1f8e8885a8"
                      , day = working_day)

with open(SAVE_LOC / f"day{working_day}.txt", "w") as file:
    file.write(input_data)

countdown, countdown_str, deadline = count_down()

print("\n"f"{'='*30}")
print('Day',current_day(), 'ends at:', deadline, '\nYou have', countdown_str)
print('You are working on Day', working_day)
print("="*30, '\n')

