import time
from pynput.keyboard import Controller, Key


"""
This file contain multiple functions, of which, "solve" and "valid_grid" is used by the main file, sudoku_gui.py
The remaining functions are used for testing/other purposes
"""

grid = [
    [0, 0, 0, 2, 0, 7, 0, 0, 4],
    [9, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 2, 6, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 1, 0],
    [0, 3, 6, 8, 0, 0, 2, 0, 0],
    [0, 0, 5, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 3, 0, 0],
    [1, 0, 0, 9, 0, 0, 0, 0, 0],
    [0, 9, 3, 0, 0, 6, 0, 7, 0]
]


def valid_sudoku(puzzle: list[list[str]]) -> bool:
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            value = puzzle[i][j]

            if value != ".":
                for row in range(len(puzzle)):
                    if puzzle[row][j] == value and row != i:
                        return False

                for column in range(len(puzzle[0])):
                    if puzzle[i][column] == value and column != j:
                        return False

                row = (i // 3) * 3
                column = (j // 3) * 3
                for temp1 in range(row, row + 3):
                    for temp2 in range(column, column + 3):
                        if puzzle[temp1][temp2] == value and temp1 != i and temp2 != j:
                            return False

    return True


def valid_position(puzzle: list[list[int]], row: int, column: int, value: int) -> bool:
    for i in range(9):
        if (puzzle[row][i] == value and i != column) or (puzzle[i][column] == value and i != row):
            return False

    x = row // 3 * 3
    y = column // 3 * 3
    for i in range(x, x + 3):
        for j in range(y, y + 3):
            if puzzle[i][j] == value:
                return False

    return True


def valid_grid(puzzle: list[list[int]]) -> bool:
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            value = puzzle[i][j]

            if value != 0:
                for row in range(len(puzzle)):
                    if puzzle[row][j] == value and row != i:
                        return False

                for column in range(len(puzzle[0])):
                    if puzzle[i][column] == value and column != j:
                        return False

                row = (i // 3) * 3
                column = (j // 3) * 3
                for temp1 in range(row, row + 3):
                    for temp2 in range(column, column + 3):
                        if puzzle[temp1][temp2] == value and temp1 != i and temp2 != j:
                            return False

        return True


def automate(puzzle: list[list[int]]) -> None:
    duration = 0.05
    keyboard = Controller()
    str_final = []
    for i in puzzle:
        str_final.extend([str(j) for j in i])

    count = 0

    for i in range(3):
        time.sleep(1)
        print(i)

    for num in str_final:
        keyboard.press(num)
        time.sleep(duration)
        keyboard.press(Key.right)
        time.sleep(duration)
        count += 1
        if count % 9 == 0:
            keyboard.press(Key.down)
            time.sleep(duration)
            for _ in range(8):
                keyboard.press(Key.left)
                time.sleep(duration)
            count = 0


def completed(puzzle: list[list[int]]):
    for i in range(len(puzzle)-1, -1, -1):
        for j in range(len(puzzle[i])-1, -1, -1):
            if puzzle[i][j] == 0:
                return False

    return True


def solve(puzzle: list[list[int]]) -> list[list[int]]:
    result = [[]]
    for x in range(9):
        for y in range(9):
            if puzzle[x][y] == 0:
                for k in range(1, 10):
                    if valid_position(puzzle, x, y, k):
                        puzzle[x][y] = k
                        temp = solve(puzzle)
                        if temp != [[]]:
                            result = [i[:] for i in temp]
                        puzzle[x][y] = 0
                if completed(result):
                    return result
                return [[]]

    return puzzle


if __name__ == "__main__":
    t1 = solve(grid)
    for rows in t1:
        print(rows)
    for second in range(3, -1, -1):
        print("Starting in " + str(second))
        time.sleep(1)
    automate(t1)
