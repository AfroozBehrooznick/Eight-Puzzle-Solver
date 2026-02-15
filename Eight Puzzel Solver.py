# 8-Puzzle Solver (A*, IDA*, RBFS)
# Created by Afrooz Behrooznick 
import sys
import os
import time
import math
import random
import heapq

try:
    import resource  
    _RESOURCE_AVAILABLE = True
except ImportError:
    _RESOURCE_AVAILABLE = False

try:
    import psutil  
    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False



GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
BOARD_SIZE = 3
EXIT_WORDS = {"exit", "quit", "q", "x"}



def safe_input(prompt):
    # Input that allows user to exit cleanly - At any prompt in this program type < exit / quit / q / x > to terminate the program immediately
    try:
        value = input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting program...")
        sys.exit(0)

    if value.strip().lower() in EXIT_WORDS:
        print("Exiting program...")
        sys.exit(0)
    return value


def print_puzzle_grid(state):
    # Display puzzle in a text grid
    n = BOARD_SIZE
    print("\n+-----+-----+-----+")
    for row in range(n):
        print("|", end="")
        offset = row * n
        for col in range(n):
            value = state[offset + col]
            if value == 0:
                cell = "  _  "
            else:
                cell = f"  {value}  "
            print(cell + "|", end="")
        print()
        if row < n - 1:
            print("+-----+-----+-----+")
    print("+-----+-----+-----+\n")


# Utility Functions
def manhattan_distance(x1, y1, x2, y2):
    #Return Manhattan distance between (x1, y1) and (x2, y2)
    return abs(x1 - x2) + abs(y1 - y2)


def euclidean_distance(x1, y1, x2, y2):
    #Return Euclidean distance between (x1, y1) and (x2, y2)
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def heuristic_manhattan(state, goal):
    # Manhattan heuristic for a given puzzle state
    h = 0
    n = BOARD_SIZE
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        current_row, current_col = divmod(i, n)
        goal_index = goal.index(tile)
        goal_row, goal_col = divmod(goal_index, n)
        h += manhattan_distance(current_row, current_col, goal_row, goal_col)
    return h


def heuristic_euclidean(state, goal):
    #Euclidean heuristic for a given puzzle state
    h = 0.0
    n = BOARD_SIZE
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        current_row, current_col = divmod(i, n)
        goal_index = goal.index(tile)
        goal_row, goal_col = divmod(goal_index, n)
        h += euclidean_distance(current_row, current_col, goal_row, goal_col)
    return h


def is_solvable(state):
    # Return True if the 8-puzzle configuration is solvable - Condition for 8-puzzle = Number of inversions must be even
    arr = [x for x in state if x != 0]
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions % 2 == 0


def get_neighbors(state):
    # Generate all neighbor states of a given state
    # Returns list of 'next state and action' where action is one of < "Up", "Down", "Left", "Right" >
    n = BOARD_SIZE
    index_blank = state.index(0)
    row_blank, col_blank = divmod(index_blank, n)
    neighbors = []

    # Up
    if row_blank > 0:
        target_index = index_blank - n
        new_state = list(state)
        new_state[index_blank], new_state[target_index] = new_state[target_index], new_state[index_blank]
        neighbors.append((tuple(new_state), "Up"))

    # Down
    if row_blank < n - 1:
        target_index = index_blank + n
        new_state = list(state)
        new_state[index_blank], new_state[target_index] = new_state[target_index], new_state[index_blank]
        neighbors.append((tuple(new_state), "Down"))

    # Left
    if col_blank > 0:
        target_index = index_blank - 1
        new_state = list(state)
        new_state[index_blank], new_state[target_index] = new_state[target_index], new_state[index_blank]
        neighbors.append((tuple(new_state), "Left"))

    # Right
    if col_blank < n - 1:
        target_index = index_blank + 1
        new_state = list(state)
        new_state[index_blank], new_state[target_index] = new_state[target_index], new_state[index_blank]
        neighbors.append((tuple(new_state), "Right"))

    return neighbors


def reconstruct_path(parent_map, action_map, goal_state):
    # Reconstruct path of states and actions from parent_map and action_map
    states_path = [goal_state]
    actions_path = []
    current = goal_state

    while current in parent_map:
        parent = parent_map[current]
        act = action_map[current]
        states_path.append(parent)
        if act is not None:
            actions_path.append(act)
        current = parent

    states_path.reverse()
    actions_path.reverse()
    return states_path, actions_path




