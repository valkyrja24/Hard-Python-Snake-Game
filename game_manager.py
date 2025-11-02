import tkinter as tk
from settings import *

class GameManager:
    def __init__(self):
        self.root = None
        self.current_state = None
        self.show_menu()
    
    def cleanup_current_state(self):
        if self.current_state:
            self.current_state.cleanup()
            self.current_state = None
    
    def show_menu(self):
        self.cleanup_current_state()
        if self.root:
            self.root.destroy()
        
        from menu import Menu
        self.root = tk.Tk()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.current_state = Menu(self.root, self)
    
    def start_game(self, players=1):
        self.cleanup_current_state()
        if self.root:
            self.root.destroy()
        
        from game import Game
        self.root = tk.Tk()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.current_state = Game(self.root, self, players)
    
    def quit_game(self):
        self.cleanup_current_state()
        if self.root:
            self.root.destroy()
    
    def run(self):
        if self.root:
            self.root.mainloop()