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


def update_map(_last_shot_cell, _last_shot_result, _map):
    _map[_last_shot_cell[0]][_last_shot_cell[1]] = _last_shot_result
    return _map


def print_welcome_message():
    # --- Welcome message and UX code ---
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


def read_map_from_csv(_file_name):
    ship_map = []
    try:
        with open(_file_name, "r") as fileData:
            ship_locations = csv.reader(fileData)
            for row in ship_locations:
                ship_map.append(row)
    except FileNotFoundError:
        print("Sorry, there was an error loading a required file.")
    return ship_map


def play_round(current_map, grid_size, missile_count, ship_map):
    previous_shots = []
    # ------ Starting the round. Code will need to loop until the user runs out of guesses or wins. ------
    while missile_count > 0:
        show_player_map(current_map, grid_size, missile_count)
        shot_coordinate_list = get_shot_input(previous_shots)
        print("---------------------------")
        shot_result = check_hit(shot_coordinate_list, ship_map)
        ship_map = update_map(shot_coordinate_list, "X", ship_map)
        ships_still_alive = check_ship_status(ship_map)
        check_ships_alive(ships_still_alive)
        current_map = update_map(shot_coordinate_list, shot_result[0], current_map)
        if True not in ships_still_alive:
            print("Good shooting! You have destroyed the enemy fleet!")
            break
        missile_count -= 1
        if missile_count == 0:
            print(
                "Looks like the enemy fleet has escaped the harbour! You had better get your crew in order Admiral!")


def check_ship_status(_ship_map):
    ship_status = []
    total_ships = len(Ships)-1
    for index in range(total_ships):
        ship_status.append(False)
    for index in range(total_ships):
        for _list in _ship_map:
            if Ships(index+1).name[0] in _list:
                ship_status[index] = True
    return ship_status


def check_ships_alive(ships_still_alive):
    for index in range(len(ships_still_alive)):
        if ships_still_alive[index]:
            print("The " + Ships(index).name + " still sails!")
        else:
            print("You have sunk the " + Ships(index).name + "!")


def get_shot_input(previous_shots):
    shot_coordinate_list = []
    while True:
        user_shot = input("Enter the coordinates you wish to shoot: ").upper()
        if len(user_shot) != 2:
            print("Please enter a valid coordinate:")
            continue
        if not user_shot[0].isalpha():
            print('Input must be Column Letter|Row Number')
            continue
        shot_coordinate_list = shot_to_numbers(user_shot)
        if shot_coordinate_list in previous_shots:
            print("You've already shot there, pick a different coordinate.")
        elif not is_coordinate_valid(shot_coordinate_list):
            print('Please choose a coordinate in range')
        else:
            previous_shots.append(shot_coordinate_list)
            break
    return shot_coordinate_list


def is_coordinate_valid(_user_shot):
    if _user_shot[0] < 0:
        return False
    elif _user_shot[0] >= BOARD_SIZE:
        return False
    elif _user_shot[1] < 0:
        return False
    elif _user_shot[1] >= BOARD_SIZE:
        return False
    return True


def show_player_map(current_map, grid_size, missile_count):
    print("---------------------------")
    print("  " + " ".join(COLUMN_NAMES))
    for counter in range(grid_size):
        print(str(counter) + " " + " ".join(current_map[counter]))
    print("---------------------------\n"
          "MISSILES REMAINING: " + str(missile_count))


def get_desired_difficulty():
    # --- Difficulty select. Loop created to ensure valid input entered. ---
    while True:
        difficulty = input("What difficulty would you like to play? (easy/hard) ").lower()
        if difficulty == "easy":
            missile_count = 50  # missileCount used to limit the players guess total
            break
        elif difficulty == "hard":
            missile_count = 35  # missileCount used to limit the players guess total
            break
        else:
            print("Please enter a valid difficulty setting.")
    return missile_count


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
            print("Unknown inout, please enter Y or N")
    return playing


def play_battleship():
    grid_size = 10
    file_name = "map.csv"
    playing = True
    print_welcome_message()
    while playing:
        ship_map = read_map_from_csv(file_name)
        missile_count = get_desired_difficulty()
        current_map = generate_start_map(grid_size)
        play_round(current_map, grid_size, missile_count, ship_map)
        playing = check_if_play_again()
    print("\nThanks for playing!")


if __name__ == '__main__':
    play_battleship()
