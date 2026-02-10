# N-Puzzle A* Solver

This project solves the N-puzzle using A* search.
The blank tile is `0`, and each move swaps `0` with one neighboring tile.

Project report: `ai_p1_report.pdf`

## Scope

- Puzzle size constraint: `3 <= n <= 5`
- Path cost per move: `1`
- Goal state used by the code: row-major order (`0, 1, 2, ...`)

## Files

- `main.py`: reads a matrix from `p1_npuzzle5.txt` and runs one test
- `run_test.py`: interactive runner (enter `n`, matrix rows, and heuristic)
- `Node.py`: node expansion, heuristics, and A* implementation
- `p1_npuzzle5.txt`: sample matrix input file
- `ai_p1_report.pdf`: report with problem setup and benchmark results

## Requirements

- Python 3
- File named `npuzzle.txt` in case of file input

## Run With Interactive Input (`run_test.py`)

Run:

```bash
python run_test.py
```

Then provide:

1. `n` (between `3` and `5`)
2. provide input method: `1` - console input; `2` - read from file (npuzzle.txt)
3. if console input is chosen provide `n` matrix rows (each row has `n` integers)
4. heuristic option:
   - `1` Manhattan + Linear Conflict
   - `2` Manhattan Distance
   - `3` Misplaced Tiles
   - `4` Gasching Distance

Examples:

```text
Enter n (3-5): 3
Row 1: 1 0 2
Row 2: 3 5 4
Row 3: 6 8 7
Select (1-4): 1
```
```text
Enter n (3-5): 5
Choose input method:
1. Console input
2. Read from file (npuzzle.txt)
Select (1-2): 2
```

Output includes solved status, move count, path length, processed nodes, and runtime.

## Heuristics

- Manhattan + Linear Conflict: Manhattan distance plus a penalty for reversed tile pairs in the same goal row/column.
- Manhattan Distance: sum of vertical and horizontal distances from each tile to its goal position.
- Misplaced Tiles: number of tiles that are not in their goal positions.
- Gasching Distance: relaxed estimate based on repeated blank-tile swaps toward the goal.

Heuristic keys used in `SearchTree`:

- `manhattan_linear_conflict`
- `manhattan`
- `misplaced_tiles`
- `gasching`

Example:

```python
SearchTree(initial_state, goal_state, "manhattan")
```

## Benchmark Snapshot (From Report)

Nodes / time (seconds):

| Test | Manhattan + Linear Conflict | Manhattan | Gasching | Misplaced |
|---|---:|---:|---:|---:|
| 3x3 | 501 / 0.004778 | 703 / 0.005620 | 2628 / 0.086516 | 1968 / 0.015341 |
| 4x4 | 35530 / 0.504591 | 100773 / 0.816537 | - | - |
| 5x5 | 404253 / 8.389636 | 1091149 / 15.692326 | - | - |

Report conclusion: Manhattan + Linear Conflict is the most effective among tested heuristics for these cases.
