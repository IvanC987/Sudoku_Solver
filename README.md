"# Sudoku_Solver" <br>
This program has 5 main files. <br>
1. sudoku_gui.py- <br>
This is where the main program is at, consisting of the GUI along with the required functions needed to run this project
Run this file to start the Sudoku Program
2. sudoku_solver.py- <br>
This python file contains two methods using within the main file. "solve" and "valid_grid" 
The former solves a given sudoku_puzzle, return [[]] if it's invalid, while the latter returns a boolean value when 
validating the grid
3. puzzle_generator.py- <br>
This python file contain several methods, the imported method, "generate_puzzle" is used to generate and return 
a puzzle based on the difficulty the user chose
4. button.py-
This python file holds the custom class, buttons, where it allows the creation of buttons within the project. 
the 5 buttons within the project is "Clear", "Note", "Solve", "Generate", and "Mode"
5. console.py-
This final python file is another custom class that creates a window and prints out messages
to the user, notifying them of the changes within the program


The primary usage of this program is to create a sudoku puzzle of varying difficulties
for users to solve, or, if the user desires, it allows the user to enter a sudoku puzzle and solve it for them. <br> <br>

Libraries used within this project are sys, time, pygame, and pynput <br> <br>

Main Features:
1. "Clear" Button
Pretty self-explanatory of its usage
2. "Note" Button
Clicking this buttons turns it on and off. When on, the user would be able to note down possible values that may be 
placed within a certain cell
3. "Solve" Button
This button automatically solves either the generated puzzle or a given puzzle. If the puzzle cannot be solved or if 
given an invalid grid, a corresponding message would appear on the "console"
4. "Generate" Button:
Clicking this button once would generate a puzzle at the set difficulty, Easy by default. When double-clicked, the 
difficulty would change, going in the order of Easy -> Medium -> Hard -> Easy...
5. "Mode" Button:
Clicking this button would allow you to switch between Mode 1 and Mode 2. Mode 1 is the default mode, where this program
will generate a puzzle for the user to solve. Clicking on Mode will switch to Mode 2, which clears the grid and allows 
the user to enter in values as needed for the program to solve. 

<br> <br>

Functions

<br> <br>
All imported local functions had been briefly discussed above. The following is a short description of each
function within the main file, sudoku_gui.py

1. calculate_grid_position()-
This function is used to calculate the x, y positions. Mainly used when the user resizes the window, scrolls up/down, 
along with placing numbers/buttons within the interface
2. draw_value()-
This function takes in several parameters, including the value and x-y coordinate position and 
draw numbers on the interface accordingly
3. highlight_cells()-
This function highlights the cells within the grid when clicked. It highlights the row, column, subgrid, 
and the cell the user has clicked on
4. is_solved()-
This function checks if the puzzle is now solved
5. automate()-
This function is the core of the "Solve" button. It takes in several parameters and fills in the grid according to the 
"answer" variable, which contains the fully solved puzzle
6. create_buttons()-
This function, as indicated by its name, creates/draws the buttons on the interface
7. background()-
This function draws the main background of this interface, including the grid and function call draw_values
8. loop()-
This function mainly handle keyboard events and continuously loops as long as the user does not exit the program.



Note- Please make sure to use this program as intended. Such as not clicking on "Solve" multiple times while
the puzzle is being solved, or clicking elsewhere on the screen while the puzzle is being solved. 