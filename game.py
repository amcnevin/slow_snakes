from appJar import gui
from models import Cookie, Snake, Bearing


class Game:
    grid_x = None
    grid_y = None

    cookie = Cookie()
    snake = None
    def __init__(self, x, y):
        """
        initialize the game state
        :param x: grid x value
        :param y: grid y value
        """
        self.grid_x = x
        self.grid_y = y
        self.snake = Snake(grid_x, grid_y)

    def tick(self):
        """
        tick of the clock
        """
        if self.snake.is_alive():
            self.snake.move_snake(self.cookie)
            self.cookie.new_cookie(self.grid_x, self.grid_y)
            self.snake.determine_if_dead(self.grid_x, self.grid_y)
        print("Snake is {} at {} {} heading {}".format(self.snake.is_alive(), self.snake.x_pos, self.snake.y_pos, self.snake.bearing))

    def get_snake_bearing(self):
        return self.snake.bearing

    def set_snake_bearing(self, bearing):
        self.snake.bearing = bearing


def key_press(key):
    """
    from a provided key, change the snake's bearing
    :param key:
    """
    bearing = game.get_snake_bearing()
    if key == "<Up>" and bearing != Bearing.SOUTH:
        game.set_snake_bearing(Bearing.NORTH)
    elif key == "<Down>" and bearing != Bearing.NORTH:
        game.set_snake_bearing(Bearing.SOUTH)
    elif key == "<Left>" and bearing != Bearing.EAST:
        game.set_snake_bearing(Bearing.WEST)
    elif key == "<Right>" and bearing != Bearing.WEST:
        game.set_snake_bearing(Bearing.EAST)


def redraw():
    """
    Redraw ths labels from the Game's state
    """
    global grid_x
    global grid_y
    for x in range(grid_x):
        for y in range(grid_y):
            name = str(x) + "-" + str(y)
            if game.snake.is_snake_at_pos(x, y):
                if game.snake.is_alive():
                    app.setLabelBg(name, "green")
                else:
                    app.setLabelBg(name, "red")
            elif game.cookie.is_cookie_at_pos(x, y):
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

    game = Game(grid_x, grid_y)

    app = gui("Slow Snakes", "250x250")
    app.setBg("black")
    init_keys()

    app.registerEvent(game.tick)
    app.registerEvent(redraw)
    # Todo why can't we speed this up?!?
    app.setPollTime(1)
    init_grid()

    app.go()







