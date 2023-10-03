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


def fill_puzzle():
    rBase = range(base)
    rows = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base*base+1))

    # produce board using randomized baseline pattern
    return [[nums[pattern(r, c)] for c in cols] for r in rows]


def fill_puzzle2() -> (list[list[int]], list[list[int]]):
    grid = [[0 for _ in range(9)] for _ in range(9)]

    count = 0
    while True:
        i, j, val = randint(0, 8), randint(0, 8), randint(1, 9)
        if grid[i][j] == 0 and valid_position(grid, i, j, val):
            grid[i][j] = val
            count += 1

        if count == 30:
            print("B")
            print(grid)
            answer = solve(grid)
            print("A")
            if answer != [[]]:
                break
            else:
                count = 0
                grid = [[0 for _ in range(9)] for _ in range(9)]
                print("No solution found")

    # Then remove the values as needed.

    return grid, answer


def generate_puzzle(difficulty: str):
    board = fill_puzzle()
    values = {
        "Easy": (38, 42),
        "Medium": (33, 37),
        "Hard": (28, 33),
    }

    remove = 81 - randint(values[difficulty][0], values[difficulty][1])
    while remove > 0:
        i, j = randint(0, 8), randint(0, 8)
        if board[i][j] != 0:
            board[i][j] = 0
            remove -= 1

    return board


