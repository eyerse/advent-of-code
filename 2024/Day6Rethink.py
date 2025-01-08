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
from get_data import SAVE_LOC, working_day

working_day = 6

cache_loc = SAVE_LOC / f"day{working_day}.txt"
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


#### ###################
# guard iterates around map turning 90 at obstacles
# how many distinct locations does he occupy


guard_re = re.compile('[><v^]')
obstacle_re = re.compile('[#O]')
turn_map = {'^':'>'
                            , '>':'v'
                            , 'v':'<'
                            , '<':'^'
                            }

move_map = {'^':(0, -1)
                            , '>':(1, 0)
                            , 'v':(0, 1)
                            , '<':(-1, 0)
                            }

def convert_input_to_map(puzzle_input):
    "converts input to array of strings. Returns Map"
    return puzzle_input.split('\n')

def find_guard(my_map):
    "find Guard on map. Return G position"
    x,y,d = [(j.index(i), my_map.index(j), guard_re.search(i).group(0) ) for j in my_map for i in j if guard_re.search(i) is not None][0]
    return (x,y,d)

def turn_guard(current_pos):
    "turn guard. Return new G position"
    x,y,d = current_pos
    return (x, y, turn_map[d])

def calc_dxdy_to_next_pos(d):
    "return (dx, dy) to get to next position"
    return move_map[d]

def is_outside_grid(my_map, position):
    "check if position has exited in grid. Return bool"
    x, y, d = position

    xmax = len(my_map[0]) - 1
    ymax = len(my_map) - 1

    return (x < 0) or (x > xmax) or (y < 0) or (y > ymax)

def is_obstacle(my_map, position):
    "eval position in my_map return bool if match obstacle regex. Return True if outside grid"
    x, y, d = position
    if is_outside_grid(my_map, position):
        return True
    p = my_map[y][x]

    return obstacle_re.match(p) is not None

def find_pos_where_hit_next_obstacle(my_map, current_pos, footprints = False, turning_points = Counter()):
    "scan map in direction until hit Obstacle. Return position before O. Return False if exits grid"
    x, y, d = current_pos
    dx, dy = calc_dxdy_to_next_pos(d)
    next_pos = (x+dx, y+dy, d)

    if footprints != False:
        footprints.update([current_pos])
    while not (is_obstacle(my_map, next_pos)):
        if footprints != False:
            footprints.update([next_pos])
        # print(next_pos)
        x, y, d = next_pos
        next_pos = (x+dx, y+dy, d)
    current_pos = (x, y, d)

    if is_outside_grid(my_map, next_pos):
        return False , footprints, turning_points
    turning_points.update([current_pos])
    return turn_guard(current_pos), footprints, turning_points

def patrol_guard(my_map, current_pos, footprints, turning_points):
    "move guard around grid until exits gird. Return last pos"
    while (next_turn_pos:= find_pos_where_hit_next_obstacle(my_map, current_pos, footprints, turning_points))[0] is not False:
        # print('turn to:', next_turn_pos[0])
        current_pos, footprints, turning_points = next_turn_pos
    return footprints, turning_points

def run_simulation(puzzle_input):
    "run sim. collect every footprint and every point of turn (pre turn)"
    my_map = convert_input_to_map(puzzle_input)
    current_pos = find_guard(my_map)
    footprints = Counter()
    turning_points = Counter()
    footprints, turning_points = patrol_guard(my_map, current_pos, footprints, turning_points)
    return footprints, turning_points

def solve_day_six(puzzle_input):
    "how many locations"
    footprints, turning_points = run_simulation(daily_input)
    # remove direction from counter
    distinct_locs = Counter({ k[:2]: v for k,v in footprints.items()})
    return len(distinct_locs)

# print('distinct locs:', solve_day_six(example))
# print('distinct locs:', solve_day_six(daily_input))


########################################################
# Part II
########################################################
    # You need to get the guard stuck in a loop by adding a single new obstruction.
    # How many different positions could you choose for this obstruction?
    # The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.


    #### ###################
    # any position is (x, y, d)
    # obstacles need only be on the original path
    # a loop is identified as a repeated position

def place_obstacle(my_map, position, obstacle="O"):
    "return new map with Obstacle added in position"
    x, y, *d = position
    new_map = my_map[:]
    new_map[y] = new_map[y][:x] + obstacle + new_map[y][x+1:]
    return new_map

def is_loop(turning_points: Counter):
    "test whether hit turning points before. Return bool"
    if len(turning_points) == 0:
        return False
    return turning_points.most_common(1)[0][1] > 1

