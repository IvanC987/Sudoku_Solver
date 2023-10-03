import pygame as py
import sys


"""
Sudoku Game

This program implements a Sudoku game utilizing Pygame and along with other 
python files that I had written.
"""


# Remember to add ICON IMAGE AND TITLE!
# Each time I change the value, print it out in console to make sure it's correct
# grid = [
#     [7, 8, 0, 4, 0, 0, 1, 2, 0],
#     [6, 0, 0, 0, 7, 5, 0, 0, 9],
#     [0, 0, 0, 6, 0, 1, 0, 7, 8],
#     [0, 0, 7, 0, 4, 0, 2, 6, 0],
#     [0, 0, 1, 0, 5, 0, 9, 3, 0],
#     [9, 0, 4, 0, 6, 0, 0, 0, 5],
#     [0, 7, 0, 3, 0, 0, 0, 1, 2],
#     [1, 2, 0, 0, 0, 7, 4, 0, 0],
#     [0, 4, 9, 2, 0, 6, 0, 0, 7]
# ]

grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Can be shortened but looks better like this but personally, I think this looks better
# Purpose of this 2d list is that it holds the coordinates of the centered cell
# x coord are the first 9, and the final value being the y direction
centered_coordinates = [
    [23, 77, 132, 190, 245, 299, 358, 413, 466, 6],
    [23, 77, 132, 190, 245, 299, 358, 413, 466, 60],
    [23, 77, 132, 190, 245, 299, 358, 413, 466, 116],
    [23, 77, 132, 190, 245, 299, 358, 413, 466, 174],
    [23, 77, 132, 190, 245, 299, 358, 413, 466, 227],
    [23, 77, 132, 190, 245, 299, 358, 413, 466, 283],
    [23, 77, 132, 190, 245, 299, 358, 413, 466, 341],
    [23, 77, 132, 190, 245, 299, 358, 413, 466, 394],
    [23, 77, 132, 190, 245, 299, 358, 413, 466, 450],
]


# Scroll speed controls the scrolling rate
# Both content_x and y are used in the calc_grid_pos function. Content_y is also used with the scroll_speed variable
# Value is a variable that contains the keyboard event when user enters a number
# x_click and y_click holds the coordinate positions when the user clicks on the screen
scroll_speed = 10
screen_size = 800, 600
content_x, content_y = 0, 0
value = 0
x_click, y_click = 0, 0

# First, initialize the pygame window
# Then, display the screen, set caption, and also creating the font that would be used in this project
py.init()
screen = py.display.set_mode(screen_size, py.RESIZABLE)
py.display.set_caption("Sudoku Project")
font1 = py.font.SysFont("comicsans", 40)


def calculate_grid_position() -> tuple:
    """
    This function calculates and return the coordinate position of the upper left-hand corner of the sudoku grid

    :return: Tuple in the format of (x_coordinate, y_coordinate)
    """
    # Calculate the center of the screen
    screen_center_x = screen.get_width() // 2
    screen_center_y = screen.get_height() // 2

    # Calculate the position of the grid based on screen size
    grid_x = screen_center_x - 252 - content_x
    grid_y = screen_center_y - 252 - content_y

    return grid_x, grid_y


def background() -> None:
    """
    This function draws the entire background, which includes the main grid along with the values
    contained within

    :return: None
    """

    global value, x_click, y_click
    screen.fill(py.Color("white"))

    # Calculate the grid position
    grid_x, grid_y = calculate_grid_position()

    # Reason why py.Rect() has +10 is so that it lines up evenly. Remove and notice the difference
    py.draw.rect(screen, py.Color("black"), py.Rect(grid_x, grid_y, 504 + 10, 504 + 10), 10)
    count = 0
    # The cells would have dimensions of 56x56 pixels
    while (count * 56) < 504:
        line_width = 3 if count % 3 != 0 else 7
        py.draw.line(screen, py.Color("black"), py.Vector2((count * 56) + grid_x + 5, grid_y),
                     py.Vector2((count * 56) + grid_x + 5, 504 + grid_y), line_width)
        py.draw.line(screen, py.Color("black"), py.Vector2(grid_x, (count * 56) + grid_y + 5),
                     py.Vector2(504 + grid_x, (count * 56) + grid_y + 5), line_width)
        count += 1

    # Populating the grid based on the current values we have
    for i in range(len(grid)):
        for j in range(9):
            if grid[i][j] != 0:
                draw_value(centered_coordinates[i][j] + grid_x, centered_coordinates[i][-1] + grid_y, grid[i][j])


