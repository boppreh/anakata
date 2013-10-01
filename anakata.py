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


player = Object([(3, 3, 3, 3)], '@')
objects = [player]

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
import sys
while True:
    sys.stdout.write('\n' * 10)
    for z in reversed(range(world_side)):
        for y in reversed(range(world_side)):
            for w in reversed(range(world_side)):
                for x in range(world_side):
                    empty = True
                    for o in objects:
                        if (x, y, z, w) in o.cells:
                            empty = False
                            sys.stdout.write(o.char)
                    if empty:
                        sys.stdout.write('.')

                sys.stdout.write(' ')
            sys.stdout.write('\n')
        sys.stdout.write('\n\n')

    command = msvcrt.getch()
    if command not in directions_by_key:
        continue

    direction = directions_by_key[command]
    player.move(direction)

