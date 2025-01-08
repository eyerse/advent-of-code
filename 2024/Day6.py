""" Day 6
https://adventofcode.com/2024/day/6

Part I

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...

The map shows the current position of the guard with ^
(to indicate the guard is currently facing up from the perspective of the map).
Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

- If there is something directly in front of you
    , turn right 90 degrees.
- Otherwise, take a step forward.

Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..


Including the guard's starting position
, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..

In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard.
How many distinct positions will the guard visit before leaving the mapped area?


Part II

You need to get the guard stuck in a loop by adding a single new obstruction.
How many different positions could you choose for this obstruction?

"""

import re
from collections import Counter
from get_data import countdown_str, deadline, SAVE_LOC, current_day

print(countdown_str)
print(deadline)

day = 6 #current_day()
cache_loc = SAVE_LOC / f"day{day}.txt"
with open(cache_loc, "r") as file:
    daily_input = file.read()
    # df = pd.read_csv(cache_loc, header=None, sep=" ")

example = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


guard=re.compile("[<>v^]")
obstacle = re.compile("[^X.<>v^]")

turn_map = {'^':'>'
                            , '>':'v'
                            , 'v':'<'
                            , '<':'^'
                            }

def find_guard(my_map):
    return [(j.index(i),my_map.index(j), guard.search(i).group(0)) for j in my_map for i in j if guard.search(i) is not None][0]

def turn_guard(d):
    return turn_map[d]

# def check_for_obstacle(p):
#     return obstacle.match(p)

# def move_to_new_pos(my_map, new_pos, x, y, d, i):
#     obstacle = check_for_obstacle(my_map[new_pos[1]][new_pos[0]])
#     if obstacle is None:
#         guard_pos = (*new_pos, d)
#         return next_step(my_map, guard_pos, i)
#     else:
#         d = turn_guard(d)
#         guard_pos = (x,y,d)
#         return next_step(my_map, guard_pos, i)


# def next_step(my_map, guard_pos, i=0):
#     x, y, d = guard_pos
#     ymax = len(my_map)-1
#     xmax = len(my_map[0])-1
#     # overwrite current position
#     if i % 100 == 0:
#         print(i)
#     if i > 500:
#         return False, my_map, guard_pos, i
#     i+=1
#     my_map[y] = my_map[y][:x] + 'X' + my_map[y][x+1:]

#     if d == '^':
#         if y == 0:
#             # exit!
#             return my_map
#         else:
#             new_pos = (x, y-1)
#             return move_to_new_pos(my_map, new_pos, x, y, d, i)
#     elif d == '>':
#         if x == xmax:
#             # exit!
#             return my_map
#         else:
#             new_pos = (x+1, y)
#             return move_to_new_pos(my_map, new_pos, x, y, d, i)
#     elif d =='<':
#         if x == 0:
#             # exit!
#             return my_map
#         else:
#             new_pos = (x-1, y)
#             return move_to_new_pos(my_map, new_pos, x, y, d, i)
#     elif d =='v':
#         if y == ymax:
#             # exit!
#             return my_map
#         else:
#             new_pos = (x, y+1)
#             return move_to_new_pos(my_map, new_pos, x, y, d, i)


# def count_X(map, X):
#     return len(re.findall(X, map))

# def batch_patrol(my_map, guard_pos, i=0, j=0):
#     output = next_step(my_map, guard_pos, i)
#     if output[0]:
#         print(j, ':', True)
#         return output
#     else:
#         print(j, ': ', output[0])
#         j+=1
#         return batch_patrol(*output[1:3],0,j)

# def solve_day_six(puzzle_input):
#     my_map= puzzle_input.split('\n')
#     guard_pos = find_guard(my_map)
#     endmap = '\n'.join(batch_patrol(my_map, guard_pos,0))
#     return count_X(endmap, 'X')


# # ans = solve_day_six(daily_input)

# # print('puzzle: ', ans)

# # print('success')


####################################
############ Part II ###############
####################################

my_obstacle = re.compile("O")

def is_loop(my_map, guard_pos):
    "Check if you've been here before (about to hit my_obstacle)"
    if my_map[guard_pos[1]][guard_pos[0]] == 'X':
        return True
    elif my_map[guard_pos[1]][guard_pos[0]] == guard_pos[2]:
        return True
    else:
        return False

def check_for_obstacle_ii(p):
    check = obstacle.match(p)
    if (check is not None):
        return True, (my_obstacle.match(p) is not None)
    else:
        return (False,)


def find_next_pos_index(my_map, guard_pos):
    "return next pos indices. If exits map return False"
    x, y, d = guard_pos
    ymax = len(my_map)-1
    xmax = len(my_map[0])-1
    if d == '^':
        if y == 0:
            # exit!
            return False
        else:
            return (x, y-1, d)
    elif d == '>':
        if x == xmax:
            # exit!
            return False
        else:
            return (x+1, y, d)
    elif d =='<':
        if x == 0:
            # exit!
            return False
        else:
            return (x-1, y, d)
    elif d =='v':
        if y == ymax:
            # exit!
            return False
        else:
            return (x, y+1, d)


