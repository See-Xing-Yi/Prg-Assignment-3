#Bug testing

from random import randint
import json
import os

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]
pickaxe_ability = {1: ['copper'], 2: ['copper', 'silver'], 3: ['copper', 'silver', 'gold']}
ore_drop = {'copper': (1, 5), 'silver': (1, 3), 'gold': (1, 2)} #Wow, stingy

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    global MAP_WIDTH, MAP_HEIGHT
    game_map.clear()
    with open("level1.txt", 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    max_width = max(len(line) for line in lines)
    for line in lines:
        map_struct.append(list(line.ljust(max_width))) 

    MAP_HEIGHT = len(map_struct)
    MAP_WIDTH = max_width

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    x, y = player['x'], player['y']
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = x + dx, y + dy
            if 0 <= ny < MAP_HEIGHT and 0 <= nx < MAP_WIDTH:
                fog[ny][nx] = True

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)
    fog.clear()
    for _ in range(MAP_HEIGHT):
        fog.append([False] * MAP_WIDTH)

    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['pickaxe_level'] = 1
    player['capacity'] = 10
    player['load'] = 0

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    print("+" + "-" * MAP_WIDTH + "+")
    for i in range(MAP_HEIGHT):
        row = "|"
        for j in range(MAP_WIDTH):
            if i == player['y'] and j == player['x']: 
                row += "M"
            elif fog[i][j]:
                row += game_map[i][j]
            else:
                row += "?"
        row += "|"
        print(row)
    print("+" + "-" * MAP_WIDTH + "+")

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    print("+---+")
    for dy in range(-1, 2):  # vertical
        row = "|"
        for dx in range(-1, 2):  # horizontal
            x = player['x'] + dx
            y = player['y'] + dy
            if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                if x == player['x'] and y == player['y']:
                    row += 'M'
                elif fog[y][x]:
                    row += game_map[y][x]
                else:
                    row += '?'
            else:
                row += '#'
        row += "|"
        print(row)
    print("+---+")

# This function shows the information for the player
def show_information(player):
    print("----- Player Information -----")
    print(f"Name: {player['name']}")
    print(f"Portal Position: ({player['x'], player['y']})")
    print(f"Pickaxe Level: {player['pickaxe_level']}")
    print("------------------------------")
    print(f"Load: {player['load']}/{player['capacity']}")
    print("------------------------------")
    print(f"GP: {player['GP']}")
    print(f"Steps Taken: {player['steps']}")
    print("------------------------------")
    show_town_menu()
    return

def check_win():
    if player['GP'] >= 1000:
        print(f"Woo-hoo! Well done, {player}, you have {player['GP']} GP!")
        print(f"You now have enough to retire and play video games every day.")
        print(f"And it only took you {player['day']} days and {player['steps']} steps! You win!")
        main()
    else:
        return

# This function saves the game
def save_game(game_map, fog, player):
    save_data = {
        "game_map":game_map,
        "fog":fog,
        "player": player
    }

    with open ("save.txt", "w") as save_file:
        json.dump(save_data, save_file)
    print("Game saved successfully")
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    with open ("save.txt", "r") as save_file:
        save_data = json.load(save_file)
        game_map.clear()
        for row in save_data['game_map']:
            game_map.append(row)
        fog.clear()
        for row in save_data['fog']:
            fog.append(row)
        player.clear()
        player.update(save_data['player'])

        print("Game loaded successfully.")    
    return

def in_bounds(x, y):
    return 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT

