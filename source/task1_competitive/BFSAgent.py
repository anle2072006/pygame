import time

class BFSAgent:
    def __init__(self, agent_id=2):
        self.agent_id = agent_id
        self.recent_actions = []
        self.last_pos = None
        self.stuck_count = 0
        self.DIRECTIONS = {'North': (0, -1), 'South': (0, 1), 'East': (1, 0), 'West': (-1, 0)}
        self.OPPOSITE = {'North': 'South', 'South': 'North', 'East': 'West', 'West': 'East'}

    def get_manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def wall(self, grid, x, y):
        if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[y]):
            return True
        return grid[y][x] == '%'

    def get_safe_neighbors(self, grid, pos, obstacles):
        neighbors = []
        for act, (dx, dy) in self.DIRECTIONS.items():
            nxt = (pos[0] + dx, pos[1] + dy)
            if not self.wall(grid, nxt[0], nxt[1]) and nxt not in obstacles:
                neighbors.append((act, nxt))
        return neighbors

    def find_path_bfs(self, grid, start, target, obstacles, max_time=0.7):
        if start == target:
            return []
        start_time = time.time()
        queue = [(start, [])]
        visited = {start}

        while queue:
            if time.time() - start_time > max_time:
                break
            current, path = queue.pop(0)
            if current == target:
                return path

            for act, nxt in self.get_safe_neighbors(grid, current, obstacles):
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, path + [act]))
        return None

    def get_next_action(self, grid, my_pos, opponent_pos, boxes, goals, remaining_steps):
        if my_pos == self.last_pos:
            self.stuck_count += 1
        else:
            self.stuck_count = 0
        self.last_pos = my_pos

        obstacles = set(boxes) | {opponent_pos}
        candidates = []
        for act, (dx, dy) in self.DIRECTIONS.items():
            nxt = (my_pos[0] + dx, my_pos[1] + dy)
            if not self.wall(grid, nxt[0], nxt[1]) and nxt not in obstacles:
                candidates.append((act, nxt))

        if self.stuck_count >= 2 or self.get_manhattan(my_pos, opponent_pos) == 1:
            valid_evades = [act for act, nxt in candidates if self.get_manhattan(nxt, opponent_pos) >= self.get_manhattan(my_pos, opponent_pos)]
            if valid_evades:
                action = valid_evades[-1]
                self.recent_actions.append(action)
                return action

        sorted_boxes = sorted(boxes, key=lambda b: self.get_manhattan(my_pos, b))
        if not sorted_boxes:
            return 'Wait'

        best_plan = None
        min_dist = float('inf')

        for b in sorted_boxes:
            sorted_goals = sorted(goals, key=lambda g: self.get_manhattan(b, g))
            g = sorted_goals[0] if sorted_goals else b

            for act, (dx, dy) in self.DIRECTIONS.items():
                box_next = (b[0] + dx, b[1] + dy)
                stand_pos = (b[0] - dx, b[1] - dy)

                if self.wall(grid, stand_pos[0], stand_pos[1]) or stand_pos in obstacles:
                    if stand_pos != my_pos:
                        continue
                if self.wall(grid, box_next[0], box_next[1]) or box_next in boxes or box_next == opponent_pos:
                    continue

                cost = self.get_manhattan(my_pos, stand_pos) + self.get_manhattan(box_next, g)
                if self.get_manhattan(stand_pos, opponent_pos) <= 1:
                    cost += 5

                if cost < min_dist:
                    path = self.find_path_bfs(grid, my_pos, stand_pos, obstacles, max_time=0.08)
                    if path is not None:
                        min_dist = cost
                        best_plan = (act, stand_pos, path)

            if best_plan:
                break

        action = 'Wait'
        if best_plan:
            act, stand_pos, path = best_plan
            if my_pos == stand_pos:
                action = act
            elif path:
                action = path[0]
        else:
            last_act = self.recent_actions[-1] if self.recent_actions else None
            forbidden = self.OPPOSITE.get(last_act)
            cand_acts = [a for a, _ in candidates]
            valid_candidates = [a for a in cand_acts if a != forbidden]
            action = valid_candidates[0] if valid_candidates else (cand_acts[0] if cand_acts else 'Wait')

        self.recent_actions.append(action)
        if len(self.recent_actions) > 10:
            self.recent_actions.pop(0)

        return action