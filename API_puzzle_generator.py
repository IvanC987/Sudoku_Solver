import time
import requests


url = "https://sudoku-api.vercel.app/api/dosuku"


"""
This is puzzle generator that uses the dosuku API, however it does have some limitations, which caused
me to not use this. 
The main problem is that the data retrieve is incorrect/has missing data, which caused the program to
freeze for several seconds. So I switched to another method, which can be seen within puzzle_generator.py file
"""


def create_puzzle() -> list:
    time.sleep(2)
    start = time.time()
    result = requests.get(url).json()
    puzzle = result["newboard"]["grids"][0]["value"]
    difficulty = result["newboard"]["grids"][0]["difficulty"]
    print(difficulty)
    print(start - time.time())
    return [puzzle, difficulty]


easy_grid = []
medium_grid = []
hard_grid = []

while len(easy_grid) < 3 or len(medium_grid) < 10 or len(hard_grid) < 10:
    result = create_puzzle()
    if result[1] == easy_grid:
        easy_grid.append(result[0])
    elif result[1] == medium_grid:
        medium_grid.append(result[0])
    elif result[1] == hard_grid:
        hard_grid.append(result[0])

print("\n\n\n")

for i in range(10):
    print(easy_grid[i])
    print(medium_grid[i])
    print(hard_grid[i])
