import heapq

class Node:

    _counter = 0

    def __init__(self, state, g,  parent = None, action = None):
        
        if isinstance(state, list):
            state = tuple(tuple(row) for row in state)
        
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.id = Node._counter
        Node._counter += 1

    def __lt__(self, other):
        return self.id < other.id

    def expand(self):
        x, y = Node.find_zero(self.state)
        children = []

        moves = [("Up", x-1, y),("Down", x+1, y), ("Left", x, y-1),("Right", x, y+1)]

        for name, nx, ny in moves:
            if 0 <= nx < len(self.state) and 0 <= ny < len(self.state):
                new_state = Node.swap(self.state, x, y, nx, ny)
                children.append(Node(new_state, self.g + 1, self, (name, (nx, ny))))

        return children

    @staticmethod
    def swap(state, x1, y1, x2, y2):
        temp_state = list(list(row) for row in state)
        temp = temp_state[x1][y1]
        temp_state[x1][y1] = temp_state[x2][y2]
        temp_state[x2][y2] = temp 
        return tuple(tuple(row) for row in temp_state)

    @staticmethod
    def find_zero(state):
        for i in range(len(state)):
            for j in range(len(state)):
                if(state[i][j] == 0): return i, j

    @staticmethod
    def copy_state( state):
        temp = []
        for row in state:
            temp_row = []
            for element in row:
                temp_row.append(element)
            temp.append(temp_row)
        return temp

class SearchTree:

    def __init__(self, initial_state, goal_state, heuristic_name="manhattan_linear_conflict"):
        if isinstance(goal_state, list):
            goal_state = tuple(tuple(row) for row in goal_state)
        
        self.goal_state = goal_state
        self.root = Node(initial_state, 0)
        self.n = len(goal_state)
        self.heuristic_name = heuristic_name
        self.goal_pos = {}
        for i in range(self.n):
            for j in range(self.n):
                tile = self.goal_state[i][j]
                self.goal_pos[tile] = (i, j)

    def goal_test(self, state):
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] != self.goal_state[i][j]:
                    return False
        return True

    def manhattan_dist(self, state):
        res = 0
        for i in range(self.n):
            for j in range(self.n):
                tile = state[i][j]
                if tile != 0:
                    expected_x, expected_y = self.goal_pos[tile]
                    res += abs(i - expected_x) + abs(j - expected_y)

        return res
    
    def misplaced_tiles(self, state):
        res = 0

        for i in range(self.n):
            for j in range(self.n):
                tile = state[i][j]

                if tile != 0:
                    goal_pos_x, goal_pos_y = self.goal_pos[state[i][j]]
                    if i != goal_pos_x or j != goal_pos_y: 
                        res += 1
        
        return res
    
    def Gashing_dist(self, state):
        temp = Node.copy_state(state)
        res = 0

        while (self.misplaced_tiles(temp) > 0):
            zero_x, zero_y = Node.find_zero(temp)
            
            if (zero_x, zero_y) != self.goal_pos[0]:
                tile = self.goal_state[zero_x][zero_y]
                for i in range(self.n):
                    for j in range(self.n):
                        if temp[i][j] == tile: gx, gy = i, j
                Node.swap(temp, gx, gy, zero_x, zero_y)

            else:
                for i in range(self.n):
                    for j in range(self.n):
                        if temp[i][j] != 0:
                            gx, gy = self.goal_pos[temp[i][j]]
                            if (i, j) != (gx, gy):
                                Node.swap(temp, zero_x, zero_y, i, j)
                                break
                else:
                    continue
                break

            res += 1
        return res


    @staticmethod
    def _count_inversions(values):
        inversions = 0
        for i in range(len(values)):
            for j in range(i + 1, len(values)):
                if values[i] > values[j]:
                    inversions += 1
        return inversions

    def linear_conflict(self, state):
        conflicts = 0

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

        return 2 * conflicts

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

    def A_star(self):
        processed_nodes = 1

        if self.goal_test(self.root.state):
            return self.solution(self.root), self.root.g, processed_nodes, True
        
        frontier = []
        best_g = {}

        best_g[self.root.state] = self.root.g
        heapq.heappush(frontier, (self.root.g + self.heuristic(self.root.state), self.root))

        while frontier:
            _, node = heapq.heappop(frontier)

            if node.g > best_g.get(node.state, float("inf")):
                continue

            if self.goal_test(node.state):
                return self.solution(node), node.g, processed_nodes, True
            
            
            for child in node.expand():
                child_g = child.g
                if child_g < best_g.get(child.state, float("inf")):
                    best_g[child.state] = child_g
                    cost = child_g + self.heuristic(child.state)
                    processed_nodes += 1
                    heapq.heappush(frontier, (cost, child))
                    

    @staticmethod     
    def solution(node):
        sol = []
        current = node

        while current is not None:
            sol.append((current.state, current.action))
            current = current.parent

        sol.reverse()
        return sol