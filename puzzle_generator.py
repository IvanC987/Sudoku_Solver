from random import randint, sample
from sudoku_solver import valid_position, solve

"""
Unfortunately after many attempts, my personal implementation of fill_puzzle that generated a 
randomized 9x9 sudoku grid doesn't quite work out. 
It works, however it takes around a few seconds on average to generate one, which is too slow
for this. The following function that generates a randomized grid is thanks to -Alain T.
who provided the code on StackOverflow. The original code can be found at 
https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python
"""

base = 3


def pattern(r, c): return (base*(r % base)+r//base+c) % 9


def shuffle(s): return sample(s, len(s))


def fill_puzzle() -> list[list[int]]:
    """
    This is the function provided by Alain T.

    :return: 2d list of ints that represents the filled puzzle
    """
    rBase = range(base)
    rows = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base*base+1))

    # produce board using randomized baseline pattern
    return [[nums[pattern(r, c)] for c in cols] for r in rows]


def fill_puzzle2() -> (list[list[int]], list[list[int]]):
    """
    My version, as previously mentioned, works, but due to its randomized behavior, it can take between
    a few milliseconds to generate a puzzle up to a few seconds.

    :return: 2d list of ints that represents the randomized puzzle
    """
    grid = [[0 for _ in range(9)] for _ in range(9)]

    count = 0
    while True:
        i, j, val = randint(0, 8), randint(0, 8), randint(1, 9)
        if grid[i][j] == 0 and valid_position(grid, i, j, val):
            grid[i][j] = val
            count += 1

        if count == 30:
            answer = solve(grid)
            if answer != [[]]:
                break
            else:
                count = 0
                grid = [[0 for _ in range(9)] for _ in range(9)]
                print("No solution found")

    return grid, answer


def generate_puzzle(difficulty: str) -> list[list[int]]:
    """
    This is the function that takes in the randomized grid and removes random values to create a puzzle
    * Note- A slight optimization, if you look over the main file, regardless of whether the user submitted a
    puzzle or if it was a generated puzzle, the "solve" method from the sudoku_solver.py was called on the puzzle.
    So the initially completed grid, which could've been stored in a variable and returned as well, was not used at all.
    The reason was because I initially planned to use an API to generate a puzzle, however due to some difficulties, I
    had to give up on that, but the main solving logic was already implemented. However, for a scale of this size, there
    isn't much of an impact on performance.

    :param difficulty: This is a string that represents the difficulty that user desires
    :return: 2d list of ints that has a certain amount of values removed, based on the difficulty parameters
    """
    board = fill_puzzle()
    values = {
        "Easy": (38, 42),
        "Medium": (33, 37),
        "Hard": (28, 33),
    }

    # Here we remove a certain amount of values based on the difficulty desired
    remove = 81 - randint(values[difficulty][0], values[difficulty][1])
    while remove > 0:
        i, j = randint(0, 8), randint(0, 8)
        if board[i][j] != 0:
            board[i][j] = 0
            remove -= 1

    return board


