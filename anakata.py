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

world_size = (7, 7, 7, 7)

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
            for i, max_i in zip(new_cell, world_size):
                if i < 0 or i >= max_i:
                    raise MovementException()
                collision = get_object_at(new_cell, ignore=[self])
                if collision:
                    collision.move(movement, obstacles, force - 1)
            new_cells.append(new_cell)

        self.cells = new_cells

    def __str__(self):
        return self.char + ' ' + ' '.join(map(str, self.cells))


player = Object([(3, 3, 3, 3)], '@')
point = Object([(3, 4, 3, 3)], '#')
objects = [player, point]

def get_object_at(position, ignore=set()):
    for o in objects:
        if o in ignore:
            continue
        if position in o.cells:
            return o


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
    for z in reversed(range(world_size[2])):
        for y in reversed(range(world_size[1])):
            for w in reversed(range(world_size[3])):
                for x in range(world_size[0]):
                    o = get_object_at((x, y, z, w))
                    if o:
                        sys.stdout.write(o.char)
                    else:
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
