import sys
try:
    from msvcrt import getch
except ImportError:
    import tty, termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

world_side = 7

class MovementException(Exception): pass

class Object(object):
    def __init__(self, cells, char):
        self.cells = cells
        self.char = char

    def move(self, movement, obstacles=[], force=1):
        if force == 0:
            raise MovementException()

        new_cells = []
        for cell in self.cells:
            new_cell = tuple(i + j for i, j in zip(cell, movement))
            for i in new_cell:
                if i < 0 or i >= world_side:
                    raise MovementException()
                for o in obstacles:
                    if o == self:
                        continue
                    if new_cell in o.cells:
                        o.move(movement, obstacles, force - 1)
            new_cells.append(new_cell)

        self.cells = new_cells

    def __str__(self):
        return self.char + ' ' + ' '.join(map(str, self.cells))


player = Object([(3, 3, 3, 3)], '@')
point = Object([(3, 4, 3, 3)], '#')
objects = [player, point]

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

    command = getch()
    if command not in directions_by_key:
        continue

    direction = directions_by_key[command]
    try:
        player.move(direction, obstacles=objects, force=2)
    except MovementException:
        continue
