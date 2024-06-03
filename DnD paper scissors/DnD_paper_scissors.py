import random
import time
import json

def load_character_sheets(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def show_intro():
    print("Welcome to Axe, Scroll, Hammer! A DnD based rock, paper, scissors game!")
    print("Each round, you and your opponent will choose Axe, Scroll, Hammer.")
    print("The winner of each round will roll a dice to deal damage to the opponent.")
    print("The game continues until one of you has no health left.")
    print("Choose your gamemode!")
    print("-" * 50)

def show_gamemodes():
    print("1. Quick play")
    print("2. Tournament")
    print("3. Exit")
    choice = input("Enter the number of your choice: ")
    return choice

def get_choice():
    choices = ['axe', 'scroll', 'hammer']
    player_choice = input("Choose Axe, Scroll, Hammer: ").lower()
    while player_choice not in choices:
        player_choice = input("Invalid choice. Choose Axe, Scroll, Hammer: ").lower()
    computer_choice = random.choice(choices)
    print(f"Computer chose: {computer_choice}")
    return player_choice, computer_choice

def determine_winner(player, computer):
    # Define the basic win conditions
    win_conditions = {
        'axe': 'hammer',
        'hammer': 'scroll',
        'scroll': 'axe'
    }
    
    # Special conditions
    special_conditions = {
        'axe': {'chance': 0.1, 'countered_by': 'scroll', 'effect': 'miss'},
        'hammer': {'chance': 0.1, 'countered_by': 'axe', 'effect': 'stun'},
        'scroll': {'chance': 0.1, 'countered_by': 'hammer', 'effect': 'reverse'}
    }
    
    if player == computer:
        return "tie", None  # Tie

    # Check for special conditions
    if random.random() < special_conditions[player]['chance']:
        if computer == special_conditions[player]['countered_by']:
            return "special", special_conditions[player]['effect']
    
    if win_conditions[player] == computer:
        return "player", None
    else:
        return "computer", None

def roll_dice(sides=6):
    input("Press Enter to roll the dice...")
    print("Rolling the dice...", end="")
    for _ in range(10):  # Simulate the dice rolling
        print(".", end="", flush=True)
        time.sleep(0.1)
    result = random.randint(1, sides)
    print(f"\nYou rolled a {result}!")
    return result

def select_enemy(character_sheets):
    print("Select your opponent:")
    for idx, enemy in enumerate(character_sheets.keys(), start=1):
        print(f"{idx}. {character_sheets[enemy]['name']}")
    choice = int(input("Enter the number of your choice: "))
    enemy_key = list(character_sheets.keys())[choice - 1]
    return character_sheets[enemy_key]

def play_round(player_health, computer_health, damage_dice, enemy_name):
    while player_health > 0 and computer_health > 0:
        player, computer = get_choice()
        result, effect = determine_winner(player, computer)
        
        if result == "player":
            if effect == "miss":
                print(f"You win this round, but your attack misses!")
            elif effect == "stun":
                damage = roll_dice(damage_dice)
                computer_health -= damage
                print(f"You win this round and stun the {enemy_name}! You deal {damage} damage.")
                time.sleep(3)
            elif effect == "reverse":
                damage = roll_dice()
                player_health -= damage
                print(f"You win this round, but the {enemy_name} reverses your attack! You take {damage} damage.")
                time.sleep(3)
            else:
                damage = roll_dice()
                computer_health -= damage
                print(f"You win this round! You deal {damage} damage.")
                time.sleep(3)
        elif result == "computer":
            if effect == "reverse":
                damage = roll_dice(damage_dice)
                computer_health -= damage
                print(f"{enemy_name} wins this round, but your attack reverses! You deal {damage} damage.")
                time.sleep(3)
            elif effect == "stun":
                damage = roll_dice(damage_dice)
                player_health -= damage
                print(f"{enemy_name} wins this round and stuns you! It deals {damage} damage.")
                time.sleep(3)
            else:
                damage = roll_dice(damage_dice)
                player_health -= damage
                print(f"{enemy_name} wins this round! It deals {damage} damage.")
                time.sleep(3)
        else:  # tie
            print("It's a tie!")
            time.sleep(3)
        
        print(f"Player Health: {player_health} | {enemy_name} Health: {computer_health}")
        print("-" * 50)
        time.sleep(3)
    
    return player_health, computer_health

def quick_play(character_sheets):
    player_health = 20
    enemy = select_enemy(character_sheets)
    computer_health = enemy["health"]
    damage_dice = enemy["damage_dice"]
    
    print(f"You are fighting against a {enemy['name']} with {computer_health} health.")
    player_health, computer_health = play_round(player_health, computer_health, damage_dice, enemy['name'])
    
    if player_health <= 0:
        print("You lost the game!")
        time.sleep(5)
    else:
        print("You won the game!")
        time.sleep(5)

def tournament(character_sheets):
    player_health = 20
    enemies = list(character_sheets.values())
    
    for enemy in enemies:
        computer_health = enemy["health"]
        damage_dice = enemy["damage_dice"]
        print(f"Next opponent: {enemy['name']} with {computer_health} health.")
        
        player_health, computer_health = play_round(player_health, computer_health, damage_dice, enemy['name'])
        
        if player_health <= 0:
            print("You lost the tournament!")
            return
    
    print("Congratulations! You won the tournament!")

if __name__ == "__main__":
    character_sheets = load_character_sheets("character_sheets.json")
    
    show_intro()
    
    while True:
        choice = show_gamemodes()
        if choice == '1':
            quick_play(character_sheets)
        elif choice == '2':
            tournament(character_sheets)
        elif choice == '3':
            print("Exiting game.")
            break
        else:
            print("Invalid choice. Please select again.")