def enter_mine(player, map_struct):
    while True:
        print("---------------------------------------------------")
        print(f"                      DAY {player['day']}                       ")
        draw_view(map_struct, fog, player)  

        print(f"\nTurns left: {player['turns']}, Load: {player['load']}/{player['capacity']}")
        action = input("(W/A/S/D to move, I: Info, P: Portal, Q: Quit): ").lower()

        if action in ['w', 'a', 's', 'd']:
            dx = -1 if action == 'a' else 1 if action == 'd' else 0
            dy = -1 if action == 'w' else 1 if action == 's' else 0

            new_x = player['x'] + dx
            new_y = player['y'] + dy

            if not (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT):
                print("You can't go that way.")
                continue

            symbol = map_struct[new_y][new_x]
            mineral = mineral_names.get(symbol)
            if mineral and mineral in pickaxe_ability[player['pickaxe_level']]:
                qty = randint(*ore_drop[mineral])
                space = player['capacity'] - player['load']
                actual = min(qty, space)
                player[mineral] += actual
                player['load'] += actual
                print(f"You mined {qty} {mineral}.")
                if actual < qty:
                    print(f"…carried only {actual} due to capacity.")
                map_struct[new_y][new_x] = '.'
            elif symbol == 'T':
                print("Returning to town.")
                return  # exits the mine loop

            player['x'], player['y'] = new_x, new_y
            player['turns'] -= 1
            player['steps'] += 1
            clear_fog(fog, player)

        elif action == 'i':
            show_information(player)
        elif action == 'p':
            return  # back to town
        elif action == 'q':
            confirm = input("Quit to main menu? (y/n): ").lower()
            if confirm == 'y':
                show_main_menu()
                return
        else:
            print("Invalid choice.")
    
def sell_ores():
    global player
    total_gained = 0
    for m in minerals:
        qty = player[m]
        if qty > 0:
            price = randint(prices[m])
            earning = qty*prices
            print(f"You sold {qty} {m} ore for {earning} GP at {price} each.")
            total_gained += earning
            player[m] = 0
    player['GP'] += total_gained
    check_win()
#Stingy

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def shop_menu():
    print("----------------------- Shop Menu -------------------------")
    print(f"(P)ickaxe upgrade to {player['pickaxe_level']+1} to mine silver ore for 50 GP")
    print(f"(B)ackpack upgrade to carry {player['capacity']} items for {player['capacity']+2} GP")
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print(f"GP: {player['GP']}")
    print("-----------------------------------------------------------")
    buying = input("Your choice? ").lower()
    if buying == "p":
        if player['GP'] >= 50:
            player['GP'] -= 50
            player['pickaxe_level'] += 1
            print(f"Pickaxe upgraded to level {player['pickaxe_level']}!")
        else:
            print("Not enough GP!")
            shop_menu()
    elif buying == "b":
        if player['GP'] >= 20:
            player['GP'] -= 20
            player['capacity'] += 2
            print(f"Backpack upgraded. New capacity: {player['capacity']}")
        else:
            print("Not enough GP!")
            shop_menu()
    elif buying == "l":
        show_town_menu()
    else:
        print("Invalid choice.")
        shop_menu()

def show_town_menu():
    print()
    print(f"DAY {player['day']}")
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
    choice = input("Your choice? ").lower()
    if choice == "b":
        shop_menu()
    if choice == "i":
        show_information(player)
    if choice == "m":
        draw_map(game_map, fog, player)
        show_town_menu()
    if choice == "e":
        enter_mine(player, game_map)
    if choice == "v":
        save_game(game_map, fog, player)
        show_town_menu()
    if choice == "q":
        print("Are you sure? Any unsaved changes would be lost.")
        confirmation = input("y/n").lower()
        if confirmation == "y":
            show_main_menu()
        elif confirmation == "n":
            show_town_menu()
        else:
            print("Invalid Input")
            show_town_menu()

def main():
    show_main_menu()
    choice = input("Your choice?").lower()
    if choice == "n":
        name = input("What is your name?")
        player['name'] = name
        initialize_game(game_map, fog, player)
        show_town_menu()
    elif choice == "l":
        load_game()
    elif choice == "q":
        print("See you again!")
    elif choice == "gimmemoney":
        player['GP'] += 1000
        check_win()
    else:
        print("Invalid Input.")
        show_main_menu()

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

main()