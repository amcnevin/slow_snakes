from collections import deque
from random import randint
from enum import Enum
from appJar import gui


class Bearing(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class Game:
    bearing = Bearing.EAST
    body = deque()
    length = 1
    x_pos = None
    y_pos = None
    dead = False
    grid_x = None
    grid_y = None

    cookie_x = None
    cookie_y = None

    def __init__(self, x, y):
        """
        initialize the game state
        :param x: grid x value
        :param y: grid y value
        """
        self.grid_x = x
        self.grid_y = y
        self.x_pos = grid_x / 2
        self.y_pos = grid_y / 2

    def tick(self):
        """
        tick of the clock
        """
        if self.is_alive():
            self.move_snake()
            self.gen_new_cookie()
            self.determine_if_dead()

    def move_snake(self):
        """
        move the snake, check for cookie, and grow body
        """
        if self.bearing is Bearing.NORTH:
            self.x_pos = self.x_pos - 1
        elif self.bearing is Bearing.SOUTH:
            self.x_pos = self.x_pos + 1
        elif self.bearing is Bearing.WEST:
            self.y_pos = self.y_pos - 1
        elif self.bearing is Bearing.EAST:
            self.y_pos = self.y_pos + 1

        if self.x_pos == self.cookie_x and self.y_pos == self.cookie_y:
            self.length += 1
            self.cookie_x = None
            self.cookie_y = None

        if len(self.body) == self.length:
            self.body.pop()
            self.body.insert(0, (self.x_pos, self.y_pos),)
        else:
            self.body.insert(0, (self.x_pos, self.y_pos),)

    def gen_new_cookie(self):
        """
        do we need to generate a new cookie, if so randomly generate
        """
        if self.cookie_x is None:
            self.cookie_x = randint(0, grid_x-1)
            self.cookie_y = randint(0, grid_y-1)

    def is_cookie_at_pos(self, x, y):
        """
        is there a cookie at this coord?
        :param x: x coord
        :param y: y coord
        :return: boolean if there's a cookie
        """
        return self.cookie_x == x and self.cookie_y == y

    def is_snake_at_pos(self, x, y):
        """
        is the snake's head or body at this coordinate?
        :param x: x coord
        :param y: y coord
        :return: boolean whether snake occupies this coord
        """
        if self.x_pos == x and self.y_pos == y:
            return True
        if (x, y) in self.body:
            return True
        return False

    def determine_if_dead(self):
        """
        check to make sure snake hasn't hit any boundaries
        or itself
        """
        if self.x_pos < 0 or self.x_pos > self.grid_x:
            self.dead = True
        if self.y_pos < 0 or self.y_pos > self.grid_y:
            self.dead = True

        if (self.x_pos, self.y_pos) in self.body:
            self.dead = True

    def is_alive(self):
        """
        :return: boolean if its alive
        """
        return not self.dead


def key_press(key):
    """
    from a provided key, change the snake's bearing
    :param key:
    """
    if key == "<Up>" and snakes.bearing != Bearing.SOUTH:
        snakes.bearing = Bearing.NORTH
    elif key == "<Down>" and snakes.bearing != Bearing.NORTH:
        snakes.bearing = Bearing.SOUTH
    elif key == "<Left>" and snakes.bearing != Bearing.EAST:
        snakes.bearing = Bearing.WEST
    elif key == "<Right>" and snakes.bearing != Bearing.WEST:
        snakes.bearing = Bearing.EAST


def redraw():
    """
    Redraw ths labels from the Game's state
    """
    global grid_x
    global grid_y
    for x in range(grid_x):
        for y in range(grid_y):
            name = str(x) + "-" + str(y)
            if snakes.is_snake_at_pos(x, y):
                if snakes.is_alive():
                    app.setLabelBg(name, "green")
                else:
                    app.setLabelBg(name, "red")
            elif snakes.is_cookie_at_pos(x, y):
                app.setLabelBg(name, "yellow")
            else:
                app.setLabelBg(name, "black")


def init_grid():
    """
    Initializes Grid of Labels
    """
    global grid_x
    global grid_y
    for x in range(grid_x):
        for y in range(grid_y):
            name = str(x) + "-" + str(y)
            app.addEmptyLabel(name, row=x, column=y)
            app.setLabelBg(name, "black")


def init_keys():
    """
    Initializes Key Bindings
    """
    app.bindKey("<Up>", key_press)
    app.bindKey("<Down>", key_press)
    app.bindKey("<Left>", key_press)
    app.bindKey("<Right>", key_press)


if __name__ == "__main__":

    grid_x = 20
    grid_y = 20

    snakes = Game(grid_x, grid_y)

    app = gui("Slow Snakes", "250x250")
    app.setBg("black")
    init_keys()

    app.registerEvent(snakes.tick)
    app.registerEvent(redraw)
    # Todo why can't we speed this up?!?
    app.setPollTime(1)
    init_grid()

    app.go()







