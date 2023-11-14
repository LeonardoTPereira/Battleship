# Adaptado de https://gist.github.com/w0300133/7f3e3e6f836e519f64272150ca34080c
import csv
from enum import IntEnum


class Ships(IntEnum):
    WATER = 0
    SUBMARINE = 1
    DESTROYER = 2
    CRUISER = 3
    BATTLESHIP = 4
    AIRCRAFT_CARRIER = 5


BOARD_SIZE = 10
COLUMN_NAMES = 'ABCDEFGHIJ'


def generate_start_map(_size):
    starting_map = []
    for x in range(_size):
        current_line = []
        for y in range(_size):
            current_line.append("~")
        starting_map.append(current_line)
    return starting_map


def shot_to_numbers(_coordinate_string):
    row_value = int(_coordinate_string[1])
    column_value = ord(_coordinate_string[0]) - ord('A')
    coordinates = (row_value, column_value)
    return coordinates


def check_hit(_shot, _map):
    if _map[_shot[0]][_shot[1]] == Ships.WATER.name[0]:
        return ["X", "Miss!"]
    elif _map[_shot[0]][_shot[1]] == Ships.SUBMARINE.name[0]:
        ship = Ships.SUBMARINE
    elif _map[_shot[0]][_shot[1]] == Ships.DESTROYER.name[0]:
        ship = Ships.DESTROYER
    elif _map[_shot[0]][_shot[1]] == Ships.CRUISER.name[0]:
        ship = Ships.CRUISER
    elif _map[_shot[0]][_shot[1]] == Ships.BATTLESHIP.name[0]:
        ship = Ships.BATTLESHIP
    elif _map[_shot[0]][_shot[1]] == Ships.AIRCRAFT_CARRIER.name[0]:
        ship = Ships.AIRCRAFT_CARRIER
    else:
        return '!'
    return [ship.name[0], 'You hit the ', ship.name, '!']
    return [ship.name[0], "You hit the", ship.name, "!"]


def update_map(_last_shot_cell, _last_shot_result, _map):
    _map[_last_shot_cell[0]][_last_shot_cell[1]] = _last_shot_result
    return _map


def checkShipStatus(_ship_list, _ship_map):
    ship_status = []
    for index in range(len(_ship_list)):
        ship_status.append(False)
    for index in range(len(_ship_list)):
        for list in _ship_map:
            if _ship_list[index] in list:
                ship_status[index] = True
    return ship_status


def create_ship(board, ship):
    ship_size = ship.value
    overlap = True
    completed = False
    while overlap and not completed:
        vertical = random.randint(0, 1)
        if vertical:
            ship_r = random.randint(0, BOARD_SIZE - ship_size - 1)
            ship_c = random.randint(0, BOARD_SIZE - 1)
            increment = [1, 0]
        else:
            ship_r = random.randint(0, BOARD_SIZE - 1)
            ship_c = random.randint(0, BOARD_SIZE - ship_size - 1)
            increment = [0, 1]
        tile_count = 0
        while tile_count < ship_size:
            if board[ship_r + increment[0] * tile_count][ship_c + increment[1] * tile_count] != Ships.WATER.name[0]:
                break
            tile_count += 1
        if tile_count != ship_size:
            continue
        overlap = False
        tile_count = 0
        while tile_count < ship_size:
            board[ship_r + increment[0] * tile_count][ship_c + increment[1] * tile_count] = ship.name[0]
            tile_count += 1
        completed = True


