# Adaptado de https://gist.github.com/w0300133/7f3e3e6f836e519f64272150ca34080c
import csv


def generate_start_map(_size):
    starting_map = []
    for counter in range(_size):
        current_line = []
        for counter in range(_size):
            current_line.append("~")
        starting_map.append(current_line)
    return starting_map


def shot_to_numbers(_coordinate_string, _headings_list):
    shot_list = [int(_coordinate_string[1])]
    for column in _headings_list:
        if _coordinate_string[0] == column:
            shot_list.append(_headings_list.index(column))
    return shot_list


def check_hit(_shot, _map):
    if _map[_shot[0]][_shot[1]] == "O":
        return ["X", "Miss!"]
    elif _map[_shot[0]][_shot[1]] == "B":
        return ["B", "You hit the BATTLESHIP!"]
    elif _map[_shot[0]][_shot[1]] == "S":
        return ["S", "You hit the SUBMARINE!"]
    elif _map[_shot[0]][_shot[1]] == "D":
        return ["D", "You hit the DESTROYER!"]
    elif _map[_shot[0]][_shot[1]] == "C":
        return ["C", "You hit the CARRIER!"]


def update_map(_last_shot_cell, _last_shot_result, _map):
    _map[_last_shot_cell[0]][_last_shot_cell[1]] = _last_shot_result
    return _map


def check_ship_status(_ship_list, _ship_map):
    ship_status = []
    for index in range(len(_ship_list)):
        ship_status.append(False)
    for index in range(len(_ship_list)):
        for list in _ship_map:
            if _ship_list[index] in list:
                ship_status[index] = True
    return ship_status


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
    valid_rows = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    valid_columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    ship_symbols = ["B", "S", "D", "C"]
    ship_names = ["BATTLESHIP", "SUBMARINE", "DESTROYER", "CARRIER"]
    previous_shots = []
    # ------ Starting the round. Code will need to loop until the user runs out of guesses or wins. ------
    while missile_count > 0:
        # --- Display currentMap to the user ---
        print("---------------------------")
        print("  " + " ".join(valid_columns))
        for counter in range(grid_size):
            print(str(counter) + " " + " ".join(current_map[counter]))

        print("---------------------------\n"
              "MISSILES REMAINING: " + str(missile_count))

        # --- Get location input from the user for their shot ---
        while True:
            userShot = input("Enter the coordinates you wish to shoot: ").upper()
            if len(userShot) != 2:
                print("Please enter a valid coordinate:")
            elif userShot in previous_shots:
                print("You've already shot there, pick a different coordinate.")
            elif userShot[0] not in valid_columns or userShot[1] not in valid_rows:
                print("Please choose a coordinate in range.")
            else:
                previous_shots.append(userShot)
                shotCoordinateList = shot_to_numbers(userShot, valid_columns)
                break

        print("---------------------------")

        # --- Check the shot vs. shipMap to verify a hit or miss ---
        shotResult = check_hit(shotCoordinateList, ship_map)
        print(shotResult[1])

        # --- Update the  game map to refer to when checking ship status ---
        ship_map = update_map(shotCoordinateList, "X", ship_map)

        # - Check the status of the ships to check win condition -
        shipsStillAlive = check_ship_status(ship_symbols, ship_map)
        for index in range(len(shipsStillAlive)):
            if shipsStillAlive[index]:
                print("The " + ship_names[index] + " still sails!")
            else:
                print("You have sunk the " + ship_names[index] + "!")

        # --- Update currentMap ---
        current_map = update_map(shotCoordinateList, shotResult[0], current_map)

        # - Check win condition. If not ships remain end the game. ---
        if True not in shipsStillAlive:
            print("Good shooting! You have destroyed the enemy fleet!")
            break

        # - Check lose condition. Modify the missile count then check if the user has shots remaining. -
        missile_count -= 1
        if missile_count == 0:
            print(
                "Looks like the enemy fleet has escaped the harbour! You had better get your crew in order Admiral!")

        # ------ End of the Round. ------


def get_desired_difficulty():
    # --- Difficulty select. Loop created to ensure valid input entered. ---
    while True:
        difficulty = input("What difficulty would you like to play? (easy/hard) ").lower()
        if difficulty == "easy":
            missileCount = 50  # missileCount used to limit the players guess total
            break
        elif difficulty == "hard":
            missileCount = 35  # missileCount used to limit the players guess total
            break
        else:
            print("Please enter a valid difficulty setting.")
    return missileCount


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
    file_name = "battleshipMap.txt"
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
