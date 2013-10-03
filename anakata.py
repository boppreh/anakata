import os
from collections import defaultdict
from console import display, get_key, get_option

class MovementError(Exception): pass
class LevelEnd(Exception): pass

movement_by_key = {
    'w': (0, 0, 1, 0),
    's': (0, 0, -1, 0),
    'a': (0, 0, 0, 1),
    'd': (0, 0, 0, -1),
    'up': (0, 1, 0, 0),
    'down': (0, -1, 0, 0),
    'right': (1, 0, 0, 0),
    'left': (-1, 0, 0, 0),
}

class Object(object):
    """
    Physical object represented by a set of cells, connected or not, and a
    single character string.
    """
    def __init__(self, cells, char, is_movable=True, world=None):
        self.cells = cells
        self.char = char
        self.is_movable = is_movable
        self.world = world

    def move(self, movement, force=1):
        """
        Moves all the object's cells in a certain direction. If any of the
        cells collide with another object, those objects are pushed
        recursively, with reduced force.

        Illegal movements (not enough force or cell out of bounds) raise an
        error and no change is made to any of the object's cells.
        """
        if force == 0 or not self.is_movable:
            raise MovementError()

        new_cells = []
        for cell in self.cells:
            new_cell = tuple(i + j for i, j in zip(cell, movement))

            for i, max_i in zip(new_cell, self.world.size):
                if i < 0 or i >= max_i:
                    raise MovementError()

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

    def draw(self, special_cases={}):
        """
        Returns a textual representation of the world and all its objects,
        placing the special case symbols over empty spaces.
        """
        # Order and direction of axis chosen for intuitive controls.
        # Current setup mimics a grid of grids: the outer rows and columns are the
        # z and w dimensions, the inner ones are y and x (respectively).

        # Example 3x3x3x3
        # ... ... ...
        # ... ... ...  
        # ... ... ... z
        #             +
        # ...y... ... |
        # ...+... ... |
        # ...|... ... |
        #     -+x
        # ... ... ...
        # ... ... ...
        # ... ... ...
        # ----------+ w
        output = []
        for z in reversed(range(self.size[2])):
            for y in reversed(range(self.size[1])):
                for w in reversed(range(self.size[3])):
                    for x in range(self.size[0]):
                        cell = (x, y, z, w)
                        o = self.get_object_at(cell)
                        if o:
                            output.append(o.char)
                        elif cell in special_cases:
                            output.append(special_cases[cell])
                        else:
                            output.append('.')
                    output.append(' ')
                output.append('\n')
            output.append('\n')

        return ''.join(output)


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
        try:
            # Force = 2. One to move the player, one to push an arbitrary item.
            self.player.move(get_option(movement_by_key), force=2)
        except MovementError:
            return

    def run(self):
        """
        Loops reading input from the user and moving the player character until
        the player wins.
        """
        while True:
            display(self.world.draw())
            self.read_and_process_input()

class Level(Game):
    """
    Class for a single game level.
    """
    @staticmethod
    def load(level_file):
        """
        Creates a new level based on a textual map. Cells with the same symbol
        are merged into a single object and '@' denotes the player.
        """
        level_text = open(level_file).read()
        level_name = os.path.basename(os.path.splitext(level_file)[0])
        cells_by_char = defaultdict(list)
        level_text = level_text.strip()

        max_z = level_text.count('\n\n') + 1
        max_w = level_text.split('\n')[0].count(' ') + 1
        max_x = int((len(level_text.split('\n')[0]) + 1) / max_w) - 1
        max_y = int((level_text.count('\n') + 1) / max_z)
        size = (max_x, max_y, max_z, max_w)

        # Mimics the World.draw method, but splitting instead of joining.
        for z, z_contents in enumerate(reversed(level_text.split('\n\n'))):
            for y, y_contents in enumerate(reversed(z_contents.split('\n'))):
                for w, w_contents in enumerate(reversed(y_contents.split(' '))):
                    for x, x_contents in enumerate(w_contents):
                        cell = (x, y, z, w)
                        assert cell < size
                        if x_contents != '.':
                            cells_by_char[x_contents].append(cell)

        target = cells_by_char['X'][0]
        del cells_by_char['X']

        objects_by_char = {char: Object(cells, char, char != 'o', None)
                           for char, cells in cells_by_char.items()}

        player = objects_by_char['@']
        item = objects_by_char['#']
        objects = [o for char, o in objects_by_char.items()]
        return Level(player, item, target, World(objects, size), level_name)

    def __init__(self, player, item, target, world, name):
        Game.__init__(self, player, world)
        self.item = item
        self.target = target
        self.name = name

    def run(self):
        while True:
            screen = self.name + '\n\n' + self.world.draw({self.target: 'X'})
            display(screen)
            if self.target in self.item.cells:
                screen += 'Level completed!'
                display(screen)
                get_key()
                raise LevelEnd()
            self.read_and_process_input()


class LevelSelection(Game):
    """
    Selection screen displayed as in-game level.
    """
    def __init__(self, levels):
        player = Object([(5, int(len(levels) / 2), 0, 0)], '@')
        objects = [player]
        self.levels = levels

        Game.__init__(self, player, World(objects, (10, len(levels), 1, 1)))

    def run(self):
        level_by_cell = {}
        for i, level in enumerate(levels):
            cell = (9, len(levels) - i - 1, 0, 0)
            level_by_cell[cell] = str(i + 1)

        while True:
            text = 'Select level\n\n' + self.world.draw(level_by_cell)
            display(text)
            self.read_and_process_input()

            player_cell = self.player.cells[0]
            if player_cell in level_by_cell:
                level_number = level_by_cell[self.player.cells[0]]
                level = self.levels[int(level_number) - 1]
                try:
                    Level.load(level).run()
                except LevelEnd:
                    continue


if __name__ == '__main__':
    levels = ['levels/' + level
              for level in sorted(os.listdir('levels'))
              if not level.startswith('.')]
    LevelSelection(levels).run()
