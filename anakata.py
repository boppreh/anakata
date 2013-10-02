import sys, os
from collections import defaultdict
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
    atexit.register(curses.endwin)
    atexit.register(curses.nocbreak)
    atexit.register(curses.echo)

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
class LevelEndException(Exception): pass

class Object(object):
    """
    Physical object represented by a set of cells, connected or not, and a
    single character string.
    """
    def __init__(self, cells, char, is_immovable=False, world=None):
        self.cells = cells
        self.char = char
        self.is_immovable = is_immovable
        self.world = world

    def move(self, movement, force=1):
        """
        Moves all the object's cells in a certain direction. If any of the
        cells collide with another object, those objects are pushed
        recursively, with reduced force.

        Illegal movements (not enough force or cell out of bounds) raise an
        exception and no change is made to any of the object's cells.
        """
        if force == 0 or self.is_immovable:
            raise MovementException()

        new_cells = []
        for cell in self.cells:
            new_cell = tuple(i + j for i, j in zip(cell, movement))

            for i, max_i in zip(new_cell, self.world.size):
                if i < 0 or i >= max_i:
                    raise MovementException()

            collision = self.world.get_object_at(new_cell, ignore=[self])
            if collision:
                collision.move(movement, force - 1)

            new_cells.append(new_cell)

        self.cells = new_cells


class World(object):
    """
    Class containing the objects and dimension for a single world.
    """
    def __init__(self, objects, size):
        self.objects = objects
        self.size = size

        for o in objects:
            o.world = self

    def get_object_at(self, position, ignore=set()):
        """
        Finds the object with a cell at `position`, unless it is in the `ignore`
        set. Returns None if no matches are found.
        """
        for o in self.objects:
            if o in ignore:
                continue
            if position in o.cells:
                return o

    def draw_world(self, special_cases={}):
        """
        Returns a generator that yields the individual chars that make up the
        world.
        """
        # Order and direction of axis chosen for intuitive controls.
        # Current setup mimics a grid of grids: the outer rows and columns are the
        # z and w dimensions, the inner ones are y and x (respectively).
        for z in reversed(range(self.size[2])):
            for y in reversed(range(self.size[1])):
                for w in reversed(range(self.size[3])):
                    for x in range(self.size[0]):
                        cell = (x, y, z, w)
                        o = self.get_object_at(cell)
                        if o:
                            yield o.char
                        elif cell in special_cases:
                            yield special_cases[cell]
                        else:
                            yield '.'
                    yield ' '
                yield '\n'
            yield '\n'


class Game(object):
    """
    Interactive game class.
    """
    def __init__(self, player, world):
        self.player = player
        self.world = world

    def read_and_process_input(self):
        """
        Reads one input command from the user and updates the world.
        """
        direction = direction_input()
        movement = movement_by_direction[direction]
        try:
            # Force = 2. One to move the player, one to push an arbitrary item.
            self.player.move(movement, force=2)
        except MovementException:
            return

    def run(self):
        """
        Loops reading input from the user and moving the player character until
        the player wins.
        """
        while True:
            display(''.join(self.world.draw_world()))
            self.read_and_process_input()

class Level(Game):
    """
    Class for a single game level.
    """
    @staticmethod
    def load(level_text):
        """
        Creates a new level based on a textual map. Cells with the same symbol
        are merged into a single object and '@' denotes the player.
        """
        cells_by_char = defaultdict(list)
        max_cell = (0, 0, 0, 0)
        level_text = level_text.strip()
        for z, z_contents in enumerate(reversed(level_text.split('\n\n'))):
            for y, y_contents in enumerate(reversed(z_contents.split('\n'))):
                for w, w_contents in enumerate(reversed(y_contents.split(' '))):
                    for x, x_contents in enumerate(w_contents):
                        cell = (x, y, z, w)
                        if x_contents != '.':
                            cells_by_char[x_contents].append(cell)
                        if cell > max_cell:
                            max_cell = cell

        target = cells_by_char['X'][0]
        del cells_by_char['X']

        objects_by_char = {char: Object(cells, char, char == 'o', None)
                           for char, cells in cells_by_char.items()}

        player = objects_by_char['@']
        item = objects_by_char['#']
        objects = [o for char, o in objects_by_char.items()]
        size = tuple(i + 1 for i in max_cell)
        return Level(player, item, target, World(objects, size))

    def __init__(self, player, item, target, world):
        Game.__init__(self, player, world)
        self.item = item
        self.target = target

    def run(self):
        while True:
            display(''.join(self.world.draw_world({self.target: 'X'})))
            if self.target in self.item.cells:
                return
            self.read_and_process_input()


class LevelSelection(Game):
    """
    Selection screen displayed as in-game level.
    """
    def __init__(self, levels):
        player = Object([(0, 4, 1, 0)], '@')
        objects = [player]
        self.levels = levels

        Game.__init__(self, player, World(objects, (5, 5, 2, 1)))

    def run(self):
        level_by_cell = {}
        for i, level in enumerate(levels):
            x = int(i % 5)
            y = 4 - int(i / 5)
            cell = (x, y, 0, 0)
            level_by_cell[cell] = str(i + 1)

        while True:
            display(''.join(self.world.draw_world(level_by_cell)))
            self.read_and_process_input()

            player_cell = self.player.cells[0]
            if player_cell in level_by_cell:
                level_number = level_by_cell[self.player.cells[0]]
                level = self.levels[int(level_number) - 1]
                level.run()


if __name__ == '__main__':
    levels = [Level.load(open('levels/' + level).read())
              for level in os.listdir('levels')
              if not level.startswith('.')]

    LevelSelection(levels).run()
