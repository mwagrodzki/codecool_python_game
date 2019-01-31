import os
import random
import time


# creates empty board
def grid_maker(h, w):
    grid = [[" " for i in range(w)] for i in range(h)]
    return grid


# colors field on a board
def paint(field, shot):
    red = '\33[91m'
    green = '\33[32m'
    yellow = '\33[33m'
    blue = '\33[34m'
    violet = '\33[35m'
    hitG = '\33[102m'
    hitR = '\33[101m'
    endc = '\033[0m'

    if field == '#':
        return yellow + ' ' + field + ' ' + endc
    elif field == 'x':
        if shot:
            return hitR + ' ' + field + ' ' + endc
        else:
            return red + ' ' + field + ' ' + endc
    elif field == 'o':
        if shot:
            return hitG + ' ' + field + ' ' + endc
        else:
            return green + ' ' + field + ' ' + endc
    elif field == 'M':
        return blue + ' ' + field + ' ' + endc
    elif field == 'm':
        return violet + ' ' + field + ' ' + endc

    return ' ' + field + ' '


# prints board
def print_board(grid, x=-1, y=-1):
    print("   | A | B | C | D | E | F | G | H | I | J |")
    for i in range(0, 10):
        print("-" * 44)
        if i == 9:
            print((i + 1), end=" ")
        else:
            print((i + 1), end="  ")
        for j in range(0, 10):
            if j == 9:
                if i == x and j == y:
                    print('|' + paint(grid[i][j], True), end="|")
                else:
                    print('|' + paint(grid[i][j], False), end="|")
            else:
                if i == x and j == y:
                    print('|' + paint(grid[i][j], True), end="")
                else:
                    print('|' + paint(grid[i][j], False), end="")
        print()
    print("-" * 44)


# change board at 'A1' type coordinates by value
def change_board(grid, coordinates, value):
    # numeral alphabetical
    x, y = translate_alphabetical(coordinates)
    grid[x][y] = value


# changes 'A1' -> 0 0
def translate_alphabetical(string):
    switcher = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "G": 6,
        "H": 7,
        "I": 8,
        "J": 9
    }
    x = int(string[1:]) - 1
    y = int(switcher.get(string[0], "Invalid coordinates"))
    return x, y


# checks if part of attributes is between 0 and 9
def check_constraints(number):
    if 0 <= number <= 9:
        return True
    return False


# returns length of ship of certain type
def ship_length(shipType):
    switcher = {
        "Destroyer": 2,
        "Submarine": 3,
        "Battleship": 4,
        "Carrier": 5
    }
    return switcher.get(shipType, "Wrong Ship Type")


# checks if the ship that would be put at coordinates would touch another ship
def check_area(grid, firstX, firstY, secondX, secondY):
    if firstX > secondX:
        firstX, secondX = secondX, firstX
    if firstY > secondY:
        firstY, secondY = secondY, firstY

    for i in range(firstX - 1, secondX + 2):
        for j in range(firstY - 1, secondY + 2):
            if check_constraints(i) and check_constraints(j):
                if grid[i][j] == '#':
                    return False
    return True


# puts ship between specified coordinates, returns True if successful
def insert_ship(grid, firstX, firstY, secondX, secondY):
    if check_area(grid, firstX, firstY, secondX, secondY):
        if firstX == secondX:
            if firstY < secondY:
                for i in range(firstY, secondY + 1):
                    grid[firstX][i] = '#'
            else:
                for i in range(secondY, firstY + 1):
                    grid[firstX][i] = '#'
        elif firstY == secondY:
            if firstX < secondX:
                for i in range(firstX, secondX + 1):
                    grid[i][firstY] = '#'
            else:
                for i in range(secondX, firstX + 1):
                    grid[i][firstY] = '#'
        else:
            return False, 'Your ship cannot be placed like that'
        return True, ' '
    else:
        return False, 'Your ship cannot be placed here'


