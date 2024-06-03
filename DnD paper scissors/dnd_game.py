import random
import time
import json
import tkinter as tk
from tkinter import messagebox

def load_character_sheets(filename):
    with open(filename, 'r') as file:
        return json.load(file)

class GameApp:
    def __init__(self, root, character_sheets):
        self.root = root
        self.character_sheets = character_sheets
        self.root.title("Axe, Scroll, Hammer")
        
        self.show_intro()
    
    def show_intro(self):
        self.clear_frame()
        intro_frame = tk.Frame(self.root)
        intro_frame.pack(pady=20)
        
        intro_text = (
            "Welcome to Axe, Scroll, Hammer! A DnD based Axe, Scroll, Hammer game!\n"
            "Each round, you and your opponent will choose Axe, Scroll, Hammer.\n"
            "The winner of each round will roll a dice to deal damage to the opponent.\n"
            "The game continues until one of you has no health left.\n"
            "Choose your gamemode!"
        )
        
        intro_label = tk.Label(intro_frame, text=intro_text, wraplength=400, justify="left")
        intro_label.pack(pady=10)
        
        gamemodes_frame = tk.Frame(self.root)
        gamemodes_frame.pack(pady=10)
        
        quick_play_button = tk.Button(gamemodes_frame, text="Quick play", command=self.quick_play)
        quick_play_button.grid(row=0, column=0, padx=10)
        
        tournament_button = tk.Button(gamemodes_frame, text="Tournament", command=self.tournament)
        tournament_button.grid(row=0, column=1, padx=10)
        
        exit_button = tk.Button(gamemodes_frame, text="Exit", command=self.root.quit)
        exit_button.grid(row=0, column=2, padx=10)
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def quick_play(self):
        self.clear_frame()
        self.player_health = 20
        self.enemy = self.select_enemy()
        self.computer_health = self.enemy["health"]
        self.damage_dice = self.enemy["damage_dice"]
        
        self.play_round()
    
    def tournament(self):
        self.clear_frame()
        self.player_health = 20
        self.enemy_keys = list(self.character_sheets.keys())
        self.tournament_opponents = random.sample(self.enemy_keys, 3)
        self.tournament_index = 0
        self.play_next_enemy()
    
    def play_next_enemy(self):
       if self.tournament_index < len(self.tournament_opponents):
        enemy_key = self.tournament_opponents[self.tournament_index]
        self.enemy = self.character_sheets[enemy_key]
        self.computer_health = self.enemy["health"]
        self.damage_dice = self.enemy["damage_dice"]
        self.tournament_index += 1

        self.play_round()
       else:
        messagebox.showinfo("Tournament", "Congratulations! You won the tournament!")
        self.show_intro()
    
    def select_enemy(self):
        enemy_keys = list(self.character_sheets.keys())
        enemy_name = random.choice(enemy_keys)
        return self.character_sheets[enemy_name]
    
    def get_choice(self):
        choices_frame = tk.Frame(self.root)
        choices_frame.pack(pady=10)
        
        tk.Label(choices_frame, text="Choose Axe, Scroll, Hammer:").grid(row=0, column=0, columnspan=3)
        
        axe_button = tk.Button(choices_frame, text="Axe", command=lambda: self.handle_choice("axe"))
        axe_button.grid(row=1, column=0, padx=5)
        
        scroll_button = tk.Button(choices_frame, text="Scroll", command=lambda: self.handle_choice("scroll"))
        scroll_button.grid(row=1, column=1, padx=5)
        
        hammer_button = tk.Button(choices_frame, text="Hammer", command=lambda: self.handle_choice("hammer"))
        hammer_button.grid(row=1, column=2, padx=5)
    
    def handle_choice(self, player_choice):
        self.player_choice = player_choice
        self.computer_choice = random.choice(['axe', 'scroll', 'hammer'])
        
        result, effect = self.determine_winner(self.player_choice, self.computer_choice)
        self.show_result(result, effect)
    
    def determine_winner(self, player, computer):
        win_conditions = {
            'axe': 'hammer',
            'hammer': 'scroll',
            'scroll': 'axe'
        }
        
        special_conditions = {
            'axe': {'chance': 0.1, 'countered_by': 'scroll', 'effect': 'miss'},
            'hammer': {'chance': 0.1, 'countered_by': 'axe', 'effect': 'stun'},
            'scroll': {'chance': 0.1, 'countered_by': 'hammer', 'effect': 'reverse'}
        }
        
        if player == computer:
            return "tie", None
        
        if random.random() < special_conditions[player]['chance']:
            if computer == special_conditions[player]['countered_by']:
                return "special", special_conditions[player]['effect']
        
        if win_conditions[player] == computer:
            return "player", None
        else:
            return "computer", None
    
    def show_result(self, result, effect):
        self.clear_frame()
        
        result_text = f"Player chose: {self.player_choice}\nComputer chose: {self.computer_choice}\n"
        
        if result == "tie":
            result_text += "It's a tie!"
        elif result == "player":
            if effect == "miss":
                result_text += "You win this round, but your attack misses!"
            elif effect == "stun":
                damage = self.roll_dice(self.damage_dice)
                self.computer_health -= damage
                result_text += f"You win this round and stun the {self.enemy['name']}! You deal {damage} damage."
            elif effect == "reverse":
                damage = self.roll_dice()
                self.player_health -= damage
                result_text += f"You win this round, but the {self.enemy['name']} reverses your attack! You take {damage} damage."
            else:
                damage = self.roll_dice()
                self.computer_health -= damage
                result_text += f"You win this round! You deal {damage} damage."
        elif result == "computer":
            if effect == "reverse":
                damage = self.roll_dice(self.damage_dice)
                self.computer_health -= damage
                result_text += f"{self.enemy['name']} wins this round, but your attack reverses! You deal {damage} damage."
            elif effect == "stun":
                damage = self.roll_dice(self.damage_dice)
                self.player_health -= damage
                result_text += f"{self.enemy['name']} wins this round and stuns you! It deals {damage} damage."
            else:
                damage = self.roll_dice(self.damage_dice)
                self.player_health -= damage
                result_text += f"{self.enemy['name']} wins this round! It deals {damage} damage."
        
        result_text += f"\n\nPlayer Health: {self.player_health} | {self.enemy['name']} Health: {self.computer_health}"
        
        result_label = tk.Label(self.root, text=result_text, wraplength=400, justify="left")
        result_label.pack(pady=10)
        
        if self.player_health <= 0:
            result_label.config(text=result_text + "\n\nYou lost the game!")
            self.root.after(3000, self.show_intro)
        elif self.computer_health <= 0:
            result_label.config(text=result_text + "\n\nYou won the game!")
            self.root.after(3000, self.show_intro)
        else:
            self.root.after(3000, self.get_choice)
    
    def roll_dice(self, sides=6):
        time.sleep(1)
        return random.randint(1, sides)

def main():
    character_sheets = load_character_sheets("character_sheets.json")
    root = tk.Tk()
    app = GameApp(root, character_sheets)
    root.mainloop()

if __name__ == "__main__":
    main()
