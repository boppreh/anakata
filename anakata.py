import sys, os
try:
    from msvcrt import getch
    directions_by_key = {
        'w': 'up', 's': 'down',
        'a': 'ana', 'd': 'kata',
        'H': 'forward', 'P': 'backward',
        'M': 'right', 'K': 'left',
    }

    # If the user presses an arrow key, `getch` interprets it as a three-byte
    # message. The first two bytes are the same for all directions, and the
    # last one is a seemingly random uppercase letter. We are counting on
    # `direction_input` to ignore the first two bytes.
    def display(text):
        os.system('cls')
        sys.stdout.write(text)

except ImportError:
    import curses, atexit
    window = curses.initscr()
    window.keypad(True)
    curses.noecho()
    curses.cbreak()

    # Without this the program works fine, but the terminal remains borked
    # after exit. If this happens to you, run `reset` to restore (just type and
    # press enter, even if you don't see the text).
    atexit.register(lambda: curses.echo()
            or curses.nocbreak() or
            curses.endwin())

    directions_by_key = {
        ord('w'): 'up', ord('s'): 'down',
        ord('a'): 'ana', ord('d'): 'kata',
        259: 'forward', 258: 'backward',
        261: 'right', 260: 'left',
    }
    # Note: window.getch() returns int, not str. Shouldn't be a problem because
    # `directions_by_key` is indexed by int too.
    getch = window.getch

    def display(text):
        window.addstr(0, 0, text)
        window.refresh()


def direction_input():
    """
    Returns a direction word (e.g. "up", "left", "ana") from user input. Blocks
    until a valid direction is entered.
    """
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
    """
    Physical object represented by a set of cells, connected or not, and a
    single character string.
    """
    def __init__(self, cells, char):
        self.cells = cells
        self.char = char

    def move(self, movement, force=1):
        """
        Moves all the object's cells in a certain direction. If any of the
        cells collide with another object, those objects are pushed
        recursively, with reduced force.

        Illegal movements (not enough force or cell out of bounds) raise an
        exception and no change is made to any of the object's cells.
        """
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


player = Object([tuple(int(i / 2) for i in world_size)], '@')
point = Object([(2, 3, 2, 2)], '#')
objects = [player, point]

def get_object_at(position, ignore=set()):
    """
    Finds the object with a cell at `position`, unless it is in the `ignore`
    set. Returns None if no matches are found.
    """
    for o in objects:
        if o in ignore:
            continue
        if position in o.cells:
            return o

while True:
    output = []
    # Order and direction of axis chosen for intuitive controls.
    # Current setup mimics a grid of grids: the outer rows and columns are the
    # z and w dimensions, the inner ones are y and x (respectively).
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
        # Force = 2. One to move the player, one to push an arbitrary item.
        player.move(movement, force=2)
    except MovementException:
        continue
