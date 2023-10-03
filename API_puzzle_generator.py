import time
import requests


url = "https://sudoku-api.vercel.app/api/dosuku"


"""
Plan: 
First, generate a single easy puzzle to set to default, putting it within a first_puz function
Then, if user changes mode, don't generate new puzzle unless its clicked just once
If clicked once, check to make sure user doesn't spam click generate within 10s

My current plan is the following. 
First, when my program first runs, I would immediately generate an easy puzzle for the user

While the user is solving the puzzle, I would create three different lists, each holding differing difficulties of easy, medium, and hard. 

While user is still solving, I  would create a function that runs on the background that calls the API to generate puzzles, until each list reaches a specified limit, for example, 10. 

So if Easy, Medium, and Hard lists all have 10 different puzzles, I would deem it sufficient and stop the API calling, thus eliminating unnecessary calls. 

Each time the user generates a puzzle, I would take that from the corresponding list and call the API to generate another puzzle to fill in for the one that was removed for the user. 

Finish backup sudoku generator! 
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

print("\n\n\n\n\n")
for i in range(10):
    print(easy_grid[i])
    print(medium_grid[i])
    print(hard_grid[i])