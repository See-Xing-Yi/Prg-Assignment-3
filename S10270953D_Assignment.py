#Name: See Xing Yi
#ID: S10270953D
#>:[

from random import randint
import json
import os

player = []
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
    with open("level.1.txt", 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    max_width = max(len(line) for line in lines)
    for line in lines:
        map_struct.append(list(line.ljust(max_width)))  # ← pad with spaces

    MAP_HEIGHT = len(map_struct)
    MAP_WIDTH = max_width

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    x, y = player['x'], player['y']
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = x + dx, y + dy
            if 0 <= nx < MAP_HEIGHT and 0 <= ny < MAP_WIDTH:
                fog[nx][ny] = True

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)
    # TODO: initialize fog
    
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
            if i == player['x'] and j == player['y']:
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
    for dx in range(-1, 2):
        row = "|"
        for dy in range(-1, 2):
            nx = player['x'] + dx
            ny = player['y'] + dy
            if 0 <= nx < MAP_HEIGHT and 0 <= ny < MAP_WIDTH:
                if nx == player['x'] and ny == player['y']:
                    row += "M"
                elif fog[nx][ny]:
                    row += game_map[nx][ny]
                else:
                    row += "?"
            else:
                row += "#"
        row += "|"
        print(row)
    print("+---+")

# This function shows the information for the player
def show_information(player):
    print("----- Player Information -----")
    print(f"Name: {player}")
    print(f"Portal Position: ({player['x'], player['y']})")
    print(f"Pickaxe Level: {player['pickaxe_level']}")
    print("------------------------------")
    print(f"Load: {player['load']}/{player['capacity']}")
    print("------------------------------")
    print(f"GP: {player['GP']}")
    print(f"Steps Taken: {player['steps']}")
    print("------------------------------")
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

def enter_mine(player,mine_map):
    print("---------------------------------------------------")
    print(f"                      DAY {player['day']}                       ")
    x, y = player['x'], player['y']
    turns = player['turns']
    print(f"\nTurns left: {turns}, Load: {player['load']}/{player['capacity']}")
    action = input("(W/A/S/D to move, I: Info, P: Portal, Q: Quit): ").lower()
    if action in ['w', 'a', 's', 'd']:
        dx, dy = 0, 0
        if action == 'w': dy = -1
        elif action == 's': dy = 1
        elif action == 'a': dx = -1
        elif action == 'd': dx = 1
        nx, ny = player['x'] + dx, player['y'] + dy
        if not in_bounds(nx, ny):
                print("You can't go that way.")
        else:
            symbol = game_map[ny][nx]
            mineral = mineral_names.get(symbol)
            if mineral:
                    if mineral not in pickaxe_ability[player['pickaxe_level']]:
                        print(f"You cannot mine {mineral} with your current pickaxe.")
                    else:
                        if player['load'] >= player['capacity']:
                            print(f"You walk over {mineral}, but your bag is full.")
                        else:
                            qty = randint(*ore_drop[mineral])
                            space = player['capacity'] - player['load']
                            actual = min(qty, space)
                            player[mineral] += actual
                            player['load'] += actual
                            print(f"You mined {qty} piece(s) of {mineral}.")
                            game_map[ny][nx] = "." # Clear the mined tile
                            if actual < qty:
                                print(f"...but you can only carry {actual} more piece(s)!")
    elif action == "i":
        pass
    elif action == "p":
        show_town_menu()
        check_win()
    elif action == "q":
        print("This is to Quit the game, are you sure?")
        confirmation = input("y/n: ").lower()
        if confirmation == "y":
            show_main_menu()
        elif confirmation == "n":
            enter_mine()
    else:
        print("Invalid input")
        enter_mine()
    
def sell_ores():
    global player
    total_gained = 0
    qty = 0
    for m in minerals:
        qty += player['copper'] + player['silver'] + player['gold']
        if qty > 0:
            prices = randint(prices)
            earning = qty * prices
            print(f"You sold {qty} {m} ore for {earning} GP at {prices} each.")
            total_gained += earning
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
    choice = input(print("Your choice? ")).lower()
    if choice == "b":
        shop_menu()
    if choice == "i":
        show_information()
    if choice == "m":
        enter_mine(player)
    if choice == "e":
        pass
    if choice == "v":
        save_game(game_map, fog, player)
    if choice == "q":
        print("Are you sure? Any unsaved changes would be lost.")
        confirmation = input(print("y/n")).lower()
        if confirmation == "y":
            show_main_menu()
        elif confirmation == "n":
            show_town_menu()
        else:
            print("Invalid Input")
            show_town_menu()
            
def shop_menu(buying):
    print("----------------------- Shop Menu -------------------------")
    print(f"(P)ickaxe upgrade to {player['pickaxe_level']+1} to mine silver ore for 50 GP")
    print("(B)ackpack upgrade to carry 12 items for 20 GP")
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print(f"GP: {player['GP']}")
    print("-----------------------------------------------------------")
    buying = input(print("Your choice? ")).lower()
    if buying == "p":
        if player['GP'] >= 50:
            player['GP'] -= 50
            player['pickaxe_level'] += 1
            print(f"Pickaxe upgraded to level {player['pickaxe_level']}!")
        else:
            print("Not enough GP!")
    elif buying == "b":
        if player['GP'] >= 20:
            player['GP'] -= 20
            player['capacity'] += 2
            print(f"Backpack upgraded. New capacity: {player['capacity']}")
        else:
            print("Not enough GP!")
    elif buying == "l":
        show_town_menu()
    else:
        print("Invalid choice.")
        shop_menu()

def main():
    show_main_menu()
    choice = input("Your choice?").lower
    if choice == "n":
        name = input(print("What is your name?"))
        player.append(name)
        show_town_menu()
        #add after initialization complete
    elif choice == "l":
        #add after load game function added
        pass
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
#I keep forgetting this
#dodododoododododododooo