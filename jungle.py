import random
import os
import copy
from colorama import init, Fore, Back, Style

init()

symbols = (
    ('F', Fore.WHITE+Back.RED,   0), # Fire
    ('T', Fore.WHITE+Back.GREEN, 0), # Tree
    ('A', Back.BLACK,            0), # Ash
    ('W', Back.BLUE,             0), # Watter
    ('G', Back.GREEN,            0), # Grass
)

def get_symbol(elem) -> list:
    if elem == 'S':
        return ['S', Fore.BLACK+Back.LIGHTBLACK_EX, 0]
    return list(next(t for t in symbols if t[0] == elem))

def create_jungle(n) -> list:
    null_symbol = ('N', Fore.BLUE+Back.BLACK, 0)
    jungle = [[null_symbol for _ in range(n+2)]]
    for _ in range(n):
        row = [null_symbol]
        for _ in range(n):
            row.append(list(random.choice(symbols)))
        row.append(null_symbol)
        jungle.append(row)
    jungle.append([null_symbol for _ in range(n+2)])
    # change random set stone
    for _ in range(random.randint(1, 5)):
        jungle[random.randint(1, len(jungle)-2)][random.randint(1, len(jungle)-2)] = get_symbol('S')
    return jungle

def show_jungle(jungle):
    for i, row in enumerate(jungle[0: len(jungle)]):
        for j, symbol in enumerate(row[0: len(row)]):
            print(f"{symbol[1]} {symbol[0]} {Style.RESET_ALL}", end='')
        print()

def is_near(i, j, elem, total=False) -> bool:
    check_list = []
    check_list.append(elem == jungle[i+1][j][0])
    check_list.append(elem == jungle[i-1][j][0])
    check_list.append(elem == jungle[i][j+1][0])
    check_list.append(elem == jungle[i][j-1][0])

    len_right = check_list.count(True)
    index_limit = len(jungle) - 2

    if total:
        if (i == 1 and j == 1) or (i == 1 and j == index_limit) or (i == index_limit and j == index_limit) or (i == index_limit and j == 1):
            return len_right == 2
        elif i == 1 or j == 1 or i == index_limit or j == index_limit:
            return len_right == 3
        else:
            return len_right == 4
    else:
        return len_right
    

def new_jungle(jungle) -> list:
    new_jungle = copy.deepcopy(jungle)
    for i in range(1, len(jungle)-1):
        for j in range(1, len(jungle)-1):
            symbol = jungle[i][j]
            elem = symbol[0]
            year = symbol[2]

            # plus year
            new_jungle[i][j][2] += 1

            # zero year
            if is_near(i, j, elem):
                new_jungle[i][j][2] = 0

            # check limit year
            if year >= 3 :
                if elem == 'F':
                    new_jungle[i][j] = get_symbol('A')
                elif elem != 'S':
                    new_jungle[i][j] = get_symbol('G')
            # stone year limit
            if year >= 10 and elem == 'S':
                new_jungle[i][j] = get_symbol('G')
            # check
            if elem == 'F': # Fire
                if is_near(i, j, 'W') or is_near(i, j, 'S', True) or is_near(i, j, 'G', True) or is_near(i, j, 'T'):
                    new_jungle[i][j] = get_symbol('A')
            elif elem == 'A': # Ash
                new_jungle[i][j] = get_symbol('G')
            elif elem == 'T': # Tree
                if is_near(i, j, 'W'):
                    new_jungle[i][j][2] = 0
                if is_near(i, j, 'F'):
                    new_jungle[i][j] = get_symbol('F')
            elif elem == 'W': #watter
                if is_near(i, j, 'F'):
                    new_jungle[i][j] = get_symbol('A')
            elif elem == 'G': # Grass
                n_tree  = is_near(i, j, 'T')
                n_water = is_near(i, j, 'W')
                n_fire  = is_near(i, j, 'F')
                if n_tree > n_water and n_tree > n_fire:
                    new_jungle[i][j] = get_symbol('T')
                elif n_water > n_tree and n_water > n_fire:
                    new_jungle[i][j] = get_symbol('W')
                elif n_fire > n_water and n_fire > n_tree:
                    new_jungle[i][j] = get_symbol('F')
                elif n_tree and n_water and n_fire:
                    new_jungle[i][j] = get_symbol(random.choice(['T', 'W', 'F']))
    return new_jungle

# main
jungle = create_jungle(10)

while True:
    # os.system("clear")
    show_jungle(jungle)
    jungle = new_jungle(jungle)
    print("""
    1 - add water
    2 - add fire
    3 - add grass
    4 - add stone""")
    limit = len(jungle) - 2
    while True:
        select = input("selcet add : ")
        if select.isdecimal():
            select = int(select)
            if 1 <= select <= 4:
                for _ in range(random.randint(1, 10)):
                    jungle[random.randint(1, limit)][random.randint(1, limit)] = get_symbol('W' if select == 1 else 'F' if select == 2 else 'G' if select == 3 else 'S')
                break
        elif not select:
            break