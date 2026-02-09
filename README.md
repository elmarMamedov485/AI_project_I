# N-Puzzle A* Solver

This project solves the N-puzzle with A* search.
The blank tile is `0`.
Each move swaps `0` with one neighbor tile.

## Files

- `main.py`: runs test cases and prints solve time
- `Node.py`: puzzle node logic, A* search, and heuristics
- `p1_npuzzle5.txt`: sample 5x5 board input

## How To Run

```bash
python main.py
```

## Heuristics

`Node.py` uses:

- Manhattan distance
- Linear conflict

Linear conflict means two tiles are in the same goal row or column but in reversed order, so they block each other and need extra moves.

Current heuristic:

```python
return self.manhattan_dist(state) + self.linear_conflict(state)
```

To test Manhattan only, use:

```python
return self.manhattan_dist(state)
```

## Quick Timing Note

On `test_3_medium_4x4` case:

- Manhattan: `2.156919` seconds
- Manhattan + linear conflict: `1.053466` seconds

So linear conflict cuts search time for this case.