def patrol_guard_with_loops(my_map, current_pos):
    "move guard around grid until exits gird or hits loop. Return is_loop"
    footprints = False
    turning_points = Counter()

    while (next_turn_pos:= find_pos_where_hit_next_obstacle(my_map, current_pos, footprints, turning_points))[0] is not False:
        # print('turn to:', next_turn_pos[0])
        current_pos, footprints, turning_points = next_turn_pos
        if is_loop(turning_points):
            break
    return is_loop(turning_points)

def count_loops(my_map, search_locs):
    "Count loops generated by placing obstacles in og path. Return loop count"
    LoopObstCounter = Counter()
    for xy, dd in search_locs.items():
        x, y = xy
        for d in dd:
            guard_pos = xy + (d,)
            dx, dy = calc_dxdy_to_next_pos(d)
            next_pos = (x+dx, y+dy, d)
            # next position might be off the map or already an obst. If so skip
            if is_obstacle(my_map, next_pos):
                continue
            # place obstacle in next position
            new_map = place_obstacle(my_map, next_pos)

            # patrol guard and capture whether loop
            if patrol_guard_with_loops(new_map, guard_pos):
                LoopObstCounter.update([next_pos[:2]])
    return len(LoopObstCounter)

def solve_day_six_ii(puzzle_input):
    footprints = run_simulation(puzzle_input)[0]
    distinct_locs = { k[:2]: [xyd[2] for xyd in footprints.keys() if xyd[:2] == k[:2]] for k,v in footprints.items()}
    my_map = convert_input_to_map(puzzle_input)
    loop_obst_pos_count = count_loops(my_map, distinct_locs)
    return loop_obst_pos_count


# # print('Found', solve_day_six_ii(example)[0], 'loops')
# print('Found', solve_day_six_ii(daily_input), 'obstacle positions that cause loops')
# print('\n')

#1798
#1918

########################omds how is it still wrong##########
# 1- putting obstacles in wrong place
# 2- calcing loops wrong


### obstacles in wrong place?
## put obstacles EVERYWHERE

def try_obstacles_EVERYWHERE(my_map, starting_pos):
    sx, sy, d = starting_pos
    ObstacleCounter = Counter()
    # iter through index and map values
    for xx, y in zip(my_map, range(len(my_map))):
        for p, x in zip(xx, range(len(xx))):
            if not ((x == sx) and (y == sy)) and (obstacle_re.match(p) is None):
                new_map = place_obstacle(my_map, (x, y))
                if patrol_guard_with_loops(new_map, starting_pos):
                    ObstacleCounter.update([(x,y)])
        # print(y, len(ObstacleCounter))
    return ObstacleCounter


def ti_day_six_ii(puzzle_input):
    my_map = convert_input_to_map(puzzle_input)
    starting_pos = find_guard(my_map)
    ObstacleCounter = try_obstacles_EVERYWHERE(my_map, starting_pos)
    return len(ObstacleCounter)

print('Method 1:')

# print('Found', ti_day_six_ii(example), 'obstacle positions that cause loops')
print('Found', ti_day_six_ii(daily_input), 'obstacle positions that cause loops')
print('\n')

### obstacles in wrong place?
## put obstacles ON PATH

def try_obstacles_on_path(my_map, starting_pos, guard_path):
    sx, sy, d = starting_pos
    ObstacleCounter = Counter()
    # iter through index and map values
    for x, y in guard_path.keys():
        p = my_map[y][x]
        if not ((x == sx) and (y == sy)) and (obstacle_re.match(p) is None):
            new_map = place_obstacle(my_map, (x, y))
            if patrol_guard_with_loops(new_map, starting_pos):
                ObstacleCounter.update([(x,y)])
    return ObstacleCounter

def tii_day_six_ii(puzzle_input):
    footprints = run_simulation(puzzle_input)[0]
    distinct_locs = { k[:2]: [xyd[2] for xyd in footprints.keys() if xyd[:2] == k[:2]] for k,v in footprints.items()}
    print('Patrol Path has', len(distinct_locs), 'distinct locations')
    my_map = convert_input_to_map(puzzle_input)
    starting_pos = find_guard(my_map)
    ObstacleCounter = try_obstacles_on_path(my_map, starting_pos, distinct_locs)
    return len(ObstacleCounter)

print('Method 2:')

# print('Found', tii_day_six_ii(example), 'obstacle positions that cause loops')
print('Found', tii_day_six_ii(daily_input), 'obstacle positions that cause loops')
print('\n')


#1719

# idek what i changed smh
## maybe I was counting og obstacles as well?