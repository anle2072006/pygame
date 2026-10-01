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

def get_neighbors(grid, pos, obstacles):
    neighbors = []
    for act, (dx, dy) in DIRECTIONS.items():
        nxt = (pos[0] + dx, pos[1] + dy)
        if not wall(grid, nxt[0], nxt[1]) and nxt not in obstacles:
            neighbors.append((act, nxt))
    return neighbors

def find_path_astar(grid, start, target, obstacles, max_time=0.8):
    """Tìm đường ngắn nhất từ start đến target bằng A* tránh obstacles"""
    start_time = time.time()
    pq = [(get_manhattan(start, target), 0, start, [])]
    visited = {start: 0}

    while pq:
        if time.time() - start_time > max_time:
            break
        _, cost, current, path = heapq.heappop(pq)
        if current == target:
            return path

        for act, nxt in get_neighbors(grid, current, obstacles):
            new_cost = cost + 1
            if nxt not in visited or new_cost < visited[nxt]:
                visited[nxt] = new_cost
                priority = new_cost + get_manhattan(nxt, target)
                heapq.heappush(pq, (priority, new_cost, nxt, path + [act]))
    return []

def get_next_action(grid, my_pos, opponent_pos, boxes, goals, remaining_steps):
    """
    Quyết định hành động tiếp theo trong vòng dưới 1000ms.
    Trả về: 'North', 'South', 'East', 'West', hoặc 'Wait'
    """
    obstacles = set(boxes) | {opponent_pos}
    unplaced_boxes = [b for b in boxes if b not in goals]
    unoccupied_goals = [g for g in goals if g not in boxes]

    candidate_boxes = unplaced_boxes if unplaced_boxes else list(boxes)
    candidate_goals = unoccupied_goals if unoccupied_goals else list(goals)

    if not candidate_boxes or not candidate_goals:
        return 'Wait'

    best_pair = None
    min_dist = float('inf')

    for b in candidate_boxes:
        for g in candidate_goals:
            d = get_manhattan(my_pos, b) + get_manhattan(b, g)
            if d < min_dist:
                min_dist = d
                best_pair = (b, g)

    target_box, target_goal = best_pair

    best_push_action = None
    min_box_goal_dist = float('inf')
    push_stand_pos = None

    for act, (dx, dy) in DIRECTIONS.items():
        box_next = (target_box[0] + dx, target_box[1] + dy)
        stand_pos = (target_box[0] - dx, target_box[1] - dy)

        if not wall(grid, stand_pos[0], stand_pos[1]) and stand_pos != opponent_pos:
            if not wall(grid, box_next[0], box_next[1]) and box_next not in boxes and box_next != opponent_pos:
                dist = get_manhattan(box_next, target_goal)
                if dist < min_box_goal_dist:
                    min_box_goal_dist = dist
                    best_push_action = act
                    push_stand_pos = stand_pos

    if my_pos == push_stand_pos and best_push_action:
        return best_push_action

    target_pos = push_stand_pos if push_stand_pos else target_box
    clean_obs = obstacles - {target_pos}
    path = find_path_astar(grid, my_pos, target_pos, clean_obs, max_time=0.6)

    if path:
        return path[0]

    for act, (dx, dy) in DIRECTIONS.items():
        nxt = (my_pos[0] + dx, my_pos[1] + dy)
        if not wall(grid, nxt[0], nxt[1]) and nxt not in obstacles:
            return act

    return 'Wait'