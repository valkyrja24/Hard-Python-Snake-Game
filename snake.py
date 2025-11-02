class Snake:
    def __init__(self, color, head_color, start_pos, direction):
        self.body = [start_pos]
        self.direction = direction
        self.color = color
        self.head_color = head_color
        self.grow_pending = False

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'Up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'Left':
            new_head = (head_x - 1, head_y)
        else:
            new_head = (head_x + 1, head_y)

        self.body.insert(0, new_head)
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self):
        self.grow_pending = True

    def head(self):
        return self.body[0]

    def collision_with_self(self):
        return self.head() in self.body[1:]

    def change_direction(self, new_dir):
        opposite = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if new_dir != opposite[self.direction]:
            self.direction = new_dir