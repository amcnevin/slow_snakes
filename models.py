from random import randint
from collections import deque
from enum import Enum

class Bearing(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class Cookie:

    x = None
    y = None

    def __init__(self):
        pass

    def new_cookie(self, grid_x, grid_y):
        """
        do we need to generate a new cookie, if so randomly generate
        """
        if self.x is None:
            self.x = randint(0, grid_x-1)
            self.y = randint(0, grid_y-1)

    def reset_cookie(self):
        self.x = None
        self.y = None

    def is_cookie_at_pos(self, x_pos, y_pos):
        """
        is there a cookie at this coord?
        :param x: x coord
        :param y: y coord
        :return: boolean if there's a cookie
        """
        return self.x == x_pos and self.y == y_pos


class Snake:
    x_pos = None
    y_pos = None
    bearing = Bearing.EAST
    body = deque()
    head = (x_pos, y_pos)
    length = 1
    alive = True

    def __init__(self, grid_x, grid_y):
        self.x_pos = grid_x / 2
        self.y_pos = grid_y / 2

    def move_snake(self, cookie):
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

        if cookie.is_cookie_at_pos(self.x_pos, self.y_pos):
            self.length += 1
            cookie.reset_cookie()

        if len(self.body) == self.length:
            self.body.pop()
            self.body.insert(0, (self.x_pos, self.y_pos),)
        else:
            self.body.insert(0, (self.x_pos, self.y_pos),)

    def is_snake_at_pos(self, x, y):
        if self.x_pos == x and self.y_pos == y:
            return True
        if (x, y) in self.body:
            return True
        return False

    def determine_if_dead(self, grid_x, grid_y):
        if self.x_pos < 0 or self.x_pos > grid_x:
            self.alive = False
        if self.y_pos < 0 or self.y_pos > grid_y:
            self.alive = False
        #if (self.x_pos, self.y_pos) in self.body:
            #self.alive = False

    def is_alive(self):
        """
        :return: boolean if its alive
        """
        return self.alive
