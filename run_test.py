from time import time

from Node import SearchTree

MIN_N = 3
MAX_N = 5


def generate_goal_state(n):
    tiles = list(range(n * n))
    return [tiles[i * n:(i + 1) * n] for i in range(n)]


def read_matrix(n):
    matrix = []
    print(f"Enter the matrix row by row ({n} numbers per row):")
    for i in range(n):
        row = list(map(int, input(f"Row {i + 1}: ").split()))
        if len(row) != n:
            raise ValueError(f"Row {i + 1} must contain exactly {n} numbers")
        matrix.append(row)
    return matrix


def validate_matrix(matrix, n):
    values = [tile for row in matrix for tile in row]
    if len(values) != n * n:
        raise ValueError("Invalid number of elements in matrix")

    expected = set(range(n * n))
    actual = set(values)
    if actual != expected:
        raise ValueError(f"Matrix must contain all numbers from 0 to {n * n - 1} exactly once")


def find_zero(state):
    for i, row in enumerate(state):
        for j, tile in enumerate(row):
            if tile == 0:
                return i, j
    raise ValueError("Matrix must contain 0")


def count_relative_inversions(initial_state, goal_state):
    goal_rank = {}
    rank = 0

    for tile in [x for row in goal_state for x in row]:
        if tile != 0:
            goal_rank[tile] = rank
            rank += 1

    mapped = [goal_rank[tile] for row in initial_state for tile in row if tile != 0]
    return SearchTree._count_inversions(mapped)


def is_solvable(initial_state, goal_state):
    n = len(initial_state)
    inversions = count_relative_inversions(initial_state, goal_state)

    if n % 2 == 1:
        return inversions % 2 == 0

    start_blank_row_from_bottom = n - find_zero(initial_state)[0]
    goal_blank_row_from_bottom = n - find_zero(goal_state)[0]
    return (inversions + start_blank_row_from_bottom) % 2 == goal_blank_row_from_bottom % 2


def choose_algorithm():
    print("Choose algorithm:")
    print("1. Manhattan + Linear Conflict")
    print("2. Manhattan Distance")
    print("3. Misplaced Tiles")
    print("4. Gasching Distance")

    choice = int(input("Select (1-4): "))
    options = {
        1: ("manhattan_linear_conflict", "Manhattan + Linear Conflict"),
        2: ("manhattan", "Manhattan Distance"),
        3: ("misplaced_tiles", "Misplaced Tiles"),
        4: ("gasching", "Gasching Distance"),
    }

    if choice not in options:
        raise ValueError("Algorithm must be between 1 and 4")

    return options[choice]


def run_test(initial_state, goal_state, heuristic_key, heuristic_label):
    if not is_solvable(initial_state, goal_state):
        print("Result: puzzle is not solvable for the selected goal state.")
        return

    start_time = time()
    result = SearchTree(initial_state, goal_state, heuristic_key).A_star()
    elapsed = time() - start_time

    print(f"\nHeuristic: {heuristic_label}")
    if not result:
        print("Result: no solution found")
        print(f"Time taken: {elapsed:.6f} seconds")
        return

    path, cost, processed_nodes, solved = result
    print(f"Result: solved={solved}, moves={cost}, path_len={len(path)}, processed_nodes={processed_nodes}")
    print(f"Time taken: {elapsed:.6f} seconds")


def main():
    n = int(input(f"Enter n ({MIN_N}-{MAX_N}): "))
    if n < MIN_N or n > MAX_N:
        raise ValueError(f"n must be between {MIN_N} and {MAX_N}")

    initial_state = read_matrix(n)
    validate_matrix(initial_state, n)
    goal_state = generate_goal_state(n)

    print("\nInitial state:")
    for row in initial_state:
        print(row)

    print("\nGoal state:")
    for row in goal_state:
        print(row)

    heuristic_key, heuristic_label = choose_algorithm()
    run_test(initial_state, goal_state, heuristic_key, heuristic_label)


if __name__ == "__main__":
    main()
