class SokobanBoard:
    def __init__(self, filepath):
        self.grid = self._read_map(filepath)
        self.initial_agent, self.initial_boxes = self._find_agent_and_boxes()
        self.goals = self._find_goal()

    def _read_map(self, filepath):
        grid = []
        with open(filepath, 'r') as f: #with giúp tự động đóng file sau khi đọc xong tránh lãng phí tài nguyên
            for line in f:
                row = line.rstrip('\r\n') #chỉ bỏ ký tư xuống dòng k bỏ các khoảng trắng tránh bị hư hỏng ma trận
                grid.append(row)
        return grid

    def _find_agent_and_boxes(self):
        agent_posit = None
        box_posit = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                char = self.grid[y][x]
                if char == 'A':
                    agent_posit = (x, y)
                elif char in ('B', 'C'):
                    box_posit.append((x, y))
        return agent_posit, frozenset(box_posit)

    def _find_goal(self):
        goal_posit = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                char = self.grid[y][x]
                if char in ('D', 'C'):
                    goal_posit.append((x, y))
        return frozenset(goal_posit)

    def is_wall(self, x, y):
        if y < 0 or y >= len(self.grid) or x < 0 or x >= len(self.grid[y]):
            return True
        return self.grid[y][x] == '%'

    def get_next_state(self, state, direction):
        agent_posit, box_posit = state
        deltas = {'North': (0, -1), 'South': (0, 1), 'East': (1, 0), 'West': (-1, 0)}
        dx, dy = deltas[direction]
        next_cell = (agent_posit[0] + dx, agent_posit[1] + dy)

        if self.is_wall(next_cell[0], next_cell[1]):
            return None

        if next_cell not in box_posit:
            return (next_cell, box_posit)
        else:
            far_cell = (next_cell[0] + dx, next_cell[1] + dy)

            if self.is_wall(far_cell[0], far_cell[1]):
                return None
            if far_cell in box_posit:
                return None

            new_box_posit = set(box_posit)
            new_box_posit.remove(next_cell)
            new_box_posit.add(far_cell)

            return (next_cell, frozenset(new_box_posit))

    def is_goal(self, box_posit):
        return box_posit == self.goals