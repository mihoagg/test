from collections import deque
import heapq
import itertools
from math import inf
import re
import sys

# test_maze = [
#     [0,0,1,1,0,0,0,"G",1,0,1],
#     ["S",0,1,1,0,0,0,0,1,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,1,0,0,0,0,0,0,1,"G"],
#     [0,0,1,1,1,1,0,0,1,1,0],
# ]

def print_maze(maze):
    # Print column indices
    print("   ", end="")
    for x in range(len(maze[0])):
        print(f"{x:2} ", end="")
    print()

    for y in range(len(maze)):
        print(f"{y:2} ", end="")  # Row index
        for x in range(len(maze[0])):
            cell = maze[y][x]
            if cell == 1:
                print("⬛ ", end="")  # Wall
            elif cell == 0:
                print(".  ", end="")  # Walkable path
            elif cell == "S":
                print("S  ", end="")  # Start
            elif cell == "G":
                print("G  ", end="")  # Goal
            else:
                print("?  ", end="")  # Unknown
        print()

def parse_problem_file(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Parse maze size
    rows, cols = eval(lines[0])
    maze = [[0 for _ in range(cols)] for _ in range(rows)]

    # Parse start (x, y) → (col, row)
    x, y = eval(lines[1])
    if 0 <= y < rows and 0 <= x < cols:
        maze[y][x] = 'S'
    else:
        raise ValueError(f"Start position ({x}, {y}) is out of bounds.")

    # Parse goals
    goal_coords = re.findall(r'\((\d+),(\d+)\)', lines[2])
    for gx, gy in [(int(x), int(y)) for x, y in goal_coords]:
        if 0 <= gy < rows and 0 <= gx < cols:
            if maze[gy][gx] == 0:
                maze[gy][gx] = 'G'
        else:
            print(f"⚠️ Goal ({gx},{gy}) is out of bounds and will be ignored.")

    # Parse walls (x, y, w, h)
    for wall_line in lines[3:]:
        x, y, w, h = eval(wall_line)
        for dy in range(h):
            for dx in range(w):
                row = y + dy
                col = x + dx
                if 0 <= row < rows and 0 <= col < cols:
                    if maze[row][col] in [0, 'G']:
                        maze[row][col] = 1

    return maze



def find_start(maze):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == "S":
                return (x, y)
                        
def get_neighbors(maze, location):
    x,y = location
    directions = [(-1,0),(0,-1),(1,0),(0,1)] #up, left, down, right
    neighbors = []
    
    for dx, dy in directions: #calculate neighbors xy
        nx = x + dx
        ny = y + dy
        
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
            if maze[ny][nx] != 1:
                neighbors.append((nx,ny))
        
    return neighbors

def is_goal(node, maze):
    x, y = node
    return maze[y][x] == "G"

def path_to_directions(path):
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # left, up, right, down in (x, y)
    # labels = ["Left", "Up", "Right", "Down"]
    labels = ["Up", "Left", "Down", "Right"]
    
    result = []
    for i in range(1, len(path)):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]
        dx, dy = x2 - x1, y2 - y1
        move = (dx, dy)
        if move in directions:
            result.append(labels[directions.index(move)])
        else:
            result.append("Unknown")
    return result

