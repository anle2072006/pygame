import heapq
import time
from board_2 import wall

DIRECTIONS = {
    'North': (0, -1),
    'South': (0, 1),
    'East': (1, 0),
    'West': (-1, 0)
}

OPPOSITE = {
    'North': 'South',
    'South': 'North',
    'East': 'West',
    'West': 'East'
}

recent_actions = []
last_pos = None
stuck_count = 0

def get_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_neighbors(grid, pos, obstacles):
    neighbors = []
    for act, (dx, dy) in DIRECTIONS.items():
        nxt = (pos[0] + dx, pos[1] + dy)
        if not wall(grid, nxt[0], nxt[1]) and nxt not in obstacles:
            neighbors.append((act, nxt))
    return neighbors

def find_path_astar(grid, start, target, obstacles, max_time=0.7):
    if start == target:
        return []
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
    return None

def get_next_action(grid, my_pos, opponent_pos, boxes, goals, remaining_steps):
    global recent_actions, last_pos, stuck_count

    if my_pos == last_pos:
        stuck_count += 1
    else:
        stuck_count = 0
    last_pos = my_pos

    obstacles = set(boxes) | {opponent_pos}

    candidates = []
    for act, (dx, dy) in DIRECTIONS.items():
        nxt = (my_pos[0] + dx, my_pos[1] + dy)
        if not wall(grid, nxt[0], nxt[1]) and nxt not in obstacles:
            candidates.append((act, nxt))

    if stuck_count >= 2 or get_manhattan(my_pos, opponent_pos) == 1:
        valid_evades = [
            act for act, nxt in candidates 
            if get_manhattan(nxt, opponent_pos) >= get_manhattan(my_pos, opponent_pos)
        ]
        if valid_evades:
            action = valid_evades[0]
            recent_actions.append(action)
            return action

    unplaced_boxes = [b for b in boxes if b not in goals]
    unoccupied_goals = [g for g in goals if g not in boxes]

    target_boxes = unplaced_boxes if unplaced_boxes else list(boxes)
    target_goals = unoccupied_goals if unoccupied_goals else list(goals)

    if not target_boxes or not target_goals:
        return 'Wait'

    best_plan = None
    min_total_cost = float('inf')

    for b in target_boxes:
        for g in target_goals:
            for act, (dx, dy) in DIRECTIONS.items():
                box_next = (b[0] + dx, b[1] + dy)
                stand_pos = (b[0] - dx, b[1] - dy)

                if wall(grid, stand_pos[0], stand_pos[1]) or stand_pos in obstacles:
                    if stand_pos != my_pos:
                        continue
                if wall(grid, box_next[0], box_next[1]) or box_next in boxes or box_next == opponent_pos:
                    continue

                cost = get_manhattan(my_pos, stand_pos) + get_manhattan(box_next, g) * 2
                if get_manhattan(stand_pos, opponent_pos) <= 1:
                    cost += 5

                if cost < min_total_cost:
                    path = find_path_astar(grid, my_pos, stand_pos, obstacles, max_time=0.08)
                    if path is not None:
                        min_total_cost = cost
                        best_plan = (act, stand_pos, path)

    action = 'Wait'

    if best_plan:
        act, stand_pos, path = best_plan
        if my_pos == stand_pos:
            action = act
        elif path:
            action = path[0]
    else:
        last_act = recent_actions[-1] if recent_actions else None
        forbidden = OPPOSITE.get(last_act)
        cand_acts = [a for a, _ in candidates]
        valid_candidates = [a for a in cand_acts if a != forbidden]
        action = valid_candidates[0] if valid_candidates else (cand_acts[0] if cand_acts else 'Wait')

    recent_actions.append(action)
    if len(recent_actions) > 10:
        recent_actions.pop(0)

    return action