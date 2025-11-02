import tkinter as tk
from snake import Snake
from food import Food
from settings import *

class Game:
    def __init__(self, root, game_manager, players=1):
        self.root = root
        self.game_manager = game_manager
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root, 
            width=GRID_WIDTH * CELL_SIZE, 
            height=GRID_HEIGHT * CELL_SIZE, 
            bg=COLOR_BACKGROUND,
            highlightthickness=0
        )
        self.canvas.pack()

        self.players = players
        self.paused = False
        self.countdown = 3
        self.game_started = False
        self.flash_timer = 0
        
        self.reset_game()
        self.setup_input()
        
        self.root.lift()
        self.root.focus_force()
        
        self.start_countdown()

    def setup_input(self):
        self.root.bind("<KeyPress>", self.key_press)
        self.canvas.bind("<FocusOut>", lambda e: self.canvas.focus_set())
        self.canvas.focus_set()

    def reset_game(self):
        self.snake1 = Snake(COLOR_SNAKE_1, COLOR_SNAKE_1_HEAD, (5, 5), "Right")
        self.snake2 = Snake(COLOR_SNAKE_2, COLOR_SNAKE_2_HEAD, (GRID_WIDTH - 6, GRID_HEIGHT - 6), "Left") if self.players == 2 else None
        snakes = [self.snake1] + ([self.snake2] if self.snake2 else [])
        self.food = Food(GRID_WIDTH, GRID_HEIGHT, snakes)
        self.delay = INITIAL_DELAY
        self.score1 = 0
        self.score2 = 0 if self.snake2 else None
        self.dead_snakes = set()
        self.running = False
        self.draw()

    def start_countdown(self):
        if self.countdown > 0:
            self.draw_countdown()
            self.root.after(1000, self.start_countdown)
            self.countdown -= 1
        else:
            self.game_started = True
            self.running = True
            self.update()

    def draw_countdown(self):
        self.draw()
        if self.countdown > 0:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2, 
                GRID_HEIGHT * CELL_SIZE // 2,
                fill=COLOR_COUNTDOWN, 
                text=str(self.countdown), 
                font=("Arial", 72, "bold")
            )
        else:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2, 
                GRID_HEIGHT * CELL_SIZE // 2,
                fill=COLOR_SNAKE_1, 
                text="GO!", 
                font=("Arial", 72, "bold")
            )

    def draw(self):
        self.canvas.delete("all")
        
        self.draw_grid()
        self.draw_food()
        self.draw_snakes()
        self.draw_hud()
        
        if self.paused:
            self.draw_pause_screen()

    def draw_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if (x + y) % 2 == 0:
                    self.canvas.create_rectangle(
                        x * CELL_SIZE, y * CELL_SIZE,
                        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                        fill=COLOR_GRID, outline=""
                    )

    def draw_food(self):
        x, y = self.food.position
        self.food.pulse = (self.food.pulse + 1) % 20
        pulse_size = 2 if self.food.pulse < 10 else 0
        
        offset = CELL_SIZE // 2
        self.canvas.create_oval(
            x * CELL_SIZE + 2 - pulse_size, 
            y * CELL_SIZE + 2 - pulse_size,
            (x + 1) * CELL_SIZE - 2 + pulse_size, 
            (y + 1) * CELL_SIZE - 2 + pulse_size,
            fill=COLOR_FOOD, outline=COLOR_FOOD_GLOW, width=2
        )

    def draw_snakes(self):
        if PLAYER_1 not in self.dead_snakes:
            for i, (sx, sy) in enumerate(self.snake1.body):
                color = self.snake1.head_color if i == 0 else self.snake1.color
                radius = 3 if i == 0 else 1
                self.canvas.create_rectangle(
                    sx * CELL_SIZE + radius, sy * CELL_SIZE + radius,
                    (sx + 1) * CELL_SIZE - radius, (sy + 1) * CELL_SIZE - radius,
                    fill=color, outline=""
                )
                if i == 0:
                    eye_offset = 6
                    eye_size = 3
                    if self.snake1.direction == "Right":
                        ex1, ey1 = sx * CELL_SIZE + 14, sy * CELL_SIZE + 6
                        ex2, ey2 = sx * CELL_SIZE + 14, sy * CELL_SIZE + 14
                    elif self.snake1.direction == "Left":
                        ex1, ey1 = sx * CELL_SIZE + 6, sy * CELL_SIZE + 6
                        ex2, ey2 = sx * CELL_SIZE + 6, sy * CELL_SIZE + 14
                    elif self.snake1.direction == "Up":
                        ex1, ey1 = sx * CELL_SIZE + 6, sy * CELL_SIZE + 6
                        ex2, ey2 = sx * CELL_SIZE + 14, sy * CELL_SIZE + 6
                    else:
                        ex1, ey1 = sx * CELL_SIZE + 6, sy * CELL_SIZE + 14
                        ex2, ey2 = sx * CELL_SIZE + 14, sy * CELL_SIZE + 14
                    
                    self.canvas.create_oval(ex1, ey1, ex1 + eye_size, ey1 + eye_size, fill="black")
                    self.canvas.create_oval(ex2, ey2, ex2 + eye_size, ey2 + eye_size, fill="black")
        
        if self.snake2 and PLAYER_2 not in self.dead_snakes:
            for i, (sx, sy) in enumerate(self.snake2.body):
                color = self.snake2.head_color if i == 0 else self.snake2.color
                radius = 3 if i == 0 else 1
                self.canvas.create_rectangle(
                    sx * CELL_SIZE + radius, sy * CELL_SIZE + radius,
                    (sx + 1) * CELL_SIZE - radius, (sy + 1) * CELL_SIZE - radius,
                    fill=color, outline=""
                )
                if i == 0:
                    eye_size = 3
                    if self.snake2.direction == "Right":
                        ex1, ey1 = sx * CELL_SIZE + 14, sy * CELL_SIZE + 6
                        ex2, ey2 = sx * CELL_SIZE + 14, sy * CELL_SIZE + 14
                    elif self.snake2.direction == "Left":
                        ex1, ey1 = sx * CELL_SIZE + 6, sy * CELL_SIZE + 6
                        ex2, ey2 = sx * CELL_SIZE + 6, sy * CELL_SIZE + 14
                    elif self.snake2.direction == "Up":
                        ex1, ey1 = sx * CELL_SIZE + 6, sy * CELL_SIZE + 6
                        ex2, ey2 = sx * CELL_SIZE + 14, sy * CELL_SIZE + 6
                    else:
                        ex1, ey1 = sx * CELL_SIZE + 6, sy * CELL_SIZE + 14
                        ex2, ey2 = sx * CELL_SIZE + 14, sy * CELL_SIZE + 14
                    
                    self.canvas.create_oval(ex1, ey1, ex1 + eye_size, ey1 + eye_size, fill="black")
                    self.canvas.create_oval(ex2, ey2, ex2 + eye_size, ey2 + eye_size, fill="black")

    def draw_hud(self):
        score_text = f"P1: {self.score1}"
        if self.snake2:
            score_text += f"   |   P2: {self.score2}"
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE // 2, 15,
            fill=COLOR_TEXT, text=score_text, font=("Arial", 14, "bold")
        )

        if PLAYER_1 in self.dead_snakes:
            self.canvas.create_text(
                80, 15, fill=COLOR_SNAKE_1, 
                text="P1 DEAD", font=("Arial", 12, "bold")
            )
        if PLAYER_2 in self.dead_snakes:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE - 80, 15, 
                fill=COLOR_SNAKE_2, text="P2 DEAD", 
                font=("Arial", 12, "bold")
            )

        speed_percent = int((1 - (self.delay / INITIAL_DELAY)) * 100)
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE - 50, 
            GRID_HEIGHT * CELL_SIZE - 10,
            fill="#666666", 
            text=f"Speed: {speed_percent}%", 
            font=("Arial", 9)
        )

    def draw_pause_screen(self):
        overlay = self.canvas.create_rectangle(
            0, 0, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE,
            fill=COLOR_BACKGROUND, stipple="gray50"
        )
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE // 2, 
            GRID_HEIGHT * CELL_SIZE // 2 - 20,
            fill=COLOR_PAUSE, 
            text="PAUSED", 
            font=("Arial", 48, "bold")
        )
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE // 2, 
            GRID_HEIGHT * CELL_SIZE // 2 + 30,
            fill=COLOR_TEXT, 
            text="Press P to Resume", 
            font=("Arial", 16)
        )

    def update(self):
        if not self.running or self.paused:
            return

        if PLAYER_1 not in self.dead_snakes:
            self.snake1.move()
        if self.snake2 and PLAYER_2 not in self.dead_snakes:
            self.snake2.move()

        self.check_collisions()
        self.check_food()

        if self.snake2:
            if PLAYER_1 in self.dead_snakes and PLAYER_2 in self.dead_snakes:
                self.end_game()
                return
        elif PLAYER_1 in self.dead_snakes:
            self.end_game()
            return

        self.draw()
        self.root.after(self.delay, self.update)

    def check_collisions(self):
        snakes = [(PLAYER_1, self.snake1)] + ([(PLAYER_2, self.snake2)] if self.snake2 else [])
        for pid, snake in snakes:
            if pid in self.dead_snakes:
                continue
            x, y = snake.head()
            if x < 0 or y < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or snake.collision_with_self():
                self.dead_snakes.add(pid)
                continue
            
            other = self.snake2 if pid == PLAYER_1 else self.snake1
            if other and (x, y) in other.body:
                self.dead_snakes.add(pid)

    def check_food(self):
        snakes = [(PLAYER_1, self.snake1)] + ([(PLAYER_2, self.snake2)] if self.snake2 else [])
        for pid, snake in snakes:
            if pid in self.dead_snakes:
                continue
            if snake.head() == self.food.position:
                snake.grow()
                if pid == PLAYER_1:
                    self.score1 += 1
                else:
                    self.score2 += 1
                
                alive_snakes = [s for p, s in snakes if p not in self.dead_snakes]
                self.food = Food(GRID_WIDTH, GRID_HEIGHT, alive_snakes)
                self.delay = max(MIN_DELAY, int(self.delay * SPEEDUP_FACTOR))
                self.flash_timer = 3
                break

    def key_press(self, event):
        self.canvas.focus_set()
        key = event.keysym
        
        if key.lower() == "p" and self.game_started:
            self.paused = not self.paused
            if not self.paused:
                self.update()
            else:
                self.draw()
            return
        
        if self.paused:
            return
        
        if key in ["Up", "Down", "Left", "Right"] and PLAYER_1 not in self.dead_snakes:
            self.snake1.change_direction(key)
        elif key in ["w", "a", "s", "d"] and self.snake2 and PLAYER_2 not in self.dead_snakes:
            mapping = {"w": "Up", "s": "Down", "a": "Left", "d": "Right"}
            self.snake2.change_direction(mapping[key])
        elif key.lower() == "q":
            self.game_manager.quit_game()
        elif key.lower() == "r":
            self.game_manager.start_game(self.players)
        elif key.lower() == "m":
            self.game_manager.show_menu()

    def end_game(self):
        self.running = False
        self.draw()
        
        winner_text = ""
        if self.snake2:
            if self.score1 > self.score2:
                winner_text = f"Player 1 Wins!\n"
            elif self.score2 > self.score1:
                winner_text = f"Player 2 Wins!\n"
            else:
                winner_text = f"It's a Tie!\n"
        
        self.canvas.create_rectangle(
            GRID_WIDTH * CELL_SIZE // 2 - 200, 
            GRID_HEIGHT * CELL_SIZE // 2 - 100,
            GRID_WIDTH * CELL_SIZE // 2 + 200, 
            GRID_HEIGHT * CELL_SIZE // 2 + 100,
            fill="#000000", outline=COLOR_TEXT, width=3
        )
        
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE // 2, 
            GRID_HEIGHT * CELL_SIZE // 2 - 60,
            fill="#ff6666", 
            text="GAME OVER", 
            font=("Arial", 32, "bold")
        )
        
        if winner_text:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2, 
                GRID_HEIGHT * CELL_SIZE // 2 - 20,
                fill=COLOR_PAUSE, 
                text=winner_text, 
                font=("Arial", 20, "bold")
            )
        
        score_display = f"P1: {self.score1}" + (f"  |  P2: {self.score2}" if self.snake2 else "")
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE // 2, 
            GRID_HEIGHT * CELL_SIZE // 2 + 10,
            fill=COLOR_TEXT, 
            text=score_display, 
            font=("Arial", 18)
        )
        
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE // 2, 
            GRID_HEIGHT * CELL_SIZE // 2 + 50,
            fill="#aaaaaa", 
            text="R: Restart  |  M: Menu  |  Q: Quit", 
            font=("Arial", 12)
        )

    def cleanup(self):
        self.running = False