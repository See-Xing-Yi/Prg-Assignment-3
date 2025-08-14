#Name: See Xing Yi
#ID: S10270953D
#>:[

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
#Why so stingy!!!

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
    if player['torch'] == False:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= ny < MAP_HEIGHT and 0 <= nx < MAP_WIDTH:
                    fog[ny][nx] = True
    else:
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = x + dx, y + dy
                if 0 <= ny < MAP_HEIGHT and 0 <= nx < MAP_WIDTH:
                    fog[ny][nx] = True

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)
    fog.clear()
    player['day'] = 1
    player['x'] = max(0, min(1, MAP_WIDTH - 1))
    player['y'] = max(0, min(1, MAP_HEIGHT - 1))
    for _ in range(MAP_HEIGHT):
        fog.append([False] * MAP_WIDTH)

    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['x'] = 1
    player['y'] = 1
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 1
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['pickaxe_level'] = 1
    player['capacity'] = 10
    player['load'] = 0
    player['torch'] = False

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
def draw_view(game_map, fog, player, viewport_size=3):
    half = viewport_size // 2
    print("+" + "-" * viewport_size + "+")
    for dy in range(-half, half + 1):
        row = "|"
        for dx in range(-half, half + 1):
            nx = player['x'] + dx
            ny = player['y'] + dy

            if 0 <= ny < MAP_HEIGHT and 0 <= nx < MAP_WIDTH:
                if nx == player['x'] and ny == player['y']:
                    row += "M"  # Player marker
                elif fog[ny][nx]:
                    row += game_map[ny][nx]
                else:
                    row += "?"
            else:
                row += "#"  # Outside of map
        row += "|"
        print(row)
    print("+" + "-" * viewport_size + "+")

# This function shows the information for the player
def show_information(player):
    print("----- Player Information -----")
    print(f"Name: {player['name']}")
    print(f"Portal Position: {player['x'], player['y']}")
    print(f"Pickaxe Level: {player['pickaxe_level']}")
    print("------------------------------")
    print(f"Load: {player['load']}/{player['capacity']}")
    print("------------------------------")
    print(f"GP: {player['GP']}")
    print(f"Steps Taken: {player['steps']}")
    print("------------------------------")
    return

#High score functionalities
def save_high_score(player):
    line = f"{player['name']} {player['GP']} {player['day']} {player['steps']}\n"
    with open("highscores.txt", "a") as file:  # 'a' to append
        file.write(line)