def reconstruct_path(parent, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    path = path_to_directions(path)  # Convert to directions
    return path
    
def find_goals(maze):
    goals = []
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == "G":
                goals.append((x, y))
    return goals

def DLS(maze, node, explored, all_explored, parent, maxDepth): # Depth-Limited Search
    #print(f"Exploring node: {node} at depth {maxDepth}")
    if is_goal(node, maze): 
        return node

    if maxDepth == 0:
        return None

    explored.add(node)
    all_explored.add(node)  # Track all explored nodes globally
    
    for neighbor in get_neighbors(maze, node):
        if neighbor not in explored:
            parent[neighbor] = node  # if tracking path
            #print(f"Adding neighbor: {neighbor} at depth {maxDepth-1}")
            # Recursively call DLS on the neighbor
            result = DLS(maze, neighbor, explored, all_explored, parent, maxDepth-1)
            if result is not None:
                return result
    
    explored.remove(node) #backtrack to allow revisiting from other paths
    return None

def manhatan_distance(n, goals):
    h_ns = []
    for goal in goals:
        gx, gy = goal
        nx, ny = n
        # Calculate Manhattan distance
        h_n = abs(gx - nx) + abs(gy - ny)
        h_ns.append(h_n)
    return min(h_ns) # Return the minimum
    
def depth_first_search(maze, start):
    frontier = deque()
    frontier.append(start) #add start node to frontier
    explored = set() #track explored nodes to avoid loop
    parent = {}  # Track where each node came from
    
    while frontier:
        node = frontier.pop() #start from first node
        #print(f"Exploring node: {node}")
        if is_goal(node, maze): #return solution of finished
            path = reconstruct_path(parent, start, node) 
            nodes_explored = len(explored) + 1  # +1 for the current node
            return (node, path, nodes_explored) 
        if node not in explored:
            explored.add(node) #add node to explored
            for neighbor in reversed(get_neighbors(maze,node)): #reversed list to ensure pop work in correct order
                if neighbor not in explored:
                    frontier.append(neighbor) #add next nodes to frontier
                    #print(f"Adding neighbor: {neighbor}")
                    parent[neighbor] = node
                    
    return len(explored) #return failed

def breadth_first_search(maze, start):
    frontier = deque()
    frontier.append(start) #add start node to frontier
    explored = set() #track explored nodes to avoid loop
    parent = {}  # Track where each node came from
    
    while frontier:
        node = frontier.popleft() #start from first node
        #print(f"Exploring node: {node}")
        if is_goal(node, maze): 
            path = reconstruct_path(parent, start, node) 
            nodes_explored = len(explored) + 1  # +1 for the current node
            return (node, path, nodes_explored) 
        
        if node not in explored:
            explored.add(node) #add node to explored
            for neighbor in get_neighbors(maze,node):
                if neighbor not in explored and neighbor not in frontier:
                    frontier.append(neighbor) #add next nodes to frontier
                    #print(f"Adding neighbor: {neighbor}")
                    parent[neighbor] = node
                    
    return len(explored) #return failed
        
def greedy_best_first_search(maze, start):
    frontier = []
    counter = itertools.count() # Create a counter to break ties in the priority queue to ensure priority of direction
    heapq.heappush(frontier, (0, next(counter), start))
    explored = set()  # Track explored nodes
    parent = {}  # Track where each node came from
    
    while frontier:
        hn, _, node = heapq.heappop(frontier)
        #print(f"Exploring node: {node} with heuristic: {hn}")
        
        if is_goal(node, maze):
            path = reconstruct_path(parent, start, node) 
            nodes_explored = len(explored) + 1  # +1 for the current node
            return (node, path, nodes_explored) 
        
        if node not in explored:
            explored.add(node)
            for neighbor in get_neighbors(maze, node):
                if neighbor not in explored and neighbor not in [n[1] for n in frontier]:
                    h_n = manhatan_distance(neighbor, find_goals(maze))
                    heapq.heappush(frontier, (h_n, next(counter), neighbor))
                    #print(f"Adding neighbor: {neighbor} with heuristic: {h_n}")
                    parent[neighbor] = node
    
    return len(explored)

def a_star_search(maze, start):
    frontier = []
    counter = itertools.count()
    heapq.heappush(frontier, (0, next(counter), start))
    explored = set()  # Track explored nodes
    parent = {}  # Track where each node came from
    g_scores = {start: 0}  # Track g(n) scores for A* search
    
    while frontier:
        hn, _, node = heapq.heappop(frontier)
        #print(f"Exploring node: {node} with heuristic: {hn}")
        
        if is_goal(node, maze):
            path = reconstruct_path(parent, start, node) 
            nodes_explored = len(explored) + 1  # +1 for the current node
            return (node, path, nodes_explored) 
        
        if node in explored:
            continue
        
        if node not in explored:
            explored.add(node)
            for neighbor in get_neighbors(maze, node):
                tentative_g = g_scores[node] + 1  # Assuming uniform cost (1 per move)
                
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    h_n = manhatan_distance(neighbor, find_goals(maze))
                    # f(n) = g(n) + h(n)
                    f_n = tentative_g + h_n
                    heapq.heappush(frontier, (f_n, next(counter), neighbor))
                    #print(f"Adding neighbor: {neighbor} with f(n): {f_n}")
                    parent[neighbor] = node
    
    return len(explored)  # Return the number of explored nodes if no goal is found

def iterative_deepening_search(maze, start, depth_limit=None):
    max_depth = 0
    all_explored = set()
    
    while True:
        if depth_limit is not None and max_depth > depth_limit:
            return len(all_explored)  # Exceeded known tree depth; stop searching

        explored = set()
        parent = {}
        result = DLS(maze, start, explored, all_explored, parent, max_depth)
        
        
        if result is not None:
            goal = result
            path = reconstruct_path(parent, start, goal)
            nodes_explored = len(all_explored)
            return (goal, path, nodes_explored)
        max_depth += 1

def iterative_deepening_a_star_search(maze, start):
    goals = find_goals(maze)
    all_explored = set()  # Track all explored nodes globally

    def DLS(node, g, threshold, explored, parent):
        f = g + manhatan_distance(node, goals)
        if f > threshold:
            return f  # Return this f to update the next threshold

        if is_goal(node, maze):
            return node

        explored.add(node)
        all_explored.add(node)  # Track all explored nodes globally

        min_exceeding = float('inf')

        for neighbor in get_neighbors(maze, node):
            if neighbor not in explored:
                parent[neighbor] = node
                result = DLS(neighbor, g + 1, threshold, explored, parent)
                if isinstance(result, (int, float)):
                    min_exceeding = min(min_exceeding, result)
                elif result is not None:
                    return result

        explored.remove(node)  # Backtrack
        return min_exceeding

    threshold = manhatan_distance(start, goals)
    while True:
        explored = set()
        parent = {}
        result = DLS(start, 0, threshold, explored, parent)
        # If result is a coordinate (tuple of two ints), it's a goal node
        if isinstance(result, tuple) and len(result) == 2 and all(isinstance(i, int) for i in result):
            goal = result
            path = reconstruct_path(parent, start, goal)
            nodes_explored = len(all_explored)
            return (goal, path, nodes_explored)
        elif isinstance(result, (int, float)) and result != float('inf'):
            threshold = result  # Increase threshold and continue
        elif isinstance(result, (int, float)) and result == float('inf'):
            return len(all_explored)  # No path exists
        elif result is not None:
            # Found goal node (not a tuple, not a number)
            goal = result
            path = reconstruct_path(parent, start, goal)
            nodes_explored = len(all_explored)
            return (goal, path, nodes_explored)



def main():
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    # Load the maze from the file
    maze = parse_problem_file(filename)
    start = find_start(maze)
    goals = find_goals(maze)

    # Dictionary of method names to function references
    methods = {
        'DFS': depth_first_search,
        'BFS': breadth_first_search,
        'GBFS': greedy_best_first_search,
        'AS': a_star_search,
        'CUS1': iterative_deepening_search,
        'CUS2': iterative_deepening_a_star_search,
    }

    if method not in methods:
        print(f"Unknown method: {method}")
        sys.exit(1)

    result = methods[method](maze, start)

    print(f"{filename} {method}")
    if result:
        goal, path, nodes_explored = result
        print(f"{goal} {nodes_explored}")
        print(' '.join(path))
    else:
        print(f"No goal is reachable; {result}")
    
    
    
    #Use the sample maze defined above
    # start = find_start(test_maze)
    # methods = {
    #     'DFS': depth_first_search,
    #     'BFS': breadth_first_search,
    #     'GBFS': greedy_best_first_search,
    #     'AS': a_star_search,
    #     'CUS1': iterative_deepening_search,
    #     'CUS2': iterative_deepening_a_star_search,  # Uncomment if implemented correctly
    # }

    # print_maze(test_maze)
    # print("\nTesting all search methods:\n")
    # for name, func in methods.items():
    #     print(f"--- {name} ---")
    #     try:
    #         result = func(test_maze, start)
    #         if isinstance(result, tuple):
    #             goal, path, nodes_explored = result
    #             print(f"Goal: {goal}")
    #             print(f"Path: {path}")
    #             print(f"Nodes explored: {nodes_explored}")
    #         else:
    #             print(f"No goal found; nodes explored: {result}")
    #     except Exception as e:
    #         print(f"Error running {name}: {e}")
    #     print()
    
    
if __name__ == '__main__':
    main()
