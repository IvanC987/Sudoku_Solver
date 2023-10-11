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

This program implements a Sudoku game utilizing libraries like Pygame and Pynput along with other 
python files that I had written.
Please read the README.md to get a better understanding of the overall structure/functionality of this program!


* Note: Truly unfortunate that I can't use pyautogui, had to use pynput instead. 
Due to when imported, pyautogui resized the size to a smaller scale, which was
less than desirable. After looking around, it seems like the reason why was because of
the design of pyautogui. It had a function called SetProcessDpiAwareness. 
Full discussion can be found here 
https://stackoverflow.com/questions/69711836/pyautogui-changing-my-window-size-when-i-import-it
"""


# The default grid holds the initial values of the puzzle, changing as new puzzles are being generated.
# This is also used to mark the initial values such that when drawn on screen, it would have a distinctive color
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

# grid holds the values that user entered, answer holds the answer to the puzzle and placed_notes is a
# 3d array that holds the notes the user placed when the "Note" button is used below
grid = [i[:] for i in DEFAULT_GRID]
answer = solve(DEFAULT_GRID)
placed_notes = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]

# Can be shortened but looks better like this but personally, I think this looks better
# First 9 columns represent the x coordinate and the last column represents the y coordinate with respect
# to the placement of the values within the grid
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


# Most of the following variable's name is pretty self-explanatory. Will briefly go over some non-obvious ones
# content_x and content_y are used in the calc_grid_pos function. Content_y is also used with the SCROLL_SPEED variable
# Value is a variable that contains the keyboard event when user enters a number
# x_click and y_click holds the coordinate positions when the user clicks on the screen
# The three values of "highlight" represents if to highlight and the coordinates of where to highlight
# x_offset and y_offset is used to offset the coordinate of the mouse/cursor due to slight inaccuracies
# x and y represents the row/column we are dealing with
# The remaining variables are used in association with the implemented buttons within the program
SCROLL_SPEED = 10
SCREEN_SIZE = 1000, 600
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
complete = False
levels = ["Easy", "Medium", "Hard"]  # Use mod 3 to get the difficulty


# First, initialize the pygame window
# Then, display the screen, set caption/Icon, and also creating the font that would be used in this project
py.init()
screen = py.display.set_mode(SCREEN_SIZE, py.RESIZABLE)
icon = py.image.load("SudokuIconImage.jpg")
py.display.set_icon(icon)
py.display.set_caption("Sudoku Project")
font1 = py.font.SysFont("comicsans", 40)  # This is for general purpose, used mainly for grid values
font2 = py.font.SysFont("verdana", 20)  # This is for Button's Label
font3 = py.font.SysFont("comicsans", 15)  # This is for the "Note" button
font4 = py.font.SysFont("verdana", 15)  # This is for console text


def calculate_grid_position() -> tuple:
    """
    This function calculates and return the coordinate position of the upper left-hand corner of the sudoku grid

    :return: Tuple in the format of (x_coordinate, y_coordinate)
    """
    # Calculate the center of the screen
    screen_center_x = screen.get_width() // 2
    screen_center_y = screen.get_height() // 2

    # Calculate the position of the grid based on screen size
    grid_x = screen_center_x - ((cell_size * 9) // 2) - content_x
    grid_y = screen_center_y - ((cell_size * 9) // 2) - content_y

    return grid_x, grid_y


initial_x, initial_y = calculate_grid_position()

# Creating the Console object first, this will print out messages to the user
console = Console(screen, centered_coords[2][0] - 250 + initial_x, centered_coords[2][-1] + initial_y, 200,
                  cell_size * 5, font4)
console.add_message("Welcome to this project!")


def draw_value(x_val: int, y_val: int, val: int, default: int) -> None:
    """
    This function uses the coordinate to draw the value on the grid

    :param x_val: x_coordinate position
    :param y_val: y_coordinate position
    :param val: user-keyed value
    :param default: checks if the value is from default grid
    :return: None
    """

    # If default == 0, then that means this is a default value, draw it in a dark-red color
    # elif default == 1, then that means it is a value placed by the user, draw it in black
    # Finally, the default would be 2, triggering else. This means the user has entered the "Note" mode
    if default == 0:
        text1 = font1.render(str(val), 1, (100, 0, 5))
    elif default == 1:
        text1 = font1.render(str(val), 1, (0, 0, 0))
    else:
        text1 = font3.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x_val, y_val))


def highlight_cells(row: int, column: int) -> None:
    """
    This function highlights certain cells within the grid based on where the user clicked

    :param row: This is the value of the current row within the grid
    :param column: This is the value of the current column within the grid
    :return: None
    """

    # First, calculate the position of x and y.
    # Find the necessary values, which includes height/width of rows/columns along with color and sizes
    grid_x, grid_y = calculate_grid_position()
    height = centered_coords[-1][-1] + 50
    width = centered_coords[0][1] - centered_coords[0][0]
    top = centered_coords[0][-1] + 50
    sub_size = cell_size * 3
    color = "#00B2FF"
    sub_coordinates = [
        [[3, 3], [171, 3], [339, 3]],
        [[3, 171], [171, 171], [339, 171]],
        [[3, 339], [171, 339], [339, 339]],
    ]

    # Highlights the column
    py.draw.rect(screen, color, py.Rect(column * cell_size + grid_x + 7, top + grid_y - 47, width, height), cell_size)

    # Highlights the row
    py.draw.rect(screen, color, py.Rect(top + grid_x - 47, row * cell_size + grid_y + 7, height, width), cell_size)

    coordinate = sub_coordinates[(row // 3)][(column // 3)]
    # Highlights the sub grid
    py.draw.rect(screen, color, py.Rect(coordinate[0] + grid_x, coordinate[1] + grid_y, sub_size, sub_size), sub_size)

    # Color current cell differently
    py.draw.rect(screen, "#0347FF", py.Rect(column * cell_size + grid_x + 7, row * cell_size + grid_y + 7,
                                            cell_size, cell_size), cell_size)


def is_solved(expected: list[list[int]], given: list[list[int]]) -> bool:
    """
    This function checks if the grid is solved by comparing the existing values within the grid to the answer.

    :param expected: This holds the answer
    :param given: This is the current grid that we are comparing
    :return: Returns a boolean, indicating whether the grid is now solved
    """

    for i in range(len(expected)):
        for j in range(len(expected[i])):
            if expected[i][j] != given[i][j]:
                return False

    return True


def automate(puzzle: list[list[int]], row, column, left, right) -> list:
    """
    This function automates the solving process by using the two imported libraries, pynput and time

    :param puzzle: This holds the current grid
    :param row: Current row
    :param column: Current column
    :param left: Boolean value representing if we need to move left
    :param right: Boolean value representing if we need to move right
    :return: Return a list that contains the updated values of variables like [True, row, column, left, right]
    """

    # First, instantiate the controller class from pynput
    keyboard = Controller()
    time.sleep(0.02)

    # Check if we are moving this. This occurs when we are at the last column, needing to move back to the first column
    if left:
        if column != 0:
            keyboard.press(Key.left)
            keyboard.release(Key.left)
            column -= 1
        else:
            left = False
    # Checks if we are now at the last column, we move down one row and set left to True
    elif column == 9:
        keyboard.press(Key.down)
        keyboard.release(Key.down)
        row += 1
        left = True
    # Checks if we are moving right. This is used when we are filling in the grid, moving right as we fill in values
    elif right:
        keyboard.press(Key.right)
        keyboard.release(Key.right)
        column += 1
        right = False
    # The last case, where we are just filling in the grid
    else:
        keyboard.press(str(puzzle[row][column]))
        keyboard.release(str(puzzle[row][column]))
        right = True

    # Now return the following values. The "if" condition checks if we have completed filled in everything, if not
    # we update the variables and return them as needed
    # If we are finished, the returned list would reset the global variables such that we can continue to solve more
    # puzzles when needed
    if row < 9 or column < 9:
        return [True, row, column, left, right]
    return [False, 0, 0, False, False]


def create_buttons():
    """
    This function creates all the necessary buttons within this program. "Note", "Solve", "Generate", and "Mode"

    :return: None
    """

    # First, globalize the required variables
    global DEFAULT_GRID, answer, placed_notes, grid, value, x_click, y_click, now_solve, \
        auto_row, auto_column, move_left, move_right, gen_click_time, note, difficulty, mode, complete

    # Calculate x, y position based on the screen first
    grid_x, grid_y = calculate_grid_position()

    # Draw the console first and checks certain conditions
    console.draw(centered_coords[2][0] - 250 + grid_x, centered_coords[2][-1] + grid_y)
    clear_b = Button(screen, centered_coords[2][0] - 250 + grid_x + console.width // 4,
                     centered_coords[2][-1] + grid_y + console.height * 1.1, 100, 40)
    clear_b.draw("#7E84F7")
    clear_b.add_text(font2, text="Clear", x_shift=25, y_shift=6)
    if clear_b.clicked(x_click - x_offset, y_click - y_offset):
        console.clear_message()
        x_click = 0

    # Draw the "Note" button and checks condition as needed
    note_b = Button(screen, centered_coords[0][0] + grid_x, centered_coords[-1][-1] + grid_y + 100, 100, 40)
    note_b.draw("#7E84F7")
    note_b.add_text(font2, text="Note", x_shift=27, y_shift=6)
    if note_b.clicked(x_click - x_offset, y_click - y_offset):
        note = False if note else True
        console.add_message(f"Note is now {note}")
        x_click = 0

    # Handling the "Solve" button is complex due to the need for a step-by-step solving animation.
    # Initially, calling the solver within this condition caused the interface to freeze for around 8 seconds
    # before displaying the solved puzzle all at once.
    # To provide a smoother user experience, I separated
    # the solving process into smaller steps, allowing the user to see the grid being solved incrementally.
    # Several variables and logic are involved to control this animation.
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
                console.add_message("Invalid puzzle. Try again")
                go = False
                x_click = 0
            temp = solve(grid)
            if temp == [[]]:
                console.add_message("No solution to this puzzle")
                go = False
                x_click = 0
            answer = temp
        if go:
            time.sleep(0.5)
            console.add_message("Now solving")
            x_click = centered_coords[0][0] + grid_x
            y_click = centered_coords[0][-1] + grid_y
            now_solve = True
            note = False

    # The "Generate" button is pretty self-explanatory. It checks if the user clicked it once, to generate a new puzzle,
    # or if it was double-clicked, to adjust the difficulty level of the puzzle.
    generate_b = Button(screen, centered_coords[0][4] + grid_x + 21, centered_coords[-1][-1] + grid_y + 100, 100, 40)
    generate_b.draw("#7E84F7")
    generate_b.add_text(font2, text="Generate", x_shift=3, y_shift=6)
    if generate_b.clicked(x_click - x_offset, y_click - y_offset) and time.time() - gen_click_time < 0.2:
        difficulty += 1
        console.add_message(f"Difficulty: {levels[difficulty % 3]}")
        DEFAULT_GRID = generate_puzzle(levels[difficulty % 3])
        grid = [i[:] for i in DEFAULT_GRID]
        answer = solve(DEFAULT_GRID)
        placed_notes = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
        x_click = 0
        complete = False
    elif generate_b.clicked(x_click - x_offset, y_click - y_offset):
        if abs(gen_click_time - time.time()) < 1:
            console.add_message("Please wait 1s")
        else:
            gen_click_time = time.time()
            DEFAULT_GRID = generate_puzzle(levels[difficulty % 3])
            grid = [i[:] for i in DEFAULT_GRID]
            answer = solve(DEFAULT_GRID)
            placed_notes = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
            console.add_message("New puzzle generated")
        x_click = 0
        complete = False

    # Here I have 2 modes
    # Mode 0: This is the mode by default where the user can ask the program to generate a puzzle on varying difficulty
    # Mode 1: This is the mode where the user can enter a puzzle to ask the program to solve it
    mode_b = Button(screen, centered_coords[0][6] + grid_x + 29, centered_coords[-1][-1] + grid_y + 100, 100, 40)
    mode_b.draw("#7E84F7")
    mode_b.add_text(font2, text="Mode", x_shift=24, y_shift=6)
    if mode_b.clicked(x_click - x_offset, y_click - y_offset):
        mode += 1
        complete = False
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
            console.add_message("Now in mode 1")
        else:
            DEFAULT_GRID = generate_puzzle(levels[difficulty % 3])
            grid = [i[:] for i in DEFAULT_GRID]
            answer = solve(DEFAULT_GRID)
            placed_notes = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
            console.add_message("Now in mode 0")
        x_click = 0


def background() -> None:
    """
    This function draws the entire background, which includes the main grid along with the values
    contained within

    :return: None
    """
    global complete

    screen.fill(py.Color("white"))

    # Calculate the grid position
    grid_x, grid_y = calculate_grid_position()

    # Checks if the condition to highlight cells are met
    if highlight[0]:
        highlight_cells(highlight[1], highlight[2])

    # Reason why py.Rect() has +10 is so that it lines up evenly. Remove and notice the difference
    py.draw.rect(screen, py.Color("black"), py.Rect(grid_x, grid_y, cell_size * 9 + 10, cell_size * 9 + 10), 10)
    count = 0
    # The cells would have dimensions of 56x56 pixels
    while (count * cell_size) < cell_size * 9:
        line_width = 3 if count % 3 != 0 else 7
        py.draw.line(screen, py.Color("black"), py.Vector2((count * cell_size) + grid_x + 5, grid_y),
                     py.Vector2((count * cell_size) + grid_x + 5, cell_size * 9 + grid_y), line_width)
        py.draw.line(screen, py.Color("black"), py.Vector2(grid_x, (count * cell_size) + grid_y + 5),
                     py.Vector2(cell_size * 9 + grid_x, (count * cell_size) + grid_y + 5), line_width)
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

    # Checks if the grid is completed
    if count == 0 and valid_grid(grid) and not complete:
        console.add_message("Grid complete!")
        complete = True

    # This checks/adds the values within cells when the user enables "Note"
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                continue
            count = 0
            for k in range(1, 10):
                if placed_notes[i][j][k - 1] != 0:
                    draw_value(centered_coords[i][j] + grid_x - 9 + (count % 3) * 15,
                               centered_coords[i][-1] + grid_y + 3 + (count // 3) * 15, placed_notes[i][j][k - 1], 3)
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
                content_y -= SCROLL_SPEED
            elif event.button == 5:  # Scroll down
                content_y += SCROLL_SPEED
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
    if centered_coords[0][0] - 30 <= (x_click - temp_x) <= centered_coords[0][-2] + 30 \
            and centered_coords[0][-1] - 25 <= (y_click - temp_y) <= centered_coords[-1][-1] + 25:
        highlight[0] = True
        for i in range(0, 9):
            if centered_coords[i][-1] - 30 <= (y_click - temp_y):
                x = i
            if centered_coords[0][i] - 30 <= (x_click - temp_x):
                y = i
        highlight[1:] = [x, y]
        if value != -1 and DEFAULT_GRID[x][y] == 0 and note:
            placed_notes[x][y][value - 1] = value
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
    loop()
