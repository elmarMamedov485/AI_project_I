from time import time
from Node import SearchTree

MIN_N = 3   # minimum puzzle size
MAX_N = 5   # maximum puzzle size


# Generate goal state (1..n²-1, 0 at the end)
def generate_goal_state(n):
    tiles = list(i + 1 for i in range(n * n))
    tiles[-1] = 0
    return [tiles[i * n:(i + 1) * n] for i in range(n)]


# Read puzzle from console
def read_matrix(n):
    matrix = []
    print(f"Enter the matrix row by row ({n} numbers per row):")
    for i in range(n):
        row = list(map(int, input(f"Row {i + 1}: ").split()))
        if len(row) != n:
            raise ValueError(f"Row {i + 1} must contain exactly {n} numbers")
        matrix.append(row)
    return matrix


# Validate puzzle contains all numbers 0..n²-1 exactly once
def validate_matrix(matrix, n):
    values = [tile for row in matrix for tile in row]

    if len(values) != n * n:
        raise ValueError("Invalid number of elements in matrix")

    expected = set(range(n * n))
    actual = set(values)

    if actual != expected:
        raise ValueError(f"Matrix must contain all numbers from 0 to {n * n - 1} exactly once")


# Find position of blank tile (0)
def find_zero(state):
    for i, row in enumerate(state):
        for j, tile in enumerate(row):
            if tile == 0:
                return i, j
    raise ValueError("Matrix must contain 0")


# Count inversions relative to goal ordering
def count_relative_inversions(initial_state, goal_state):
    goal_rank = {}
    rank = 0

    # Assign rank to each tile in goal (excluding 0)
    for tile in [x for row in goal_state for x in row]:
        if tile != 0:
            goal_rank[tile] = rank
            rank += 1

    # Map initial state to goal ranks
    mapped = [goal_rank[tile] for row in initial_state for tile in row if tile != 0]

    return SearchTree._count_inversions(mapped)


# Check puzzle solvability
def is_solvable(initial_state, goal_state):
    n = len(initial_state)
    inversions = count_relative_inversions(initial_state, goal_state)

    # Odd grid: inversions must be even
    if n % 2 == 1:
        return inversions % 2 == 0

    # Even grid: consider blank row from bottom
    start_blank_row_from_bottom = n - find_zero(initial_state)[0]
    goal_blank_row_from_bottom = n - find_zero(goal_state)[0]

    return (inversions + start_blank_row_from_bottom) % 2 == goal_blank_row_from_bottom % 2


# Let user choose heuristic
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


# Run A* and print results
def run_test(initial_state, goal_state, heuristic_key, heuristic_label, time_limit=None):

    # Check solvability before running search
    if not is_solvable(initial_state, goal_state):
        print("Result: puzzle is not solvable for the selected goal state.")
        return

    start_time = time()
    result = SearchTree(initial_state, goal_state, heuristic_key).A_star(time_limit)
    elapsed = time() - start_time

    print(f"\nHeuristic: {heuristic_label}")

    if not result:
        print("Result: no solution found")
        print(f"Time taken: {elapsed:.6f} seconds")
        return

    path, cost, processed_nodes, solved = result

    print(f"Result: solved={solved}, moves={cost}, processed_nodes={processed_nodes}")
    print(f"Time taken: {elapsed:.6f} seconds")

    # Optionally display full solution path
    view_path = input("View path (y, n):")

    if view_path == 'y':
        count = 1
        for state, action in path:
            print(f"\nMovement №: {count}\n Action: {action}\n")
            for row in state:
                print(row)
            count += 1
    elif view_path == 'n':
        pass
    else:
        raise ValueError("Incorrect input")


def main():
    # Read puzzle size
    n = int(input(f"Enter n ({MIN_N}-{MAX_N}): "))
    if n < MIN_N or n > MAX_N:
        raise ValueError(f"n must be between {MIN_N} and {MAX_N}")

    print("Choose input method:")
    print("1. Console input")
    print("2. Read from file (npuzzle.txt)")
    input_choice = int(input("Select (1-2): "))

    # Load initial state
    if input_choice == 1:
        initial_state = read_matrix(n)

    elif input_choice == 2:
        with open("npuzzle.txt", "r") as file:
            content = file.readlines()

        if len(content) != n:
            raise ValueError(f"File does not contain {n} rows")

        initial_state = []
        for line in content:
            row = list(map(int, line.split()))
            if len(row) != n:
                raise ValueError(f"File row does not contain {n} numbers")
            initial_state.append(row)

    else:
        raise ValueError("Input method must be 1 or 2")

    validate_matrix(initial_state, n)

    goal_state = generate_goal_state(n)

    # Print initial and goal states
    print("\nInitial state:")
    for row in initial_state:
        print(row)

    print("\nGoal state:")
    for row in goal_state:
        print(row)

    heuristic_key, heuristic_label = choose_algorithm()

    # Optional time limit
    time_limit = input("(Optional) Provide time limit in seconds:")

    if time_limit.strip() == "":
        time_limit = None
    else:
        try:
            time_limit = int(time_limit)
            if time_limit == 0:
                time_limit = None
        except ValueError:
            print("Invalid type. Time limit ignored")
            time_limit = None

    run_test(initial_state, goal_state, heuristic_key, heuristic_label, time_limit)

if __name__ == "__main__":
    main()
