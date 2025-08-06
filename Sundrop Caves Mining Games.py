#Name: See Xing Yi
#ID: S10270953D

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
backpack_price = 

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    # TODO: Add your map loading code here
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    return

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
    player["pickaxe"] = 1
    player["capacity"] = 10

    clear_fog(fog, player)

#Game Mechanic Functions
# This function draws the entire map, covered by the fog
def draw_map(game_map, fog, player,map):
    print("\n ")
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    return

#Portal Stone Functions

#Mine ore functions
def mine_drop():
    

# Bag functions
def backpack():
    pass

# Pickaxe functions
def pickaxe(level):

    pass

#Sell of ores
def sell_ores():
    global player
    gained_gp = 0

    if player

# This function shows the information for the player
def show_information(player):
    print("----- Player Information -----")
    print(f"Name: {player}")
    print(f"Portal Position: ({})")
    print(f"Pickaxe Level: {}")
    print("------------------------------")
    print(f"Load: {}")
    print("------------------------------")
    print(f"GP: {}")
    print(f"Steps Taken: {}")
    print("------------------------------")
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

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    #print("(H)igh scores")
    print("(Q)uit")
    print("------------------")
    choice = input(print("Your choice?: ")).lower()
    if choice == "n":
        show_town_menu()
    elif choice == "l":
        load_game()
    elif choice == "q":
        print("Goodbye :D")
    else:
        print("Invalid Input")
        return

def show_town_menu():
    print()
    # TODO: Show Day
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
        pass
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
            return
            
def shop_menu(buying):
    print("----------------------- Shop Menu -------------------------")
    print(f"(P)ickaxe upgrade to {player['pickaxe']+1} to mine silver ore for 50 GP")
    print("(B)ackpack upgrade to carry 12 items for 20 GP")
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print(f"GP: {}")
    print("-----------------------------------------------------------")
    buying = input(print("Your choice? ")).lower()
    if buying == "p":
        -
    elif buying == "b":
        -
    elif buying == "l":
        show_town_menu()

def enter

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")



