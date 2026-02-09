MIN_N = 3
MAX_N = 8

from time import time
from Node import SearchTree


with open("p1_npuzzle5.txt", "r") as file:
    content = file.readlines()

n = len(content)

if n < MIN_N or n > MAX_N:
    raise ValueError("Wrong matrix size")

matrix = []
for line in content:
    values = list(map(int, line.split()))
    matrix.append(values)


def run_test(name, initial_state, goal_state):
    start_time = time()
    result = SearchTree(initial_state, goal_state).A_star()
    elapsed = time() - start_time

    if not result:
        print(f"{name}: no solution found")
        print(f"Time taken: {elapsed:.6f} seconds")
        print("-" * 60)
        return

    path, cost, solved = result
    print(f"{name}: solved={solved}, moves={cost}, path_len={len(path)}")
    print(f"Time taken: {elapsed:.6f} seconds")
    print("-" * 60)


goal_state = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9],
              [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24]]
init_state = [[0, 1, 2, 3, 4], [5, 6, 16, 8, 9],
              [10, 11, 12, 13, 14], [15, 7, 17, 18, 19], [20, 21, 22, 23, 24]]

goal_state_2 = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
init_state_2 = [[1, 0, 2], [3, 4, 5], [6, 7, 8]]

goal_state_3 = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
init_state_3 = [[5, 1, 15, 7], [8, 4, 2, 11], [0, 3, 6, 14], [12, 9, 10, 13]]


tests = [
    # ("test_1_hard_5x5", init_state, goal_state),
    ("test_2_medium_3x3", init_state_2, goal_state_2),
    ("test_3_medium_4x4", init_state_3, goal_state_3)
]

for test_name, init_state, goal_state in tests:
    run_test(test_name, init_state, goal_state)
