import sys
import time
import pygame as py
from pynput.keyboard import Controller, Key
from button import Button
from console import Console
from sudoku_solver import solve, valid_grid
from puzzle_generator import generate_puzzle


"""
Sudoku Game

This program implements a Sudoku game utilizing Pygame and along with other 
python files that I had written.

When "Solve" button is clicked, make sure to click on first cell...
The mode button consists of two mode...
ADD TO THIS WHEN COMPLETED!

* Note: Truly unfortunate that I can't use pyautogui, had to use pynput instead. 
That's because when imported, pyautogui resized the size to a smaller scale, which was
less than desirable. After looking around, it seems like the reason why was because of
the design of pyautogui. It had a function called SetProcessDpiAwareness. 
Full discussion can be found here 
https://stackoverflow.com/questions/69711836/pyautogui-changing-my-window-size-when-i-import-it
"""


# Remember to add ICON IMAGE AND TITLE!
DEFAULT_GRID = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


grid = [i[:] for i in DEFAULT_GRID]
answer = solve(DEFAULT_GRID)
placed_notes = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]


# Can be shortened but looks better like this but personally, I think this looks better
# Purpose of this 2d list is that it holds the coordinates of the centered cell
# x coord are the first 9, and the final value being the y direction
centered_coords = [
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
screen_size = 1000, 600
content_x, content_y = 0, 0
value = -1
x_click, y_click = 0, 0
highlight = [False, 0, 0]
x_offset, y_offset = -13, -30
cell_size = 56
x, y = -1, -1
now_solve = False
auto_row, auto_column = 0, 0
move_left, move_right = False, False
difficulty = 0
note = False
gen_click_time = 0
mode = 0
levels = ["Easy", "Medium", "Hard"]  # Use mod 3 to get the difficulty


# First, initialize the pygame window
# Then, display the screen, set caption, and also creating the font that would be used in this project
py.init()
screen = py.display.set_mode(screen_size, py.RESIZABLE)
py.display.set_caption("Sudoku Project")
font1 = py.font.SysFont("comicsans", 40)
font2 = py.font.SysFont("verdana", 20)
font3 = py.font.SysFont("comicsans", 15)


def calculate_grid_position() -> tuple:
    """
    This function calculates and return the coordinate position of the upper left-hand corner of the sudoku grid

    :return: Tuple in the format of (x_coordinate, y_coordinate)
    """
    # Calculate the center of the screen
    screen_center_x = screen.get_width() // 2
    screen_center_y = screen.get_height() // 2

    # Calculate the position of the grid based on screen size
    grid_x = screen_center_x - ((cell_size*9)//2) - content_x
    grid_y = screen_center_y - ((cell_size*9)//2) - content_y

    return grid_x, grid_y


def draw_value(x_val: int, y_val: int, val: int, default: int) -> None:
    """
    This function uses the coordinate to draw the value on the grid

    :param x_val: x_coordinate position
    :param y_val: y_coordinate position
    :param val: user-keyed value
    :param default: checks if the value is from default grid
    :return: None
    """

    if default == 0:
        text1 = font1.render(str(val), 1, (100, 0, 5))
    elif default == 1:
        text1 = font1.render(str(val), 1, (0, 0, 0))
    else:
        text1 = font3.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x_val, y_val))


def highlight_cells(row: int, column: int) -> None:
    grid_x, grid_y = calculate_grid_position()
    height = centered_coords[-1][-1] + 50
    width = centered_coords[0][1] - centered_coords[0][0]
    top = centered_coords[0][-1] + 50
    sub_size = cell_size * 3
    color = "#1998FF"
    sub_coordinates = [
        [[3, 3], [171, 3], [339, 3]],
        [[3, 171], [171, 171], [339, 171]],
        [[3, 339], [171, 339], [339, 339]],
    ]

    # Highlights the column
    py.draw.rect(screen, color, py.Rect(column*cell_size+grid_x+7, top+grid_y-47, width, height), cell_size)

    # Highlights the row
    py.draw.rect(screen, color, py.Rect(top+grid_x-47, row * cell_size + grid_y + 7, height, width), cell_size)

    coordinate = sub_coordinates[(row // 3)][(column // 3)]
    # Highlights the sub grid
    py.draw.rect(screen, color, py.Rect(coordinate[0]+grid_x, coordinate[1] + grid_y, sub_size, sub_size), sub_size)

    # Color current cell differently
    py.draw.rect(screen, "#0300FF", py.Rect(column*cell_size + grid_x + 7, row*cell_size + grid_y + 7,
                                            cell_size, cell_size), cell_size)


def is_solved(expected: list[list[int]], given: list[list[int]]) -> bool:
    for i in range(len(expected)):
        for j in range(len(expected[i])):
            if expected[i][j] != given[i][j]:
                return False

    return True


def automate(puzzle: list[list[int]], row, column, left, right) -> list:
    keyboard = Controller()
    time.sleep(0.05)

    if left:
        if column != 0:
            keyboard.press(Key.left)
            keyboard.release(Key.left)
            column -= 1
        else:
            left = False
    elif column == 9:
        keyboard.press(Key.down)
        keyboard.release(Key.down)
        row += 1
        left = True
    elif right:
        keyboard.press(Key.right)
        keyboard.release(Key.right)
        column += 1
        right = False
    else:
        keyboard.press(str(puzzle[row][column]))
        keyboard.release(str(puzzle[row][column]))
        right = True

    if row < 9 or column < 9:
        return [True, row, column, left, right]
    return [False, 0, 0, False, False]


def create_buttons():
    global DEFAULT_GRID, answer, placed_notes, grid, value, x_click, y_click, now_solve, \
        auto_row, auto_column, move_left, move_right, gen_click_time, note, difficulty, mode
    grid_x, grid_y = calculate_grid_position()
    # Creating the Console, Note, Solve, Generate, and Mode button
    console = Console(screen, centered_coords[2][0] - 250 + grid_x, centered_coords[2][-1] + grid_y, 200,
                      cell_size*5, font2)
    console.draw()
    console.add_message("Temp", "black")

    note_b = Button(screen, centered_coords[0][0] + grid_x, centered_coords[-1][-1] + grid_y + 100, 100, 40)
    note_b.draw("#7E84F7")
    note_b.add_text(font2, text="Note", x_shift=27, y_shift=6)
    if note_b.clicked(x_click - x_offset, y_click - y_offset):
        note = False if note else True
        print(f"Note is now {note}")
        x_click = 0

    solve_b = Button(screen, centered_coords[0][2] + grid_x + 13, centered_coords[-1][-1] + grid_y + 100, 100, 40)
    solve_b.draw("#7E84F7")
    solve_b.add_text(font2, text="Solve", x_shift=24, y_shift=6)
    if now_solve:
        now_solve, auto_row, auto_column, move_left, move_right = \
            automate(answer, auto_row, auto_column, move_left, move_right)
    if solve_b.clicked(x_click - x_offset, y_click - y_offset):
        go = True
        if mode % 2 == 1:
            check = valid_grid(grid)
            if not check:
                print("Invalid puzzle. Try again")
                go = False
                x_click = 0
            temp = solve(grid)
            print("passed solve method")  # Solve can take a couple seconds. Tell user to wait
            if temp == [[]]:
                print("This puzzle have no solution. Try another one")
                go = False
                x_click = 0
            answer = temp
        if go:
            for starting in range(3, -1, -1):
                time.sleep(1)
                print(f"Starting in {starting}")
            x_click = centered_coords[0][0] + grid_x
            y_click = centered_coords[0][-1] + grid_y
            now_solve = True

    generate_b = Button(screen, centered_coords[0][4] + grid_x + 21, centered_coords[-1][-1] + grid_y + 100, 100, 40)
    generate_b.draw("#7E84F7")
    generate_b.add_text(font2, text="Generate", x_shift=3, y_shift=6)
    if generate_b.clicked(x_click - x_offset, y_click - y_offset) and time.time()-gen_click_time < 0.2:
        difficulty += 1
        print(f"Generate Clicked, difficulty is now {levels[difficulty % 3]}")
        DEFAULT_GRID = generate_puzzle(levels[difficulty % 3])
        grid = [i[:] for i in DEFAULT_GRID]
        answer = solve(DEFAULT_GRID)
        placed_notes = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
        x_click = 0
    elif generate_b.clicked(x_click - x_offset, y_click - y_offset):
        if abs(gen_click_time - time.time()) < 3:
            print("Please wait a few seconds before generation")
        else:
            gen_click_time = time.time()
            DEFAULT_GRID = generate_puzzle(levels[difficulty % 3])
            grid = [i[:] for i in DEFAULT_GRID]
            answer = solve(DEFAULT_GRID)
            placed_notes = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
            print("Generate Button Clicked")
        x_click = 0

    # mode = 1 Use this variable to keep track and switch between modes!
    mode_b = Button(screen, centered_coords[0][6] + grid_x + 29, centered_coords[-1][-1] + grid_y + 100, 100, 40)
    mode_b.draw("#7E84F7")
    mode_b.add_text(font2, text="Mode", x_shift=24, y_shift=6)
    if mode_b.clicked(x_click - x_offset, y_click - y_offset):
        mode += 1
        if mode % 2 == 1:
            DEFAULT_GRID = [
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
            grid = [i[:] for i in DEFAULT_GRID]
            placed_notes = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
            print("Now in mode 1")
        else:
            DEFAULT_GRID = generate_puzzle(levels[difficulty % 3])
            grid = [i[:] for i in DEFAULT_GRID]
            answer = solve(DEFAULT_GRID)
            placed_notes = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
            print("Now in mode 0")
        x_click = 0


def background() -> None:
    """
    This function draws the entire background, which includes the main grid along with the values
    contained within

    :return: None
    """
    screen.fill(py.Color("white"))

    # Calculate the grid position
    grid_x, grid_y = calculate_grid_position()

    if highlight[0]:
        highlight_cells(highlight[1], highlight[2])

    # Reason why py.Rect() has +10 is so that it lines up evenly. Remove and notice the difference
    py.draw.rect(screen, py.Color("black"), py.Rect(grid_x, grid_y, cell_size*9 + 10, cell_size*9 + 10), 10)
    count = 0
    # The cells would have dimensions of 56x56 pixels
    while (count * cell_size) < cell_size*9:
        line_width = 3 if count % 3 != 0 else 7
        py.draw.line(screen, py.Color("black"), py.Vector2((count * cell_size) + grid_x + 5, grid_y),
                     py.Vector2((count * cell_size) + grid_x + 5, cell_size*9 + grid_y), line_width)
        py.draw.line(screen, py.Color("black"), py.Vector2(grid_x, (count * cell_size) + grid_y + 5),
                     py.Vector2(cell_size*9 + grid_x, (count * cell_size) + grid_y + 5), line_width)
        count += 1

    # Call to create the buttons
    create_buttons()

    # Populating the grid based on the current values we have while checking if grid is complete
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if DEFAULT_GRID[i][j] != 0:
                draw_value(centered_coords[i][j] + grid_x, centered_coords[i][-1] + grid_y, grid[i][j], 0)
            elif grid[i][j] != 0:
                draw_value(centered_coords[i][j] + grid_x, centered_coords[i][-1] + grid_y, grid[i][j], 1)
            else:
                count += 1

    if count == 0 and valid_grid(grid):
        print("Grid complete!")

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                continue
            count = 0
            for k in range(1, 10):
                if placed_notes[i][j][k-1] != 0:
                    draw_value(centered_coords[i][j] + grid_x - 9 + (count % 3) * 15,
                               centered_coords[i][-1] + grid_y + 3 + (count // 3) * 15, placed_notes[i][j][k-1], 2)
                count += 1


def loop() -> None:
    """
    This is the main function that connects everything together.
    It handles keyboard events, call the background function, update the grid based on user response, among others

    :return: None
    """

    # Globalize the required variables and iterates through the events to handle them
    global content_y, content_x, value, x_click, y_click, highlight, x, y
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
                x_click, y_click = event.pos[0] + x_offset, event.pos[1] + y_offset
            elif event.button == 4:  # Scroll up
                content_y -= scroll_speed
            elif event.button == 5:  # Scroll down
                content_y += scroll_speed
        # Checks if the user pressed keys like left, right, up, down, 1, 2, 3, etc.
        elif event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                x_click -= cell_size
            if event.key == py.K_RIGHT:
                x_click += cell_size
            if event.key == py.K_UP:
                y_click -= cell_size
            if event.key == py.K_DOWN:
                y_click += cell_size
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
            if event.key == py.K_0:
                value = 0

    # Here, I performed some complex calculation that took me around 2 days to get everything working the way I liked,
    # Unfortunately it would take too long to explain everything in detail. I will just go over the basics
    # First, find the coordinate of the upper-left part of the grid
    temp_x, temp_y = calculate_grid_position()
    # Checks if the user clicked within the grid
    if centered_coords[0][0]-30 <= (x_click - temp_x) <= centered_coords[0][-2] + 30 \
            and centered_coords[0][-1]-25 <= (y_click - temp_y) <= centered_coords[-1][-1]+25:
        highlight[0] = True
        for i in range(0, 9):
            if centered_coords[i][-1] - 30 <= (y_click - temp_y):
                x = i
            if centered_coords[0][i] - 30 <= (x_click - temp_x):
                y = i
        highlight[1:] = [x, y]
        if value != -1 and DEFAULT_GRID[x][y] == 0 and note:
            placed_notes[x][y][value-1] = value
            value = -1
        elif value != -1 and DEFAULT_GRID[x][y] == 0:
            # After iteration, it changes the value at that location, which would be reflected on the window
            # when the background() function is called again at the bottom, and setting the value back to 0
            grid[x][y] = value
            placed_notes[x][y] = [0 for _ in range(9)]
            value = -1
    else:
        highlight[0] = False

    background()
    py.display.flip()


while True:
    # if len(easy_grid) < 10 or len(medium_grid) < 10 or len(hard_grid) < 10:
    #     create_puzzle()
    loop()
