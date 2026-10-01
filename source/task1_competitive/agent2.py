import heapq
import time
from board_2 import wall

DIRECTIONS = {
    'North': (0, -1),
    'South': (0, 1),
    'East': (1, 0),
    'West': (-1, 0)
}

def get_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_safe_neighbors(grid, pos, obstacles):
    neighbors = []
    for act, (dx, dy) in DIRECTIONS.items():
        nxt = (pos[0] + dx, pos[1] + dy)
        if not wall(grid, nxt[0], nxt[1]) and nxt not in obstacles:
            neighbors.append((act, nxt))
    return neighbors

def find_path_bfs(grid, start, target, obstacles, max_time=0.8):
    """Tìm đường nhanh bằng BFS có time-limit"""
    start_time = time.time()
    queue = [(start, [])]
    visited = {start}

    while queue:
        if time.time() - start_time > max_time:
            break
        current, path = queue.pop(0)
        if current == target:
            return path

        for act, nxt in get_safe_neighbors(grid, current, obstacles):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [act]))
    return []

def get_next_action(grid, my_pos, opponent_pos, boxes, goals, remaining_steps):
    """
    Agent 2: Ra quyết định trong < 1000ms.
    """
    obstacles = set(boxes) | {opponent_pos}

    sorted_boxes = sorted(boxes, key=lambda b: get_manhattan(my_pos, b))
    if not sorted_boxes:
        return 'Wait'

    target_box = sorted_boxes[0]
    sorted_goals = sorted(goals, key=lambda g: get_manhattan(target_box, g))
    target_goal = sorted_goals[0] if sorted_goals else target_box

    best_push_action = None
    min_dist = float('inf')
    push_stand_pos = None

    for act, (dx, dy) in DIRECTIONS.items():
        box_next = (target_box[0] + dx, target_box[1] + dy)
        stand_pos = (target_box[0] - dx, target_box[1] - dy)

        if not wall(grid, stand_pos[0], stand_pos[1]) and stand_pos != opponent_pos:
            if not wall(grid, box_next[0], box_next[1]) and box_next not in boxes and box_next != opponent_pos:
                dist = get_manhattan(box_next, target_goal)
                if dist < min_dist:
                    min_dist = dist
                    best_push_action = act
                    push_stand_pos = stand_pos

    if my_pos == push_stand_pos and best_push_action:
        return best_push_action

    target_pos = push_stand_pos if push_stand_pos else target_box
    clean_obs = obstacles - {target_pos}
    path = find_path_bfs(grid, my_pos, target_pos, clean_obs, max_time=0.6)

    if path:
        return path[0]

    for act, (dx, dy) in DIRECTIONS.items():
        nxt = (my_pos[0] + dx, my_pos[1] + dy)
        if not wall(grid, nxt[0], nxt[1]) and nxt not in obstacles:
            return act

    return 'Wait'