'''
x x x x x x
1 1 1 1 [5-9] [5-9]
1 2 3 4 [5-9] [5-9]
'''

def meets_adjacent_condition(p):
    return ((p[0] == p[1] and p[1] != p[2]) or 
        (p[0] != p[1] and p[1] == p[2] and p[2] != p[3]) or 
        (p[1] != p[2] and p[2] == p[3] and p[3] != p[4]) or 
        (p[2] != p[3] and p[3] == p[4] and p[4] != p[5]) or 
        (p[3] != p[4] and p[4] == p[5]))

def meets_never_decrease_condition(p):
    return p[0] <= p[1] and p[1] <= p[2] and p[2] <= p[3] and p[3] <= p[4] and p[4] <= p[5]


def count_possibilities(range_start, range_end):
    criteria_met = 0
    for p in range(range_start, range_end + 1):
        str_p = str(p)

        if meets_adjacent_condition(str_p) and meets_never_decrease_condition(str_p):
            criteria_met += 1

    return criteria_met

print(count_possibilities(134564, 585159))