# first check of coordinates given by a player, leads to ship placement
def put_ship(grid, shipType, firstCoordinate, secondCoordinate):
    try:
        firstX, firstY = translate_alphabetical(firstCoordinate)
        secondX, secondY = translate_alphabetical(secondCoordinate)

        if not (check_constraints(firstX) and check_constraints(firstY)
                and check_constraints(secondX) and check_constraints(secondY)):
            return False, 'Please stay within the board'

    except ValueError:
        return False, 'Problem with coordinates, please use correct format (i.e. A4)'

    if firstX == secondX:
        if abs(firstY - secondY) + 1 == ship_length(shipType):
            return insert_ship(grid, firstX, firstY, secondX, secondY)
        else:
            return False, 'Ship has wrong length'
    elif firstY == secondY:
        if abs(firstX - secondX) + 1 == ship_length(shipType):
            return insert_ship(grid, firstX, firstY, secondX, secondY)
        else:
            return False, 'Ship has wrong length'
    return False, "Can't place ships diagonally"


# asks for coordinates while placement phase
def player_placement_turn(ship_list):
    errorString = ' '
    stop = ''
    ships = ship_list[:]
    while stop != 'Y':
        grid = grid_maker(10, 10)
        while 0 != len(ships):
            os.system('clear')
            print_board(grid)
            print(errorString)
            # reset - reset whole board
            first = input(
                "Enter first coordinates of the %s (length= %s): " %
                (ships[0], ship_length(
                    ships[0])))
            if first == 'reset':
                break
            second = input(
                "Enter second coordinates of the %s (length= %s): " %
                (ships[0], ship_length(
                    ships[0])))
            check, errorString = put_ship(grid, ships[0], first, second)
            if check:
                ships.pop(0)
        os.system('clear')
        print_board(grid)
        stop = input('Those are your ships. Are you sure? Y/N ')
        while stop not in ['N', 'Y']:
            stop = input('Those are your ships. Are you sure? Y/N ')
    return grid


# places ships in custom places
def generate_ship(grid):
    # Carrier
    insert_ship(grid, 0, 0, 0, 4)
    # Battleship
    insert_ship(grid, 2, 0, 2, 3)
    insert_ship(grid, 4, 0, 4, 3)
    # Submarine
    insert_ship(grid, 6, 0, 6, 2)
    insert_ship(grid, 8, 0, 8, 2)
    insert_ship(grid, 0, 9, 0, 7)
    # Destroyer
    insert_ship(grid, 2, 9, 2, 8)
    insert_ship(grid, 4, 9, 4, 8)
    insert_ship(grid, 6, 9, 6, 8)
    insert_ship(grid, 8, 9, 8, 8)

    return grid


# skip generates ships in predefined places
def placement_phase(player, ship_list):
    cheat = input(
        "Player %d placing ships \nPress enter to continue..." %
        player)
    if cheat == 'skip':
        player_grid = grid_maker(10, 10)
        player_grid = ai_placement_vM(ship_list)
    else:
        player_grid = player_placement_turn(ship_list)
    shooting_grid = grid_maker(10, 10)
    input("You have placed your ships \nPress enter to continue...")
    os.system('clear')
    return player_grid, shooting_grid


# places mines in random places on board
def generate_mines(mines, grid):
    while mines != 0:
        x = random.randrange(0, 10)
        y = random.randrange(0, 10)

        if grid[x][y] == ' ':
            x_table = [x, x - 1, x + 1, x, x]
            y_table = [y, y, y, y - 1, y + 1]
            coordinates = set(zip(x_table, y_table))

            stop = 0
            for a, b in coordinates:
                if check_constraints(a) and check_constraints(b):
                    if(str(grid[a][b]) == 'M'):
                        stop = 1
            if stop == 0:
                mines -= 1
                grid[x][y] = 'M'


# mines functionality, what happens when mine is triggered
def mine_explode(x, y, shooting_grid, enemy_grid, enemy_life):
    x_table = [x, x - 1, x + 1, x, x]
    y_table = [y, y, y, y - 1, y + 1]

    coordinates = set(zip(x_table, y_table))

    for a, b in coordinates:
        if check_constraints(a) and check_constraints(b):
            if(str(enemy_grid[a][b]) == '#'):
                shooting_grid[a][b] = 'x'
                enemy_grid[a][b] = 'x'
                enemy_life -= 1
            if(str(enemy_grid[a][b]) == ' '):
                shooting_grid[a][b] = 'o'
    if 0 > enemy_life:
        return 0
    return enemy_life