# A* Search algorithm 
def a_star_search(start_state, goal_state, heuristic_fn):
    open_heap = []
    g_cost = {start_state: 0}
    parent = {}
    action_from_parent = {}

    h0 = heuristic_fn(start_state, goal_state)
    f0 = g_cost[start_state] + h0
    heapq.heappush(open_heap, (f0, 0, 0, start_state))

    closed = set()
    nodes_expanded = 0
    max_search_depth = 0

    while open_heap:
        f, g, depth, state = heapq.heappop(open_heap)

        if state in closed:
            continue
        closed.add(state)

        if state == goal_state:
            states_path, actions_path = reconstruct_path(parent, action_from_parent, state)
            return {
                "path_to_goal": actions_path,
                "cost_of_path": len(actions_path),
                "nodes_expanded": nodes_expanded,
                "search_depth": len(actions_path),
                "max_search_depth": max_search_depth,
                "states_path": states_path,
            }

        nodes_expanded += 1

        for neighbor, action in get_neighbors(state):
            tentative_g = g + 1 #cost

            if neighbor in g_cost and tentative_g >= g_cost[neighbor]:
                continue

            g_cost[neighbor] = tentative_g
            h = heuristic_fn(neighbor, goal_state)
            f_new = tentative_g + h
            heapq.heappush(open_heap, (f_new, tentative_g, depth + 1, neighbor))
            parent[neighbor] = state
            action_from_parent[neighbor] = action

            if depth + 1 > max_search_depth:
                max_search_depth = depth + 1
    
    return None # No solution



# IDA* Search algorithm (Iterative Deepening A*) 
def ida_star_search(start_state, goal_state, heuristic_fn):

    def search(path, g, bound, nodes_expanded_info, max_depth_info):
        state = path[-1]
        f = g + heuristic_fn(state, goal_state)
        if f > bound:
            return f
        if state == goal_state:
            return "FOUND"

        minimum = float("inf")
        for neighbor, action in get_neighbors(state):
            if neighbor in path:
                continue
            nodes_expanded_info[0] += 1
            path.append(neighbor)
            depth = len(path) - 1
            if depth > max_depth_info[0]:
                max_depth_info[0] = depth
            result = search(path, g + 1, bound, nodes_expanded_info, max_depth_info)
            if result == "FOUND":
                parent_map[neighbor] = state
                action_map[neighbor] = action
                return "FOUND"
            if isinstance(result, (int, float)) and result < minimum:
                minimum = result
            path.pop()
        return minimum


    parent_map = {}
    action_map = {}

    bound = heuristic_fn(start_state, goal_state)
    nodes_expanded_info = [0]
    max_depth_info = [0]

    path = [start_state]
    while True:
        t = search(path, 0, bound, nodes_expanded_info, max_depth_info)
        if t == "FOUND":
            # Reconstruct by walking back from goal_state to start_state .Because parent_map only stores direct edges we used when "FOUND"
            # The final state is the last element in path
            goal = path[-1]
            # parent_map and action_map are only partially filled - complete them
            for i in range(1, len(path)):
                parent_map[path[i]] = path[i - 1]
                # The action here is not stored. to avoid complexity, we will recompute actions by comparing states
                action_map[path[i]] = infer_action(path[i - 1], path[i])

            states_path, actions_path = reconstruct_path(parent_map, action_map, goal)
            return {
                "path_to_goal": actions_path,
                "cost_of_path": len(actions_path),
                "nodes_expanded": nodes_expanded_info[0],
                "search_depth": len(actions_path),
                "max_search_depth": max_depth_info[0],
                "states_path": states_path,
            }

        if t == float("inf"):
            return None
        bound = t


