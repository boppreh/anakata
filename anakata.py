import msvcrt

world_side = 7

class MovementException(Exception): pass

class Cell(object):
    def __init__(self, pos, char):
        self.pos = pos
        self.char = char

    def move(self, delta_pos):
        new_pos = tuple(i + j for i, j in zip(self.pos, delta_pos))
        for i in new_pos:
            if i < 0 or i >= world_side:
                raise MovementException()

        self.pos = new_pos

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