def player_shot(coordinates, shooting_grid, enemy_grid, enemy_life):
    x, y = translate_alphabetical(coordinates)
    if(str(enemy_grid[x][y]) == '#'):
        shooting_grid[x][y] = 'x'
        enemy_grid[x][y] = 'x'
        enemy_life -= 1
    if(str(enemy_grid[x][y]) == ' '):
        shooting_grid[x][y] = 'o'
        enemy_grid[x][y] = 'o'
    if(str(enemy_grid[x][y]) == 'M'):
        shooting_grid[x][y] = 'm'
        enemy_grid[x][y] = 'm'
        return mine_explode(x, y, shooting_grid, enemy_grid, enemy_life)
    return enemy_life


def player_turn(ammo_number, shooting_grid, enemy_grid, enemy_life):
    errorString = ' '
    print_board(shooting_grid)
    while ammo_number > 0:
        ammo_number -= 1
        stop = ''
        while stop != 'Y':
            try:
                print(errorString)
                coordinates = input("where should I shoot? ")
                if coordinates == 'cheat':
                    return 0
                x, y = translate_alphabetical(coordinates)
                if check_constraints(x) and check_constraints(y):
                    errorString = ' '
                    stop = 'Y'
                else:
                    errorString = 'Please stay within the board'
            except ValueError:
                errorString = 'Problem with coordinates, please use correct format (i.e. A4)'
        enemy_life = player_shot(
            coordinates,
            shooting_grid,
            enemy_grid,
            enemy_life)
        print_board(shooting_grid)
        if enemy_life == 0:
            return 0
        print("Remaining bullets: %d" % ammo_number)
    return enemy_life


# pirate mode mechanic
def pirate_shot(grid, player_life):
    shot = 1
    while shot != 0:
        x = random.randrange(0, 10)
        y = random.randrange(0, 10)

        if grid[x][y] not in ['x', 'o']:
            if(grid[x][y] == '#'):
                grid[x][y] = 'x'
                player_life -= 1
            if(grid[x][y] == ' '):
                grid[x][y] = 'o'
            shot -= 1
    return player_life


# random ship placement
def ai_placement_vM(ship_list):
    grid = grid_maker(10, 10)
    ships = ship_list[:]
    counter = 0
    while len(ships) > 0:
        x = random.randrange(0, 10)
        y = random.randrange(0, 10)
        direction = ['left', 'right', 'up', 'down']
        while len(direction) > 0:
            choice = random.choice(direction)
            a, b = x, y
            if choice == 'left':
                a -= ship_length(ships[0]) - 1
            elif choice == 'right':
                a += ship_length(ships[0]) - 1
            elif choice == 'up':
                b -= ship_length(ships[0]) - 1
            elif choice == 'down':
                b += ship_length(ships[0]) - 1
            if check_constraints(a) and check_constraints(b):
                check = check_area(grid, x, y, a, b)
            else:
                check = False
            if not check:
                direction.remove(choice)
            else:
                insert_ship(grid, x, y, a, b)
                del ships[0]
                counter = 0
                break
        if len(direction) == 0:
            counter += 1
        if counter == 20:
            grid = grid_maker(10, 10)
            ships = ship_list[:]
            counter = 0
    return grid


# ai checks area, remembers possible other coordinates of the hit ship and
# marks fields where ship cannot be
def ai_area_check(possibilities, grid, x, y):
    for k in [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]:
        i, j = k
        if check_constraints(i) and check_constraints(j):
            grid[i][j] = 'o'
            if k in possibilities:
                possibilities.remove(k)
    for k in [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]:
        i, j = k
        if check_constraints(i) and check_constraints(j):
            if grid[i][j] == ' ':
                possibilities.append((i, j))

    return possibilities, grid


