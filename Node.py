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

    def goal_test(self, state):
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] != self.goal_state[i][j]:
                    return False
        return True

    def manhattan_dist(self, state):
        res = 0
        expected = {}

        for i in range(len(self.goal_state)):
            for j in range(len(self.goal_state)):
                if self.goal_state[i][j] != 0:
                    expected[self.goal_state[i][j]] = (i, j)

        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] != 0:
                    expected_x, expected_y = expected[state[i][j]][0], expected[state[i][j]][1] 
                    res += abs(i - expected_x) + abs(j - expected_y)

        return res

    def A_star(self):
        if self.goal_test(self.root.state):
            return self.solution(self.root), self.root.g, True
        
        frontier = []
        optimal_cost = {}

        heapq.heappush(frontier, (self.root.g + self.manhattan_dist(self.root.state), self.root))
        root_key = tuple(tuple(row) for row in self.root.state)
        optimal_cost[root_key] = self.manhattan_dist(self.root.state)

        while(True):
            if not frontier:
                return False
            
            current_cost, node = heapq.heappop(frontier)

            if self.goal_test(node.state):
                return self.solution(node), node.g, True
            
            node.expand()
            for i in node.children:
                cost = i.g + self.manhattan_dist(i.state)
                key = tuple(tuple(row) for row in i.state)
                if key not in optimal_cost:
                    heapq.heappush(frontier, (cost, i))
                    print(i.state, cost)
                elif key in optimal_cost and cost < optimal_cost[key]:
                    optimal_cost[key] = cost
                    

    @staticmethod     
    def solution(node):
        sol = []
        current = node

        while current.parent is not None:
            sol.append(current.state)
            current = current.parent

        sol.reverse()
        return sol
