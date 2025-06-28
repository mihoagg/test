import pytest
from main import DLS, is_goal

# File: tests/test_dls.py

def make_structs():
    return set(), set(), {}

def test_goal_at_start():
    maze = [
        [0, 'G'],
        ['S', 0]
    ]
    explored, all_explored, parent = make_structs()
    result = DLS(maze, (0,1), explored, all_explored, parent, 1)
    assert result == (0,1) or is_goal(result, maze)

def test_goal_unreachable_blocked():
    maze = [
        [1, 'G'],
        ['S', 1]
    ]
    explored, all_explored, parent = make_structs()
    result = DLS(maze, (0,1), explored, all_explored, parent, 10)
    assert result is None

def test_goal_depth_1():
    maze = [
        [0, 'G'],
        ['S', 0]
    ]
    explored, all_explored, parent = make_structs()
    result = DLS(maze, (0,1), explored, all_explored, parent, 1)
    assert result == (1,0) or is_goal(result, maze)

def test_goal_depth_2():
    maze = [
        [0, 0, 'G'],
        ['S', 1, 1]
    ]
    explored, all_explored, parent = make_structs()
    result = DLS(maze, (0,1), explored, all_explored, parent, 3)
    assert result == (2,0) or is_goal(result, maze)

def test_multiple_goals():
    maze = [
        [0, 'G', 0],
        ['S', 0, 'G']
    ]
    explored, all_explored, parent = make_structs()
    result = DLS(maze, (0,1), explored, all_explored, parent, 3)
    assert result in [(1,0), (2,1)] or is_goal(result, maze)

def test_no_goal():
    maze = [
        [0, 0],
        ['S', 0]
    ]
    explored, all_explored, parent = make_structs()
    result = DLS(maze, (0,1), explored, all_explored, parent, 5)
    assert result is None

def test_start_surrounded_by_walls():
    maze = [
        [1, 1, 1],
        [1, 'S', 1],
        [1, 1, 1]
    ]
    explored, all_explored, parent = make_structs()
    result = DLS(maze, (1,1), explored, all_explored, parent, 10)
    assert result is None

def test_multiple_paths():
    maze = [
        ['S', 0, 0, 'G'],
        [1, 1, 0, 1]
    ]
    explored, all_explored, parent = make_structs()
    result = DLS(maze, (0,0), explored, all_explored, parent, 5)
    assert result == (3,0) or is_goal(result, maze)

def test_large_depth_limit_goal_close():
    maze = [
        ['S', 'G', 0, 0]
    ]
    explored, all_explored, parent = make_structs()
    result = DLS(maze, (0,0), explored, all_explored, parent, 100)
    assert result == (1,0) or is_goal(result, maze)

def test_goal_at_max_depth():
    maze = [
        ['S', 0, 0, 0, 'G']
    ]
    explored, all_explored, parent = make_structs()
    result = DLS(maze, (0,0), explored, all_explored, parent, 4)
    assert result == (4,0) or is_goal(result, maze)