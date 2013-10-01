import msvcrt

world_side = 7

class MovementException(Exception): pass

class Object(object):
    def __init__(self, cells, char):
        self.cells = cells
        self.char = char

    def move(self, movement):
        new_cells = []
        for cell in self.cells:
            new_cell = tuple(i + j for i, j in zip(cell, movement))
            for i in new_cell:
                if i < 0 or i >= world_side:
                    raise MovementException()
            new_cells.append(new_cell)

        self.cells = new_cells

    def __str__(self):
        return self.char + ' ' + ' '.join(map(str, self.cells))


player = Object([(0, 0, 0, 0)], '@')

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
    print player
