import heapq
import time

class Node:

    _counter = 0  # unique id for tie-breaking in heap

    def __init__(self, state, g, parent=None, action=None):
        
        # Convert list state to tuple for hashing (dictionary keys)
        if isinstance(state, list):
            state = tuple(tuple(row) for row in state)
        
        self.state = state          # board configuration
        self.parent = parent        # parent node in search tree
        self.action = action        # move taken to reach this node
        self.g = g                  # path cost
        self.id = Node._counter     # tie-breaker id
        Node._counter += 1

    # Tie-breaking when f-costs are equal
    def __lt__(self, other):
        return self.id < other.id

    # Generate all valid neighboring states
    def expand(self):
        x, y = Node.find_zero(self.state)
        children = []

        moves = [("Up", x-1, y), ("Down", x+1, y),
                 ("Left", x, y-1), ("Right", x, y+1)]

        for name, nx, ny in moves:
            if 0 <= nx < len(self.state) and 0 <= ny < len(self.state):
                new_state = Node.copy_state(self.state)
                # Swap zero with target tile
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                children.append(Node(new_state, self.g + 1, self, (name, (nx, ny))))

        return children

    # Locate zero tile position
    @staticmethod
    def find_zero(state):
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] == 0:
                    return i, j

    # Deep copy state (as list for modification)
    @staticmethod
    def copy_state(state):
        return [list(row) for row in state]


class SearchTree:

    def __init__(self, initial_state, goal_state, heuristic_name="manhattan_linear_conflict"):

        # Convert goal to tuple if needed
        if isinstance(goal_state, list):
            goal_state = tuple(tuple(row) for row in goal_state)
        
        self.goal_state = goal_state
        self.root = Node(initial_state, 0)
        self.n = len(goal_state)
        self.heuristic_name = heuristic_name

        # Precompute goal positions for fast lookup
        self.goal_pos = {}
        for i in range(self.n):
            for j in range(self.n):
                tile = self.goal_state[i][j]
                self.goal_pos[tile] = (i, j)

    # Check if state equals goal
    def goal_test(self, state):
        return state == self.goal_state

    # Manhattan distance heuristic
    def manhattan_dist(self, state):
        res = 0
        for i in range(self.n):
            for j in range(self.n):
                tile = state[i][j]
                if tile != 0:
                    gx, gy = self.goal_pos[tile]
                    res += abs(i - gx) + abs(j - gy)
        return res
    
    # Count misplaced tiles
    def misplaced_tiles(self, state):
        res = 0
        for i in range(self.n):
            for j in range(self.n):
                tile = state[i][j]
                if tile != 0:
                    gx, gy = self.goal_pos[tile]
                    if (i, j) != (gx, gy):
                        res += 1
        return res
    
    # Gaschnig's heuristic
    def Gashing_dist(self, state):
        temp = Node.copy_state(state)
        res = 0

        while self.misplaced_tiles(temp) > 0:
            zero_x, zero_y = Node.find_zero(temp)
            
            # If zero not in goal position, swap with correct tile
            if (zero_x, zero_y) != self.goal_pos[0]:
                tile = self.goal_state[zero_x][zero_y]
                for i in range(self.n):
                    for j in range(self.n):
                        if temp[i][j] == tile:
                            gx, gy = i, j
                temp[gx][gy], temp[zero_x][zero_y] = temp[zero_x][zero_y], temp[gx][gy]
            else:
                # Otherwise swap any misplaced tile
                for i in range(self.n):
                    for j in range(self.n):
                        if temp[i][j] != 0:
                            gx, gy = self.goal_pos[temp[i][j]]
                            if (i, j) != (gx, gy):
                                temp[gx][gy], temp[i][j] = temp[i][j], temp[gx][gy]
                                break
                else:
                    continue
            res += 1
        return res

    # Count inversions (used for linear conflict)
    @staticmethod
    def _count_inversions(values):
        inversions = 0
        for i in range(len(values)):
            for j in range(i + 1, len(values)):
                if values[i] > values[j]:
                    inversions += 1
        return inversions

    # Linear conflict heuristic component
    def linear_conflict(self, state):
        conflicts = 0

        # Row conflicts
        for row in range(self.n):
            goal_cols = []
            for col in range(self.n):
                tile = state[row][col]
                if tile == 0:
                    continue
                goal_row, goal_col = self.goal_pos[tile]
                if goal_row == row:
                    goal_cols.append(goal_col)
            conflicts += self._count_inversions(goal_cols)

        # Column conflicts
        for col in range(self.n):
            goal_rows = []
            for row in range(self.n):
                tile = state[row][col]
                if tile == 0:
                    continue
                goal_row, goal_col = self.goal_pos[tile]
                if goal_col == col:
                    goal_rows.append(goal_row)
            conflicts += self._count_inversions(goal_rows)

        return 2 * conflicts  # each conflict adds 2 moves

    # Select heuristic function
    def heuristic(self, state):
        if self.heuristic_name == "manhattan_linear_conflict":
            return self.manhattan_dist(state) + self.linear_conflict(state)
        if self.heuristic_name == "manhattan":
            return self.manhattan_dist(state)
        if self.heuristic_name == "misplaced_tiles":
            return self.misplaced_tiles(state)
        if self.heuristic_name == "gasching":
            return self.Gashing_dist(state)
        raise ValueError(f"Unknown heuristic: {self.heuristic_name}")    

    # A* search algorithm
    def A_star(self, time_limit=None):
        start_time = time.time()
        processed_nodes = 1

        if self.goal_test(self.root.state):
            return self.solution(self.root), self.root.g, processed_nodes, True
        
        frontier = []          # priority queue
        best_g = {}            # best cost to each state

        best_g[self.root.state] = self.root.g
        heapq.heappush(frontier, (self.root.g + self.heuristic(self.root.state), self.root))

        while frontier:

            # Stop if time limit exceeded
            if time_limit is not None and (time.time() - start_time) >= time_limit:
                print("\nTime limit exceeded")
                return False

            _, node = heapq.heappop(frontier)

            # Skip outdated entries
            if node.g > best_g.get(node.state, float("inf")):
                continue

            if self.goal_test(node.state):
                return self.solution(node), node.g, processed_nodes, True
            
            # Expand node
            for child in node.expand():
                child_g = child.g
                if child_g < best_g.get(child.state, float("inf")):
                    best_g[child.state] = child_g
                    cost = child_g + self.heuristic(child.state)
                    processed_nodes += 1
                    heapq.heappush(frontier, (cost, child))

    # Reconstruct solution path
    @staticmethod     
    def solution(node):
        sol = []
        current = node

        while current is not None:
            sol.append((current.state, current.action))
            current = current.parent

        sol.reverse()
        return sol