def ai_shoot_vM(possible_shots, ammo_number,
                shooting_grid, enemy_grid, enemy_life):
    while ammo_number != 0:
        x = random.randrange(0, 10)
        y = random.randrange(0, 10)
        if len(possible_shots) > 0:
            x = possible_shots[0][0]
            y = possible_shots[0][1]
            del possible_shots[0]

        if enemy_grid[x][y] not in ['x', 'o']:
            if(enemy_grid[x][y] == '#'):
                enemy_grid[x][y] = 'x'
                shooting_grid[x][y] = 'x'
                enemy_life -= 1
                possible_shots, shooting_grid = ai_area_check(
                    possible_shots, shooting_grid, x, y)
            if(enemy_grid[x][y] == ' '):
                enemy_grid[x][y] = 'o'
                shooting_grid[x][y] = 'o'
            ammo_number -= 1
            os.system('clear')
            print("Remaining bullets: %d" % (ammo_number + 1))
            print_board(enemy_grid, x, y)
            time.sleep(1)

    return enemy_life


def main():
    player1_life = 30
    player2_life = 30
    ammunition = 3
    mines_number = 5
    mode_pirates = False

    possible_shots = []
    ships = [
        'Carrier',
        'Battleship',
        'Battleship',
        'Submarine',
        'Submarine',
        'Submarine',
        'Destroyer',
        'Destroyer',
        'Destroyer',
        'Destroyer']

    print("  \n  \n  \n  ")
    print("Legend:\n#-your ship\no-missed shot\nx-hit shot and your ship hit\nM-active mine\nm-destroyed mine\nships have to be played at least 1 tile further\nyou have 3 shots every turn")
    print("  \n  \n  \n  ")

    pv_mode = ''
    while pv_mode == '':
        pv_mode = input("Would you like to play vs player or ai? ")
        if pv_mode not in ['player', 'ai']:
            pv_mode = ''

    if pv_mode == 'player':
        game_mode = ''
        while game_mode == '':
            game_mode = input("What mode (normal/mines/pirates)? ")
            if game_mode not in ['normal', 'mines', 'pirates']:
                game_mode = ''
        player1, player1_shooting = placement_phase(1, ships)
        player2, player2_shooting = placement_phase(2, ships)
        if game_mode == 'mines':
            generate_mines(mines_number, player1)
            generate_mines(mines_number, player2)
        elif game_mode == 'pirates':
            mode_pirates = True
    elif pv_mode == 'ai':
        player1, player1_shooting = placement_phase(1, ships)
        player2 = ai_placement_vM(ships)
        player2_shooting = grid_maker(10, 10)

    turn = 0
    while (player1_life > 0 and player2_life > 0):
        if turn != 0:
            input(
                "You are out of bullets, switching player \nPress enter key to continue...")
            os.system('clear')
        if turn % 2 == 0:
            input("Turn of player 1 \nPress any key to continue...")
            print_board(player1)
            input("Those are your ships \nPress enter key to continue...")
            player2_life = player_turn(
                ammunition, player1_shooting, player2, player2_life)
            if mode_pirates:
                pirate_shot(player1, player1_life)
        else:
            if pv_mode == 'player':
                input("Turn of player 2 \nPress enter key to continue...")
                print_board(player2)
                input("Those are your ships \nPress enter key to continue...")
                player1_life = player_turn(
                    ammunition, player2_shooting, player1, player1_life)
                if mode_pirates:
                    pirate_shot(player2, player2_life)
            elif pv_mode == 'ai':
                print("Turn of player 2")
                player1_life = ai_shoot_vM(
                    possible_shots,
                    ammunition,
                    player2_shooting,
                    player1,
                    player1_life)
        turn += 1

    os.system('clear')
    if(int(player1_life) == 0):
        print("VICTORY ROYALE \nplayer 2 win\n")
        print_board(player1)
    else:
        for i in range(10):
            for j in range(10):
                if player2[i][j] == '#':
                    player2[i][j] = 'x'
        print("VICTORY ROYALE \nplayer 1 win\n")
        print_board(player2)


main()

# https://docs.google.com/document/d/1VBnJelTuwHtcQZPzLOdoqOp3PQxQG-3mAzb_ZNXK6n0/edit
# http://www.ultrabattleship.com/variations.php
# https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