def infer_action(prev_state, next_state):
    # Infer the move action name between two states < This is used only as a fallback for IDA* path reconstruction >
    n = BOARD_SIZE
    idx_prev_blank = prev_state.index(0)
    idx_next_blank = next_state.index(0)
    row_prev, col_prev = divmod(idx_prev_blank, n)
    row_next, col_next = divmod(idx_next_blank, n)

    dr = row_next - row_prev
    dc = col_next - col_prev

    # If the blank moved down, the tile moved Up
    if dr == 1 and dc == 0:
        return "Up"
    if dr == -1 and dc == 0:
        return "Down"
    if dr == 0 and dc == 1:
        return "Left"
    if dr == 0 and dc == -1:
        return "Right"
    return "Unknown"



# RBFS (Recursive Best First Search)
def rbfs_search(start_state, goal_state, heuristic_fn):

    def make_node(state, g, parent_state, action):
        h = heuristic_fn(state, goal_state)
        f = g + h
        depth = g  # each move = cost 1
        return {
            "state": state,
            "g": g,
            "f": f,
            "parent": parent_state,
            "action": action,
            "depth": depth,
        }

    nodes_expanded_info = [0]
    max_depth_info = [0]

    start_node = make_node(start_state, 0, None, None)

    def rbfs(node, f_limit):
        if node["state"] == goal_state:
            return node, 0

        successors = []
        for neighbor, action in get_neighbors(node["state"]):
            g_new = node["g"] + 1
            child = make_node(neighbor, g_new, node, action)
            successors.append(child)

        nodes_expanded_info[0] += 1

        if not successors:
            return None, float("inf")

        for child in successors:
            if child["depth"] > max_depth_info[0]:
                max_depth_info[0] = child["depth"]
            child["f"] = max(child["f"], node["f"])

        while True:
            successors.sort(key=lambda n: n["f"])
            best = successors[0]
            if best["f"] > f_limit:
                return None, best["f"]
            alternative = successors[1]["f"] if len(successors) > 1 else float("inf")
            result, best["f"] = rbfs(best, min(f_limit, alternative))
            if result is not None:
                return result, best["f"]

    result_node, _ = rbfs(start_node, float("inf"))
    if result_node is None:
        return None


    states_path = []
    actions_path = []
    current = result_node
    while current is not None:
        states_path.append(current["state"])
        if current["action"] is not None:
            actions_path.append(current["action"])
        current = current["parent"]

    states_path.reverse()
    actions_path.reverse()

    return {
        "path_to_goal": actions_path,
        "cost_of_path": len(actions_path),
        "nodes_expanded": nodes_expanded_info[0],
        "search_depth": len(actions_path),
        "max_search_depth": max_depth_info[0],
        "states_path": states_path,
    }


# Performance Measurement
def measure_and_solve(start_state, goal_state, algorithm_name, heuristic_name):
    # Its selects algorithm, measures time and memory, and returns combined result
    if heuristic_name == "manhattan":
        heuristic_fn = heuristic_manhattan
    else:
        heuristic_fn = heuristic_euclidean

    if algorithm_name == "a_star":
        solver_fn = a_star_search
    elif algorithm_name == "ida_star":
        solver_fn = ida_star_search
    else:  # "rbfs"
        solver_fn = rbfs_search

    # Initial memory
    if _RESOURCE_AVAILABLE:
        mem_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    elif _PSUTIL_AVAILABLE:
        process = psutil.Process(os.getpid())
        mem_init = process.memory_info().rss / (1024 * 1024)
    else:
        mem_init = 0.0

    start_time = time.time()
    result = solver_fn(start_state, goal_state, heuristic_fn)
    running_time = time.time() - start_time

    # Final memory
    ram_usage = None
    if _RESOURCE_AVAILABLE:
        mem_final = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        ram_usage = (mem_final - mem_init) / 1024.0  # KB -> MB
    elif _PSUTIL_AVAILABLE:
        process = psutil.Process(os.getpid())
        mem_final = process.memory_info().rss / (1024 * 1024)
        ram_usage = mem_final - mem_init

    if result is None:
        return None

    result["running_time"] = running_time
    result["ram_usage_mb"] = ram_usage
    result["algorithm"] = algorithm_name
    result["heuristic"] = heuristic_name
    return result



