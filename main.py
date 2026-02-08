MIN_N = 3
MAX_N = 8

from Node import Node, SearchTree

with open("p1_npuzzle5.txt", "r") as file:
    content = file.readlines()

n = len(content)

if n < MIN_N or n > MAX_N:
    raise ValueError("Wrong matrix size")

matrix = []

for line in content:
    values = list(map(int, line.split()))
    matrix.append(values)

goal_state = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9],
              [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24]]

root = Node(goal_state, 0)
t = SearchTree(goal_state, goal_state)
res = t.A_star()
print(res)