def patrol_guard_ii(my_map, guard_pos, track_record, i=0):
    "Move guard around patrol looking for loops"
    x, y, d = guard_pos
    my_map[y] = my_map[y][:x] + 'X' + my_map[y][x+1:]

    if track_record.most_common(1)[0][1] > 1:
        # visited same place in same direction 4 times
        return (True,)
    # batch admin
    if i > 999:
        return False, my_map, guard_pos, track_record
    i+=1
    #move around map
        # identify next step
    next_pos = find_next_pos_index(my_map, guard_pos)
    if next_pos == False:
        # next step will exit map
        return (False,)
    else:
        #check next pos for obstacle
        obst_check = check_for_obstacle_ii(my_map[next_pos[1]][next_pos[0]])
        if obst_check[0]:
            # take next step = turn 90
            track_record.update([(x,y,turn_guard(d))])
            return patrol_guard_ii(my_map, (x,y,turn_guard(d)), track_record, i)
        else:
            # take next step
            track_record.update([next_pos])
            return patrol_guard_ii(my_map, next_pos, track_record, i)


def batch_patrol_ii(my_map, guard_pos, track_record, i=0, j=0):
    "batch patrol the grid. return is loop"
    # output[0] = is_loop()
    track_record.update([guard_pos])
    output = patrol_guard_ii(my_map, guard_pos, track_record)
    if output[0]:
        # print(j, ': loop found')
        return output[0]
    elif len(output) == 1:
        # print(j, ': loop not found')
        return output[0]
    else:
        j+=1
        return batch_patrol_ii(*output[1:3],track_record,0,j)

def test_obstacle_pos(my_map, guard_pos, obst_pos, my_obstacle = "O"):
    "does obstacle in front of guard create loop"
    my_map_test = my_map[:]

    track_record = Counter()
    # new map with obstacle
    my_map_test[obst_pos[1]] = my_map_test[obst_pos[1]][:obst_pos[0]] + my_obstacle + my_map_test[obst_pos[1]][obst_pos[0]+1:]

    next_pos = find_next_pos_index(my_map_test, (*guard_pos[:2], turn_guard(guard_pos[2])))
    # check if next pos is obstacle
    is_obst = check_for_obstacle_ii(my_map_test[next_pos[1]][next_pos[0]])[0]
    if is_obst:
        # # next pos hits obstacle - convert to my_obst
        # my_map_test[next_pos[1]] = my_map_test[next_pos[1]][:next_pos[0]] + my_obstacle + my_map_test[next_pos[1]][obst_pos[0]+2:]
        # run patrol in batches ALREADY TURNED
        is_loop = batch_patrol_ii(my_map_test, (*guard_pos[:2], turn_guard(guard_pos[2])), track_record)

    else:
        # run patrol in batches
        is_loop = batch_patrol_ii(my_map_test, guard_pos, track_record)
    if is_loop:
        is_loop
    return is_loop

def run_simulation(my_map, guard_pos, loopers = Counter(), s=0, t=0):
    "Run through a sim of a map and starting pos with object at start"
    # batch admin
    if s > 50:
        return False, my_map, guard_pos, loopers, 0, t
    s+=1

    # X marks a start already tried
    my_map[guard_pos[1]] = my_map[guard_pos[1]][:guard_pos[0]] + "X" + my_map[guard_pos[1]][guard_pos[0]+1:]

    # find next position
    next_pos = find_next_pos_index(my_map, guard_pos)

    # check next pos is still in grid
    if next_pos == False:
        # next pos exits sim
        return True, len(loopers)
    if check_for_obstacle_ii(my_map[next_pos[1]][next_pos[0]])[0]:
        # next pos hits obstacle
        return run_simulation(my_map, (*guard_pos[:2], turn_guard(guard_pos[2])), loopers, s, t)
    # does obst postion create loop
    if test_obstacle_pos(my_map, guard_pos, next_pos):
        loopers.update([next_pos[:2]])
    # try next obst position
    return run_simulation(my_map, next_pos, loopers, s, t)


def batch_simulation(my_map, guard_pos, loopers = Counter(), s=0, t=0):
    "batch run the simulation. return loop count"
    # output[0] = run finished
    print('t',t, len(loopers))
    output = run_simulation(my_map, guard_pos, loopers, s, t)
    if output[0]:
        print(t, ': all loops found')
        return output[1]
    else:
        return batch_simulation(*output[1:4], 0, t+1)


def solve_day_six_ii(puzzle_input):
    my_map= puzzle_input.split('\n')
    loops = batch_simulation(my_map, find_guard(my_map))
    return loops

print("let's go")
# print(solve_day_six_ii(example), 'loops')

import sys
sys.setrecursionlimit(int(2E9))

print(solve_day_six_ii(example), 'loops')

print(solve_day_six_ii(daily_input), 'loops')
print("full run success")

#4726
#2722
#1804
#1798
#720