import snakelib

width = 0  # initialized in play_animation
height = 0  # initialized in play_snake
ui = None  # initialized in play_animation
SPEED = 20
keep_running = True
x = 0
y = 0
input = 1


def draw():
    global input, x, y
    if input % 2 != 0:
        ui.clear()
        ui.place(x,y,ui.SNAKE)
    if input % 2 == 0:
        ui.clear()
        ui.place(x,y,ui.FOOD)
    ui.show()


def play_animation(init_ui):
    global width, height, ui, keep_running, x, y, input
    ui = init_ui
    width, height = ui.board_size()
    while keep_running:
        ui.show()
        event = ui.get_event()
        if event.name == "alarm":
            draw()
            x = x + 1
            if x == width and y == height -1:
                x = 0
                y = 0
            if x == width :
                x = 0
                y = y + 1
        if event.name == 'other' and event.data == 'space':
            input += 1
        ui.show()
        # make sure you handle the quit event like below,
        # or the test might get stuck in an infinite loop
        if event.name == "quit":
            keep_running = False


if _name_ == "_main_":
    # do this if running this module directly
    # (not when importing it for the tests)
    ui = snakelib.SnakeUserInterface(10, 10)
    ui.set_animation_speed(SPEED)
    play_animation(ui)