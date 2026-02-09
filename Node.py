import heapq

class Node:

    _counter = 0

    def __init__(self, state, g,  parent = None, action = None, children = None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = children
        self.g = g
        self.id = Node._counter
        Node._counter += 1

    def __lt__(self, other):
        return self.id < other.id

    def expand(self):
        if not self.children:
            x, y = self.find_zero()
            children = []

            if x-1 >= 0: 
                temp = self.copy_state(self.state)
                self.swap(temp, x, y, x-1, y)
                children.append(Node(temp, self.g + 1, self))
            if x+1 < len(self.state):
                temp = self.copy_state(self.state)
                self.swap(temp, x, y, x+1, y)
                children.append(Node(temp, self.g + 1, self))
            if y-1 >= 0: 
                temp = self.copy_state(self.state)
                self.swap(temp, x, y, x, y-1)
                children.append(Node(temp, self.g + 1, self))
            if y+1 < len(self.state):
                temp = self.copy_state(self.state)
                self.swap(temp, x, y, x, y+1)
                children.append(Node(temp, self.g + 1, self))

            self.children = children

    
    def swap(self, state, x1, y1, x2, y2):
        temp = state[x1][y1]
        state[x1][y1] = state[x2][y2]
        state[x2][y2] = temp 

    def find_zero(self):
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if(self.state[i][j] == 0): return i, j

    def copy_state(self, state):
        temp = []
        for row in state:
            temp_row = []
            for element in row:
                temp_row.append(element)
            temp.append(temp_row)
        return temp
    

class SearchTree:

    def __init__(self, initial_state, goal_state):
        self.root = Node(initial_state, 0)
        self.goal_state = goal_state
        self.n = len(goal_state)
        self.goal_pos = {}
        for i in range(self.n):
            for j in range(self.n):
                tile = self.goal_state[i][j]
                if tile != 0:
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
        return self.manhattan_dist(state) + self.linear_conflict(state)
        # return self.manhattan_dist(state)

    @staticmethod
    def state_key(state):
        return tuple(tuple(row) for row in state)

    def A_star(self):
        if self.goal_test(self.root.state):
            return self.solution(self.root), self.root.g, True
        
        frontier = []
        best_g = {}

        root_key = self.state_key(self.root.state)
        best_g[root_key] = self.root.g
        heapq.heappush(frontier, (self.root.g + self.heuristic(self.root.state), self.root))

        while(True):
            if not frontier:
                return False
            
            _, node = heapq.heappop(frontier)
            key = self.state_key(node.state)

            if node.g > best_g.get(key, float("inf")):
                continue

            if self.goal_test(node.state):
                return self.solution(node), node.g, True
            
            node.expand()
            for i in node.children:
                child_key = self.state_key(i.state)
                child_g = i.g
                if child_g < best_g.get(child_key, float("inf")):
                    best_g[child_key] = child_g
                    cost = child_g + self.heuristic(i.state)
                    heapq.heappush(frontier, (cost, i))
                    

    @staticmethod     
    def solution(node):
        sol = []
        current = node

        while current is not None:
            sol.append(current.state)
            current = current.parent

        sol.reverse()
        return sol
