#Name: See Xing Yi
#ID: S10270953D

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
    player['pickaxe_level'] = 1

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    return

# This function shows the information for the player
def show_information(player):
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
    return

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
        return

def enter_mine(player,mine_map):
    
    print("---------------------------------------------------")
    print(f"                      DAY {player['day']}                       ")
    x, y = player['x'], player['y']
    turns = player['turns']
    print(f"\nTurns left: {turns}, Load: {player['load']}/{player['capacity']}")
    action = input("(W/A/S/D to move, I: Info, P: Portal, Q: Quit): ").lower()
    if action == "w":
        new_pos = (x + 1, y)
    elif action == "a":
        new_pos = (x, y - 1)
    elif action == "s":
        new_pos = (x - 1, y)
    elif action == "d":
        new_pos = (x, y + 1)
    else:
        print("Invalid input")
        return
    

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

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
    else:
        print("Invalid Input.")
        return