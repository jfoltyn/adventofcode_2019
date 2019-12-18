import math
import os
import sys

# raw_input = open(os.path.join(sys.path[0], 'input_test_1_2_35')).read()
# raw_input = open(os.path.join(sys.path[0], 'input_test_5_8_33')).read()
raw_input = open(os.path.join(sys.path[0], 'input')).read()


map = []

for map_row in raw_input.split('\n'):
    map.append(list(map_row))


asteroid_locations = {}


for y, map_row in enumerate(map):
    for x, item in enumerate(map_row):
        if item == '#':
            asteroid_locations[(x, y)] = set()


for asteroid in asteroid_locations.keys():
    for other_asteroid in asteroid_locations.keys():
        if asteroid == other_asteroid:
            continue

        direction_x = other_asteroid[0] - asteroid[0]
        direction_y = other_asteroid[1] - asteroid[1]
        direction_gcd = math.gcd(direction_x, direction_y)

        direction_x /= direction_gcd
        direction_y /= direction_gcd

        asteroid_locations[asteroid].add((direction_x, direction_y))


best_asteroid = max(asteroid_locations.items(), key=lambda asteroid: len(asteroid[1]))
print(best_asteroid[0])
print(len(best_asteroid[1]))