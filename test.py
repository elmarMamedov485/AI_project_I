import unittest
from Node import SearchTree
from run_test import (
    generate_goal_state,
    is_solvable,
    count_relative_inversions
)


class TestNPuzzle(unittest.TestCase):

    def setUp(self):
        self.goal_3 = generate_goal_state(3)
        self.goal_4 = generate_goal_state(4)
        self.goal_5 = generate_goal_state(5)

        self.solved_3 = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]

    # ======================================================
    # HEURISTIC TESTS
    # ======================================================

    def test_manhattan_zero_for_goal(self):
        tree = SearchTree(self.solved_3, self.goal_3, "manhattan")
        self.assertEqual(tree.manhattan_dist(tree.root.state), 0)

    def test_misplaced_zero_for_goal(self):
        tree = SearchTree(self.solved_3, self.goal_3, "misplaced_tiles")
        self.assertEqual(tree.misplaced_tiles(tree.root.state), 0)

    def test_gasching_zero_for_goal(self):
        tree = SearchTree(self.solved_3, self.goal_3, "gasching")
        self.assertEqual(tree.Gashing_dist(tree.root.state), 0)

    def test_linear_conflict_zero_for_goal(self):
        tree = SearchTree(self.solved_3, self.goal_3)
        self.assertEqual(tree.linear_conflict(tree.root.state), 0)

    def test_manhattan_simple_case(self):
        state = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]
        ]
        tree = SearchTree(state, self.goal_3, "manhattan")
        self.assertEqual(tree.manhattan_dist(tree.root.state), 1)

    def test_misplaced_simple_case(self):
        state = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]
        ]
        tree = SearchTree(state, self.goal_3, "misplaced_tiles")
        self.assertEqual(tree.misplaced_tiles(tree.root.state), 1)

    def test_gasching_simple_case(self):
        state = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]
        ]
        tree = SearchTree(state, self.goal_3, "gasching")
        self.assertEqual(tree.Gashing_dist(tree.root.state), 1)

    def test_linear_conflict_dominates_manhattan(self):
        state = [
            [2, 1, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        tree = SearchTree(state, self.goal_3)

        manhattan = tree.manhattan_dist(tree.root.state)
        combined = tree.heuristic(tree.root.state)

        self.assertGreaterEqual(combined, manhattan)

    # ======================================================
    # SOLVABILITY TESTS
    # ======================================================

    def test_solvable_3x3(self):
        initial = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]
        ]
        self.assertTrue(is_solvable(initial, self.goal_3))

    def test_unsolvable_3x3(self):
        unsolvable = [
            [1, 2, 3],
            [4, 5, 6],
            [8, 7, 0]
        ]
        self.assertFalse(is_solvable(unsolvable, self.goal_3))

    def test_solvable_4x4(self):
        solvable = [
            [1,  2,  3,  4],
            [5,  6,  7,  8],
            [9, 10, 11, 12],
            [13, 14,  0, 15]
        ]
        self.assertTrue(is_solvable(solvable, self.goal_4))

    def test_unsolvable_4x4(self):
        unsolvable = [
            [1,  2,  3,  4],
            [5,  6,  7,  8],
            [9, 10, 11, 12],
            [13, 15, 14,  0]
        ]
        self.assertFalse(is_solvable(unsolvable, self.goal_4))

    # ======================================================
    # A* SEARCH TESTS
    # ======================================================

    def test_astar_trivial(self):
        tree = SearchTree(self.solved_3, self.goal_3, "manhattan")
        path, cost, processed_nodes, solved = tree.A_star()

        self.assertTrue(solved)
        self.assertEqual(cost, 0)

    def test_astar_one_move(self):
        state = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]
        ]
        tree = SearchTree(state, self.goal_3)
        path, cost, processed_nodes, solved = tree.A_star()

        self.assertTrue(solved)
        self.assertEqual(cost, 1)

    def test_astar_two_moves(self):
        state = [
            [1, 2, 3],
            [4, 5, 6],
            [0, 7, 8]
        ]
        tree = SearchTree(state, self.goal_3)
        path, cost, processed_nodes, solved = tree.A_star()

        self.assertTrue(solved)
        self.assertEqual(cost, 2)

    def test_astar_time_limit(self):
        state = [
            [8, 6, 7],
            [2, 5, 4],
            [3, 0, 1]
        ]
        tree = SearchTree(state, self.goal_3)

        result = tree.A_star(time_limit=0.0001)

        self.assertFalse(result)

    # ======================================================
    # 5x5 INTEGRATION TEST
    # ======================================================

    def test_astar_5x5(self):
        state = [
            [11, 1, 2, 3, 14],
            [12, 7, 9, 10, 13],
            [6, 8, 18, 5, 4],
            [21, 16, 17, 19, 15],
            [22, 23, 0, 24, 20],
        ]

        tree = SearchTree(state, self.goal_5)
        path, cost, processed_nodes, solved = tree.A_star()

        self.assertTrue(solved)
        self.assertEqual(cost, 38)

    # ======================================================
    # INVERSION TESTS
    # ======================================================

    def test_inversion_zero(self):
        inversions = count_relative_inversions(self.solved_3, self.goal_3)
        self.assertEqual(inversions, 0)

    def test_inversion_one(self):
        state = [
            [1, 2, 3],
            [4, 5, 6],
            [8, 7, 0]
        ]
        inversions = count_relative_inversions(state, self.goal_3)
        self.assertEqual(inversions, 1)


if __name__ == "__main__":
    unittest.main()
