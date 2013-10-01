import sys
try:
    from msvcrt import getch
    directions_by_key = {
        'w': 'up', 's': 'down',
        'a': 'ana', 'd': 'kata',
        'H': 'forward', 'P': 'backward',
        'M': 'right', 'K': 'left',
    }
    def display(text):
        sys.stdout.write('\n\n\n' + text)
except ImportError:
    import curses
    window = curses.initscr()
    window.keypad(True)
    curses.noecho()
    curses.cbreak()
    directions_by_key = {
        'w': 'up', 's': 'down',
        'a': 'ana', 'd': 'kata',
        '^u': 'forward', '^d': 'backward',
        '^r': 'right', '^l': 'left',
    }
    def getch():
        code = window.getch()
        if code == 155:
            window.getch()
            return '^' + chr(window.getch())
        else:
            return chr(code)
    def display(text):
        window.addstr(0, 0, text)
        window.refresh()
    import atexit
    atexit.register(lambda: curses.echo()
            or curses.nocbreak() or
            curses.endwin())


def direction_input():
    while True:
        try:
            return directions_by_key[getch()]
        except KeyError:
            continue

world_size = (5, 5, 5, 5)
movement_by_direction = {
    'up': (0, 0, 1, 0),
    'down': (0, 0, -1, 0),
    'ana': (0, 0, 0, 1),
    'kata': (0, 0, 0, -1),
    'forward': (0, 1, 0, 0),
    'backward': (0, -1, 0, 0),
    'right': (1, 0, 0, 0),
    'left': (-1, 0, 0, 0),
}

class MovementException(Exception): pass

class Object(object):
    def __init__(self, cells, char):
        self.cells = cells
        self.char = char

    def move(self, movement, force=1):
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
                    collision.move(movement, force - 1)
            new_cells.append(new_cell)

        self.cells = new_cells

    def __str__(self):
        return self.char + ' ' + ' '.join(map(str, self.cells))


player = Object([tuple(int(i / 2) for i in world_size)], '@')
point = Object([(3, 4, 3, 3)], '#')
objects = [player, point]

def get_object_at(position, ignore=set()):
    for o in objects:
        if o in ignore:
            continue
        if position in o.cells:
            return o


while True:
    output = []
    for z in reversed(range(world_size[2])):
        for y in reversed(range(world_size[1])):
            for w in reversed(range(world_size[3])):
                for x in range(world_size[0]):
                    o = get_object_at((x, y, z, w))
                    if o:
                        output.append(o.char)
                    else:
                        output.append('.')
                output.append(' ')
            output.append('\n')
        output.append('\n')
    display(''.join(output))

    direction = direction_input()
    movement = movement_by_direction[direction]
    try:
        player.move(movement, force=2)
    except MovementException:
        continue