def get_predefined_puzzle():
    # Allow the user choose one of several predefined puzzles
    puzzles = {
        1: (1, 2, 3, 4, 5, 6, 7, 8, 0),  # Solved
        2: (1, 2, 3, 4, 5, 6, 0, 7, 8),  # Easy
        3: (1, 2, 3, 4, 0, 5, 7, 8, 6),  # Medium
        4: (0, 1, 2, 4, 5, 3, 7, 8, 6),  # Hard
        5: (8, 1, 3, 4, 0, 2, 7, 6, 5),  # Very Hard
    }

    print("\nPredefined puzzles:")
    print("1. Solved         (1, 2, 3, 4, 5, 6, 7, 8, 0)")
    print("2. Easy           (1, 2, 3, 4, 5, 6, 0, 7, 8)")
    print("3. Medium         (1, 2, 3, 4, 0, 5, 7, 8, 6)")
    print("4. Hard           (0, 1, 2, 4, 5, 3, 7, 8, 6)")
    print("5. Very Hard      (8, 1, 3, 4, 0, 2, 7, 6, 5)")
    print("Type 'exit' to quit.")

    while True:
        raw = safe_input("Select puzzle number (1-5): ").strip()
        if not raw.isdigit():
            print("[Error] Please enter a valid number between 1 and 5.")
            continue

        choice = int(raw)
        if choice in puzzles:
            return puzzles[choice]
        print("[Error] Please enter a number between 1 and 5.")


def get_manual_puzzle():
    # Read puzzle configuration from keyboard, User must enter 9 distinct numbers from 0 to 8, comma-separated
    print("\nManual puzzle entry.")
    print("Enter numbers from left-to-right, top-to-bottom.")
    print("Use 0 for the blank cell.")
    print("Example: 1,2,3,4,5,6,7,8,0")
    print("Type 'exit' to quit.")

    while True:
        raw = safe_input("Enter puzzle (comma-separated 9 numbers): ")
        parts = [p.strip() for p in raw.split(",") if p.strip() != ""]
        if len(parts) != 9:
            print("[Error] Exactly 9 numbers are required.")
            continue
        try:
            nums = [int(x) for x in parts]
        except ValueError:
            print("[Error] Please enter only integer numbers between 0 and 8.")
            continue

        if any(n < 0 or n > 8 for n in nums):
            print("[Error] All numbers must be between 0 and 8.")
            continue

        if len(set(nums)) != 9:
            print("[Error] Numbers must be unique (0-8 with no duplicates).")
            continue

        return tuple(nums)


def shuffle_from_goal(goal_state, num_shuffles):
    # Shuffle a solved puzzle by performing random valid moves, This guarantees the puzzle remains solvable
    state = list(goal_state)
    n = BOARD_SIZE

    for _ in range(num_shuffles):
        idx_blank = state.index(0)
        row_blank, col_blank = divmod(idx_blank, n)

        moves = []
        if row_blank > 0:
            moves.append("Up")
        if row_blank < n - 1:
            moves.append("Down")
        if col_blank > 0:
            moves.append("Left")
        if col_blank < n - 1:
            moves.append("Right")

        move = random.choice(moves)
        for neighbor, action in get_neighbors(tuple(state)):
            if action == move:
                state = list(neighbor)
                break

    return tuple(state)


def get_shuffled_puzzle():
    # Ask for number of shuffles and return a shuffled puzzle
    print("\nShuffle solved puzzle.")
    print("Type 'exit' to quit.")

    while True:
        raw = safe_input("Enter number of random moves (recommended 20-100): ").strip()
        if not raw.isdigit():
            print("[Error] Please enter a positive integer number.")
            continue

        n_moves = int(raw)
        if n_moves < 1:
            print("[Error] Number of moves must be at least 1.")
            continue
        if n_moves > 1000:
            print("[Warning] Very large number; solving may be slow.")
            confirm = safe_input("Are you sure you want to continue? (y/n): ").strip().lower()
            if confirm != "y":
                continue

        shuffled = shuffle_from_goal(GOAL_STATE, n_moves)
        print("[Info] Puzzle shuffled successfully.")
        return shuffled


def choose_heuristic():
    # Choose heuristic function
    print("\nChoose heuristic function (type 'exit' to quit):")
    print("1. Manhattan distance")
    print("2. Euclidean distance")

    while True:
        raw = safe_input("Select heuristic (1-2): ").strip()
        if not raw.isdigit():
            print("[Error] Please enter 1 or 2.")
            continue
        choice = int(raw)
        if choice == 1:
            return "manhattan"
        if choice == 2:
            return "euclidean"
        print("[Error] Please enter 1 or 2.")


