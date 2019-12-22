import math
import os
import sys

# raw_input = open(os.path.join(sys.path[0], 'input_test_1_2_35')).read()
# raw_input = open(os.path.join(sys.path[0], 'input_test_5_8_33')).read()
# raw_input = open(os.path.join(sys.path[0], 'input_test_3_4')).read()
# raw_input = open(os.path.join(sys.path[0], 'input_test_8_3')).read()
raw_input = open(os.path.join(sys.path[0], 'input')).read()
station_location = (26, 28)

# raw_input = open(os.path.join(sys.path[0], 'input_test_11_13_210')).read()
# station_location = (11,13)

map = []

for map_row in raw_input.split('\n'):
    map.append(list(map_row))


asteroid_locations = set()


for y, map_row in enumerate(map):
    for x, item in enumerate(map_row):
        if item != '.':
            asteroid_locations.add((x, y))



asteroid_by_direction = {}
for asteroid in asteroid_locations:
    if asteroid == station_location:
        continue

    direction_x = asteroid[0] - station_location[0]
    direction_y = asteroid[1] - station_location[1]
    direction_gcd = math.gcd(direction_x, direction_y)
    direction_x /= direction_gcd
    direction_y /= direction_gcd

    if (direction_x, direction_y) not in asteroid_by_direction:
        asteroid_by_direction[(direction_x, direction_y)] = []

    asteroid_by_direction[(direction_x, direction_y)].append((asteroid[0], asteroid[1]))


def degree_from_y_axis(vector):
    x = vector[0]
    y = -vector[1]

    propper_rads = math.atan2(y, x)
    if x >= 0 and y >= 0:
        # 1 quadrant
        return propper_rads + (math.pi * (3/2))
    if x >= 0 and y < 0:
        # 4 quadrant
        return propper_rads + (math.pi * (3/2))
    if x <= 0 and y <= 0:
        # 3 quadrant
        return propper_rads + (math.pi * (3/2))
    if x < 0 and y > 0:
        # 2 quadrant
        return propper_rads - (math.pi * (1/2))


asteroid_by_direction_sorted = sorted(asteroid_by_direction.items(), key= lambda asteroid: -degree_from_y_axis(asteroid[0]) ) 
asteroids_ordered_by_distance = list()
for direction, asteroids in asteroid_by_direction_sorted:
    asteroids_ordered_by_distance.append( sorted(asteroids, key=lambda pos: ((pos[0] - station_location[0]) ** 2) + ((pos[1] - station_location[1]) ** 2) ) )

counter = 0

direction_index = 0
destructed = {}
while True:
    asteroids_in_direction = asteroids_ordered_by_distance[direction_index]
    if len(asteroids_in_direction) != 0:
        counter += 1
        asteroid = asteroids_in_direction.pop(0)
        destructed[counter] = asteroid
        if counter == 200:
            print(asteroid)
            break
    direction_index = (direction_index + 1) % len(asteroid_by_direction_sorted)

print(destructed)