def create_ships():
    board = [[Ships.WATER.name[0]] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    for i in range(2):
        create_ship(board, Ships.SUBMARINE)
    for i in range(2):
        create_ship(board, Ships.DESTROYER)
    create_ship(board, Ships.CRUISER)
    create_ship(board, Ships.BATTLESHIP)
    create_ship(board, Ships.AIRCRAFT_CARRIER)
    return board


def is_coordinate_valid(_user_shot):
    column_value = _user_shot[0]
    row_value = _user_shot[1]
    if column_value < 0:
        return False
    if column_value >= BOARD_SIZE:
        return False
    if row_value < 0:
        return False
    if row_value >= BOARD_SIZE:
        return False
    return True


def print_welcome_message():
    print("---------------------------\n"
          "        BATTLESHIPS\n"
          "---------------------------\n")

    print("Welcome to Battleships Admiral!\n"
          "We've spotted an enemy fleet in our harbour and it's up to you to sink them!\n"
          "You'll need to hit the BATTLESHIP 4 times to get through the thick armour.\n"
          "There's a small DESTROYER that will take two hits, but be careful, it packs a punch!\n"
          "The CARRIER is the biggest ship, it will take five hits to destroy.\n"
          "Then there is a SUBMARINE that will need to be hit three times.\n\n"
          "Your navigator has been given a map of the seas. Fire your missiles into one of the coordinates on the map.\n"
          "Pick your shots carefully though as we have limited ammunition, if you run out they will sail away freely.\n"
          "It's all up to you now Admiral, GOOD LUCK!\n"
          "---------------------------\n")


def run_game_loop(_grid_size, ship_map, ship_dict):
    missile_count = select_difficulty()
    player_map = generate_player_map(_grid_size)
    previous_shots = []
    while missile_count > 0:
        show_player_map(_grid_size, missile_count, player_map)
        shot_coordinate_list = get_shot_input(previous_shots)
        print("---------------------------")
        shot_result = checkHit(shot_coordinate_list, ship_map)
        ship_map = update_map(shot_coordinate_list, "X", ship_map)
        ''''
        # - Check the status of the ships to check win condition -
        shipsStillAlive = checkShipStatus(ship_map)
        for index in range(len(shipsStillAlive)):
            if shipsStillAlive[index]:
                print("The " + shipNames[index] + " still sails!")
            else:
                print("You have sunk the " + shipNames[index] + "!")
        '''

        player_map = update_map(shot_coordinate_list, shot_result[0], player_map)

        ''''
        # - Check win condition. If not ships remain end the game. ---
        if True not in shipsStillAlive:
            print("Good shooting! You have destroyed the enemy fleet!")
            break
        '''

        missile_count -= 1
    print("Looks like the enemy fleet has escaped the harbour! You had better get your crew in order Admiral!")


def get_shot_input(previous_shots):
    shot_coordinate_list = []
    while True:
        user_shot = input("Enter the coordinates you wish to shoot (Column Letter|Row Number):").upper()
        if len(user_shot) != 2:
            print("Please enter a valid coordinate:")
            continue
        if not user_shot[0].isalpha():
            print("Input must be Column Letter|Row Number")
            continue
        shot_coordinate_list = shotToNumbers(user_shot)
        if shot_coordinate_list in previous_shots:
            print("You've already shot there, pick a different coordinate.")
        elif not is_coordinate_valid(shot_coordinate_list):
            print("Please choose a coordinate in range.")
        else:
            previous_shots.append(shot_coordinate_list)
            break
    return shot_coordinate_list


def show_player_map(_grid_size, missile_count, player_map):
    print("---------------------------")
    print("  " + " ".join('ABCDEFGHIJ'))
    for counter in range(_grid_size):
        print(str(counter) + " " + " ".join(player_map[counter]))
    print("---------------------------\n"
          "MISSILES REMAINING: " + str(missile_count))


def select_difficulty():
    while True:
        difficulty = input("What difficulty would you like to play? (easy/hard) ").lower()
        if difficulty == "easy":
            missile_count = 50
            break
        elif difficulty == "hard":
            missile_count = 35
            break
        else:
            print("Please enter a valid difficulty setting.")
    return missile_count


def initialize_ship_map(_mode, _file_name=''):
    if _mode == 0:
        ship_map = create_ships()
    else:
        ship_map = load_ship_map(_file_name)
    return ship_map


def check_if_play_again():
    print("---------------------------")
    user_continue = input("Would you like to play again? (Y/N) ").upper()
    while True:
        if user_continue == "Y":
            playing = True
            break
        elif user_continue == "N":
            playing = False
            break
        else:
            print("Unknown input, please enter Y or N")
    return playing


def load_ship_map(_file_name):
    ship_map = []
    try:
        with open(_file_name, "r") as fileData:
            print('File found. Loaded Ships')
            ship_locations = csv.reader(fileData)
            for row in ship_locations:
                ship_map.append(row)
    except FileNotFoundError:
        print("File not found. Generating a Random Map")
        ship_map = create_ships()
    print(ship_map)
    return ship_map


def get_game_mode():
    print('Please enter the game mode:')
    print('0 - Procedural Map')
    print('1 - Load from a csv file')
    while True:
        try:
            mode = int(input())
        except Exception:
            print('Entrada inválida. Digite 0 ou 1')
        else:
            if mode < 0 or mode > 1:
                print('Entrada inválida. Digite 0 ou 1')
            else:
                break
    return mode


def initialize_ship_dict(_ship_map, grid_size):
    ship_dict = defaultdict(list)
    for i in range(len(_ship_map)):
        for j in range(len(_ship_map[i])):
            if _ship_map[i][j] == Ships.SUBMARINE.name[0]:
                ship_size = Ships.SUBMARINE.value
                ship_symbol = Ships.SUBMARINE.name[0]
            elif _ship_map[i][j] == Ships.DESTROYER.name[0]:
                ship_size = Ships.DESTROYER.value
                ship_symbol = Ships.DESTROYER.name[0]
            elif _ship_map[i][j] == Ships.CRUISER.name[0]:
                ship_size = Ships.CRUISER.value
                ship_symbol = Ships.CRUISER.name[0]
            elif _ship_map[i][j] == Ships.BATTLESHIP.name[0]:
                ship_size = Ships.BATTLESHIP.value
                ship_symbol = Ships.BATTLESHIP.name[0]
            elif _ship_map[i][j] == Ships.AIRCRAFT_CARRIER.name[0]:
                ship_size = Ships.AIRCRAFT_CARRIER.value
                ship_symbol = Ships.AIRCRAFT_CARRIER.name[0]
            else:
                continue
            find_ship_and_fill_dict_with_coordinates(_ship_map, i, j, ship_dict, ship_size, ship_symbol, grid_size)
    return ship_dict


def find_ship_and_fill_dict_with_coordinates(_ship_map, i, j, ship_dict, ship_size, ship_symbol, grid_size):
    increment_index = 0
    increments = [(1, 0), (0, 1)]
    completed = False
    while increment_index < len(increments) and not completed:
        pieces_found = 1
        while pieces_found < ship_size:
            offset_i = i + pieces_found * increments[increment_index][0]
            offset_j = j + pieces_found * increments[increment_index][1]
            if offset_i >= grid_size or offset_j >= grid_size:
                increment_index += 1
                break
            if _ship_map[offset_i][offset_j] == ship_symbol:
                pieces_found += 1
            else:
                increment_index += 1
                break
        if increment_index >= len(increments) or pieces_found < ship_size:
            continue
        offset_i = i + pieces_found * increments[increment_index][0]
        offset_j = j + pieces_found * increments[increment_index][1]
        if _ship_map[offset_i][offset_j] != ship_symbol:
            completed = True
        else:
            offset_i = i + (pieces_found + 1) * increments[increment_index][0]
            offset_j = j + (pieces_found + 1) * increments[increment_index][1]
            if _ship_map[offset_i][offset_j] == ship_symbol:
                completed = True
    if not completed:
        return
    ship_coords = []
    for pieces_found in range(ship_size):
        offset_i = i + pieces_found * increments[increment_index][0]
        offset_j = j + pieces_found * increments[increment_index][1]
        ship_coords.append((offset_i, offset_j))
        pieces_found += 1
    ship_dict[ship_symbol].append(ship_coords)


def main():
    grid_size = 10
    playing = True
    print_welcome_message()
    while playing:
        game_mode = get_game_mode()
        if game_mode == 1:
            print('Enter the file to read the map from:')
            _file_name = input()
            ship_map = initialize_ship_map(game_mode, _file_name)
        else:
            ship_map = initialize_ship_map(game_mode)
        ship_dict = initialize_ship_dict(ship_map, grid_size)
        run_game_loop(grid_size, ship_map, ship_dict)
        playing = check_if_play_again()
    print("\nThanks for playing!")


if __name__ == '__main__':
    main()
