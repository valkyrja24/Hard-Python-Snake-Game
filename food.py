import random
from settings import MAX_FOOD_SPAWN_ATTEMPTS

class Food:
    def __init__(self, grid_width, grid_height, snakes):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = self.spawn(snakes)
        self.pulse = 0

    def spawn(self, snakes):
        all_positions = {pos for snake in snakes for pos in snake.body}
        
        available_positions = []
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) not in all_positions:
                    available_positions.append((x, y))
        
        if not available_positions:
            return (self.grid_width // 2, self.grid_height // 2)
        
        return random.choice(available_positions)