def draw_value(x: int, y: int, val: int) -> None:
    """
    This function uses the coordinate to draw the value on the grid

    :param x: x_coordinate position
    :param y: y_coordinate position
    :param val: user-keyed value
    :return: None
    """

    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x, y))


def highlight_cells(row: int, column: int) -> None:
    pass
# call highlight cells first then draw the grid?
# Possibly create a small 2d list that holds coordinates for the sub-grids to highlight?


def loop() -> None:
    """
    This is the main function that connects everything together.
    It handles keyboard events, call the background function, update the grid based on user response, among others

    :return: None
    """

    # Globalize the required variables and iterates through the events to handle them
    global content_y, content_x, value, x_click, y_click
    for event in py.event.get():
        # If "X" is clicked on the window, exits the program
        if event.type == py.QUIT:
            sys.exit()
        # Resizes the window as needed by the user
        elif event.type == py.VIDEORESIZE:
            new_width, new_height = event.size
            py.display.set_mode((new_width, new_height), py.RESIZABLE)
        # Checks if the users left-clicked or scrolled
        elif event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left Click
                # Reason for the addition is because there are some slight discrepancies
                # between the given coordinates and where the user actually clicked.
                x_click, y_click = event.pos[0] - 12, event.pos[1] - 30
            elif event.button == 4:  # Scroll up
                content_y -= scroll_speed
            elif event.button == 5:  # Scroll down
                content_y += scroll_speed
        # Checks if the user pressed keys like left, right, up, down, 1, 2, 3, etc.
        elif event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                pass
            if event.key == py.K_RIGHT:
                pass
            if event.key == py.K_UP:
                pass
            if event.key == py.K_DOWN:
                pass
            if event.key == py.K_1:
                value = 1
            if event.key == py.K_2:
                value = 2
            if event.key == py.K_3:
                value = 3
            if event.key == py.K_4:
                value = 4
            if event.key == py.K_5:
                value = 5
            if event.key == py.K_6:
                value = 6
            if event.key == py.K_7:
                value = 7
            if event.key == py.K_8:
                value = 8
            if event.key == py.K_9:
                value = 9

    # Here, I performed some complex calculation that took me around 2 days to get everything working the way I liked,
    # Unfortunately it would take too long to explain everything in detail. I will just go over the basics
    # First, find the coordinate of the upper-left part of the grid
    temp_x, temp_y = calculate_grid_position()
    # Checks if the user clicked within the grid
    if centered_coordinates[0][0]-30 <= (x_click - temp_x) <= centered_coordinates[0][-2] + 30 \
            and centered_coordinates[0][-1]-25 <= (y_click - temp_y) <= centered_coordinates[-1][-1]+25:
        # Instantiate x and y values, these would represent the indicies of the grid
        x, y = 0, 0
        for i in range(1, 9):
            if centered_coordinates[i][-1] - 30 <= (y_click - temp_y):
                x = i
            if centered_coordinates[0][i] - 30 <= (x_click - temp_x):
                y = i
        if value == 0:
            highlight_cells(x, y)
        else:
            # After iteration, it changes the value at that location, which would be reflected on the window
            # when the background() function is called again at the bottom, and setting the value back to 0
            grid[x][y] = value
            value = 0

    background()
    py.display.flip()


while True:
    loop()