def show_high_scores():
    print("----- High Scores -----")

    if not os.path.exists("highscores.txt"):
        print("No high scores yet!")
        return

    scores = []
    with open("highscores.txt", "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 4:
                name, gp, day, steps = parts
                scores.append({
                    'name': name,
                    'GP': int(gp),
                    'day': int(day),
                    'steps': int(steps)
                })
    if not scores:
        print("No high scores yet!")
        return
    scores.sort(key=lambda x: (x['day'], x['steps'], x['GP']))

    #Score then steps
    for i, score in enumerate(scores[:5], 1):  # Show top 5
        print(f"{i}. {score['name']} - {score['day']} days, {score['steps']} steps, {score['GP']} GP")
    print("------------------------")

def check_win():
    if player['GP'] >= 500:
        print(f"Woo-hoo! Well done, {player['name']}, you have {player['GP']} GP!")
        print(f"You now have enough to retire and play video games every day.")
        print(f"And it only took you {player['day']} days and {player['steps']} steps! You win!")
        save_high_score(player)
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
    if not os.path.exists("save.txt"):
        print("No saved game found.")
        return  
    return

def in_bounds(x, y):
    return 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT

def enter_mine(player, mine_map):
    player['turns'] = TURNS_PER_DAY
    clear_fog(fog, player)
    while True:  
        print("---------------------------------------------------")
        print(f"                      DAY {player['day']}                       ")
        viewport = 5 if player.get('torch', False) else 3
        draw_view(game_map, fog, player, viewport_size=viewport)

        print(f"\nTurns left: {player['turns']}, Load: {player['load']}/{player['capacity']}, Steps: {player['steps']}")
        print("(WASD) to move")
        print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")
        action = input("Action?").lower()
        if action in ['w', 'a', 's', 'd']:
            if player['load'] >= player['capacity']:
                print("Your bag is so full, you can't move at all!")
                sell_ores()
                player['day'] += 1
                show_town_menu()
                continue
            dx, dy = 0, 0
            if action == 'w':
                dy = -1
            elif action == 's':
                dy = 1
            elif action == 'a':
                dx = -1
            elif action == 'd':
                dx = 1
            nx = player['x'] + dx
            ny = player['y'] + dy
            if not in_bounds(nx, ny):
                print("You can't go that way.")
                continue
            symbol = game_map[ny][nx]
            mineral = mineral_names.get(symbol)
            player['x'], player['y'] = nx, ny
            player['steps'] += 1
            player['turns'] -= 1
            clear_fog(fog, player)
            if player['turns'] == 0:
                sell_ores()
                print("You are exhausted.")
                print("You place your portal stone here and zap back to town.")
                player['day'] += 1
                show_town_menu()    #Auto this time
            if symbol == 'T':
                print("You step into the portal and return to town.")
                player['day'] += 1
                show_town_menu()
                return
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
                        if actual < qty:
                            print(f"...but you can only carry {actual} more piece(s)!")
                        game_map[ny][nx] = '.'
            continue
        elif action == "m":
            draw_map(game_map, fog, player)
            continue
        elif action == "i":
            show_information(player)
            continue
        elif action == "p":
            print("You place your portal stone here and zap back to town.")
            player['day'] += 1
            player['turns'] = TURNS_PER_DAY
            sell_ores()
            show_town_menu()
            check_win()
            return
        elif action == "q":
            print("This is to Quit the game, are you sure?")
            print("(You can save in the town menu)")
            confirmation = input("y/n: ").lower()
            if confirmation == "y":
                main()
                return
            else:
                continue
        else:
            print("Invalid input.")
    
def sell_ores():
    global player
    total_gained = 0
    for m in minerals:
        qty = player[m]
        if qty > 0:
            price = randint(*prices[m]) 
            earning = qty*price
            print(f"You sold {qty} {m} ore for {earning} GP at {price} each.")
            total_gained += earning
            player[m] = 0
    player['GP'] += total_gained
    player['load'] = 0
    check_win()
#Stingy

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def shop_menu():
    print("----------------------- Shop Menu -------------------------")
    if player['pickaxe_level'] < 3:
        next_level = player['pickaxe_level'] + 1
        ores_for_next_level = pickaxe_ability[next_level]
        ore_name = ores_for_next_level[-1]
        price_index = next_level - 2
        price = pickaxe_price[price_index]
        print(f"(P)ickaxe upgrade to {player['pickaxe_level']+1} to mine {ore_name} ore for {price} GP")
    else:
        print("Pickaxe is already at max level")
    print(f"(B)ackpack upgrade to carry {player['capacity']+2} items for {player['capacity']*2} GP")
    if player['torch'] == False:    
        print("Magic (T)orch, expands your view to 5x5 for 50 GP")
    if player['torch'] == True:
        print("You already have a torch")
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print(f"GP: {player['GP']}")
    print("-----------------------------------------------------------")
    buying = input("Your choice? ").lower()
    if buying == "p":
        if player['GP'] >= price and player['pickaxe_level'] < 3:
            player['GP'] -= price
            player['pickaxe_level'] += 1
            print(f"Pickaxe upgraded to level {player['pickaxe_level']}!")
            shop_menu()
        else:
            print("Not enough GP!")
            shop_menu()
    elif buying == "b":
        if player['GP'] >= 20:
            player['GP'] -= 20
            player['capacity'] += 2
            print(f"Backpack upgraded. New capacity: {player['capacity']}")
            shop_menu()
        else:
            print("Not enough GP!")
            shop_menu()
    elif buying == "t":
        if player['GP'] >= 50:
            player['GP'] -= 50
            player['torch'] = True
            print("You bought the Magic Torch! Your viewport is now 5x5.")
            shop_menu()
        else:
            print("Not enough GP!")
            shop_menu()
    elif buying == "l":
        show_town_menu()
    else:
        print("Invalid choice.")
        shop_menu()

def show_town_menu(sell=False):
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

    if sell:
        sell_ores()

    choice = input("Your choice? ").lower()
    if choice == "b":
        shop_menu()
    elif choice == "i":
        show_information(player)
        show_town_menu()
    elif choice == "m":
        draw_map(game_map, fog, player)
        show_town_menu()
    elif choice == "e":
        clear_fog(fog, player)
        enter_mine(player, game_map)
    elif choice == "v":
        save_game(game_map, fog, player)
        show_town_menu()
    elif choice == "gimmemoney":
        input("How much? ")
        player['GP'] += 10000
        print("Wow. Okay. Here's 10 000 GP")
        check_win()
        show_town_menu()
    elif choice == "q":
        print("Are you sure? Any unsaved changes would be lost.")
        confirmation = input("y/n").lower()
        if confirmation == "y":
            show_main_menu()
            main()
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
        load_game(game_map, fog, player)
        show_town_menu()
    elif choice == "h":
        show_high_scores()
        main()
    elif choice == "q":
        print("See you again!")
    else:
        print("Invalid Input.")
        main()

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 500 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

main()

#I keep forgetting this