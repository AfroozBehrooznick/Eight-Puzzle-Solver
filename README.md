🧩8-Puzzle Solver (A*, IDA*, RBFS)

A fully interactive command-line 8-puzzle solver written in Python.
This program allows you to solve the classic 8-puzzle problem using three advanced search algorithms,
with clear step-by-step output and performance measurement.

It is designed to be simple, user-friendly, and fully compatible with Windows CMD.

❓But what Is the 8-Puzzle?
The 8-puzzle is a sliding puzzle played on a 3×3 grid.
It contains numbers from 1 to 8 and one empty space (represented as "0" or "\_").
The goal is to move the tiles until the puzzle reaches this state:

1 2 3
4 5 6
7 8 0

🌐Web Version Available

An interactive browser-based version of this project is also available.
The web application implements the same search algorithms (A*, IDA*, RBFS) entirely in JavaScript and provides:

- Visual puzzle board
- Step-by-step animation
- Playback controls
- Modern responsive UI
- Real-time statistics display

You can access the web version here:
👉 [https://github.com/AfroozBehrooznick/eight-puzzle-solver-web]

The CLI version (this repository) is focused on algorithm design, performance measurement, and system-level resource analysis.

📝Features

- Three puzzle input methods
- Three informed search algorithms
- Two heuristic functions
- Step-by-step solution printing
- Time and memory usage measurement
- Input validation with automatic re-prompt
- Exit available at almost every prompt
- Clean and readable terminal output

💻Input Methods
You can choose how to create the puzzle:

1. Predefined Puzzles

Ready-made puzzles with different difficulty levels:
Solved - Easy - Medium - Hard - Very Hard

2. Manual Entry

Enter your own puzzle using 9 unique numbers from 0 to 8.
Example: 1,2,3,4,5,6,7,8,0

The program checks:

- Exactly 9 numbers
- Numbers between 0 and 8
- No duplicates

3. Shuffle from Goal

The program starts from the solved puzzle and performs random valid moves.
This guarantees that the puzzle is solvable.

🎯Search Algorithms

The solver supports three informed search algorithms:

1. A\* Search
   A best-first search algorithm that uses:

- g(n): cost from start
- h(n): heuristic estimate to goal
- f(n) = g(n) + h(n)

Advantages:

- Optimal solution (if heuristic is admissible)
- Usually fast
- Uses more memory

2. IDA* (Iterative Deepening A*)
   A memory-efficient version of A\*.

How it works:

- Uses f-cost as a depth limit
- Repeats search with increasing bound

Advantages:

- Much lower memory usage
- Still optimal with admissible heuristic

3. RBFS (Recursive Best-First Search)
   A recursive best-first search algorithm.

How it works:

- Explores best node first
- Uses f-limit to control recursion
- Backtracks when necessary

Advantages:

- Memory efficient
- Good alternative to A\*

🖋️Heuristic Functions
You can choose between two heuristics:

1. Manhattan Distance
   Sum of vertical and horizontal distances of each tile from its goal position.

This heuristic is:
Admissible & Consistent & Recommended

2. Euclidean Distance
   Straight-line distance between current and goal positions.

This heuristic:
Is admissible & Usually slightly less accurate than Manhattan for 8-puzzle

🔎Solvability Check

Before solving, the program checks whether the puzzle is solvable.
Rule for 8-puzzle:
The number of inversions must be even.
If not solvable, the program asks you to choose another puzzle.

📜Output Information

After solving, the program prints:

- Algorithm used
- Heuristic used
- Path to goal (list of moves)
- Total number of moves
- Nodes expanded
- Search depth
- Maximum search depth
- Running time (seconds)
- Memory usage (MB)

Then it prints the solution step-by-step in a clear grid format.

⏱️Performance Measurement

The program measures:

- Running time using Python time module
- Memory usage using:
  - resource (Unix systems)
  - psutil (if available)

If memory measurement is not supported on your platform, it shows a message.

🔗User Experience

- At almost every prompt, you can type:
  - exit
  - quit
  - q
  - x

- Invalid input automatically triggers an error message and re-prompt.
- Clear separators and formatted output make it easy to read in CMD.

💻Technical Details

State representation:

- Each puzzle state is stored as a tuple of 9 integers.
- Example: "(1, 2, 3, 4, 5, 6, 7, 8, 0)"

Neighbor generation:

- Moves: Up, Down, Left, Right
- Only valid moves are generated.

Path reconstruction:

- Uses parent mapping
- Rebuilds solution from goal back to start

❇️Why This Project Is Good

- Demonstrates understanding of informed search algorithms
- Shows comparison between A*, IDA*, and RBFS
- Includes performance analysis
- Clean structure and modular functions
- Strong input validation

⚙️Requirements
Python 3.x
Install psutil : pip install psutil
