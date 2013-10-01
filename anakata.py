import msvcrt

max_x = 7
max_y = 7
max_z = 7
max_w = 7

class Cell(object):
    def __init__(self, pos, char):
        self.pos = pos
        self.char = char

    def move(self, delta_pos):
        self.pos = tuple(i + j for i, j in zip(self.pos, delta_pos))

    def __str__(self):
        return self.char

player = Cell((0, 0, 0, 0), '@')

directions_by_key = {
    'w': (0, 0, 1, 0),
    's': (0, 0, -1, 0),
    'a': (0, 0, 0, 1),
    'd': (0, 0, 0, -1),
    'H': (0, 1, 0, 0),
    'P': (0, -1, 0, 0),
    'M': (1, 0, 0, 0),
    'K': (-1, 0, 0, 0),
}
while True:
    command = msvcrt.getch()
    if command not in directions_by_key:
        continue

    direction = directions_by_key[command]
    player.move(direction)
    print player.pos