def choose_algorithm():
    # Choose search algorithm
    print("\nChoose search algorithm (type 'exit' to quit):")
    print("1. A* ")
    print("2. IDA* ")
    print("3. RBFS ")

    while True:
        raw = safe_input("Select algorithm (1-3): ").strip()
        if not raw.isdigit():
            print("[Error] Please enter 1, 2 or 3.")
            continue
        choice = int(raw)
        if choice == 1:
            return "a_star"
        if choice == 2:
            return "ida_star"
        if choice == 3:
            return "rbfs"
        print("[Error] Please enter 1, 2 or 3.")


def show_solution_path(states_path, actions_path):
    # Print the solution path step by step 
    if not states_path:
        return

    for idx, state in enumerate(states_path):
        if idx == 0:
            step_label = "[Step 0] Initial state"
        else:
            step_label = f"[Step {idx}] Move: {actions_path[idx - 1]}"

        print(step_label)
        print_puzzle_grid(state)
        if idx < len(states_path) - 1:
            print("  |")
            print("  v")

    print(f"[Result] Total moves: {len(states_path) - 1}")


def print_result_summary(result):
    # Print final statistics of the search
    print("=" * 60)
    print("[Results] 8-Puzzle solution summary")
    print("=" * 60)
    print(f"Algorithm:         {result['algorithm']}")
    print(f"Heuristic:         {result['heuristic']}")
    print(f"Path to goal:      {result['path_to_goal']}")
    print(f"Cost of path:      {result['cost_of_path']} moves")
    print(f"Nodes expanded:    {result['nodes_expanded']}")
    print(f"Search depth:      {result['search_depth']}")
    print(f"Max search depth:  {result['max_search_depth']}")
    print(f"Running time:      {result['running_time']:.6f} seconds")
    if result["ram_usage_mb"] is not None:
        print(f"Memory used:     {result['ram_usage_mb']:.4f} MB")
    else:
        print("Memory used:     Not available on this platform")
    print("=" * 60)


def main():
    # ("exit" / "quit" / "q" / "x") terminates the program 
    print("=" * 60)
    print("8-Puzzle Solver (A*, IDA*, RBFS)")
    print("\nType 'exit' or 'q' at any prompt to quit the program.")
    print("=" * 60)

    while True:
        print("\nChoose puzzle input method:")
        print("1. Predefined puzzle")
        print("2. Manual entry")
        print("3. Shuffle solved puzzle")
        print("Type 'exit' to quit.")

        # Choose input method
        while True:
            raw = safe_input("Select method (1-3): ").strip()
            if not raw.isdigit():
                print("[Error] Please enter 1, 2 or 3.")
                continue
            method = int(raw)
            if method in (1, 2, 3):
                break
            print("[Error] Please enter 1, 2 or 3.")

        # Get puzzle according to selected method
        if method == 1:
            start_state = get_predefined_puzzle()
        elif method == 2:
            start_state = get_manual_puzzle()
        else:
            start_state = get_shuffled_puzzle()

        print("=" * 60)
        print("[Initial puzzle]")
        print_puzzle_grid(start_state)

        if not is_solvable(start_state):
            print("[Error] This puzzle configuration is not solvable.")
            print("Please choose or enter another start state.")
            continue

        heuristic_name = choose_heuristic()
        algorithm_name = choose_algorithm()

        print("=" * 60)
        print(f"Solving with algorithm: {algorithm_name} | heuristic: {heuristic_name}")
        print("Please wait...")

        result = measure_and_solve(start_state, GOAL_STATE, algorithm_name, heuristic_name)
        if result is None:
            print("=" * 60)
            print("[Error] No solution found by the selected algorithm.")
            print("=" * 60)
        else:
            print_result_summary(result)
            print("\n[Path] Solution steps:")
            print("=" * 60)
            show_solution_path(result["states_path"], result["path_to_goal"])

        # Ask user if they want to solve another puzzle
        again = safe_input("Solve another puzzle? (y/n, or 'exit'): ").strip().lower()
        if again not in {"y", "yes"}:
            print("Exiting program. Goodbye.")
            break

main()