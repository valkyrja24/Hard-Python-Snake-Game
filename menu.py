import tkinter as tk
from settings import *

class Menu:
    def __init__(self, root, game_manager):
        self.root = root
        self.game_manager = game_manager
        self.root.title("Snake Game Menu")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=500, height=400, bg=COLOR_BACKGROUND, highlightthickness=0)
        self.canvas.pack()

        self.draw_menu()
        self.setup_input()
        
        self.root.lift()
        self.root.focus_force()

    def draw_menu(self):
        self.canvas.create_text(250, 100, text="🐍 SNAKE GAME 🐍",
                                fill=COLOR_SNAKE_1, font=("Arial", 28, "bold"))
        
        self.canvas.create_text(250, 180, text="Press 1 for Single Player",
                                fill=COLOR_TEXT, font=("Arial", 16))
        self.canvas.create_text(250, 220, text="Press 2 for Two Players",
                                fill=COLOR_TEXT, font=("Arial", 16))
        
        self.canvas.create_text(250, 280, text="Controls:",
                                fill=COLOR_PAUSE, font=("Arial", 14, "bold"))
        self.canvas.create_text(250, 310, text="Player 1: Arrow Keys  |  Player 2: WASD",
                                fill="#888888", font=("Arial", 12))
        
        self.canvas.create_text(250, 360, text="Press Q to Quit",
                                fill="#666666", font=("Arial", 12))

    def setup_input(self):
        self.root.bind("<KeyPress>", self.key_press)
        self.canvas.bind("<FocusOut>", lambda e: self.canvas.focus_set())
        self.canvas.focus_set()

    def key_press(self, event):
        self.canvas.focus_set()
        key = event.keysym
        if key == "1":
            self.game_manager.start_game(players=1)
        elif key == "2":
            self.game_manager.start_game(players=2)
        elif key.lower() == "q":
            self.game_manager.quit_game()

    def cleanup(self):
        pass