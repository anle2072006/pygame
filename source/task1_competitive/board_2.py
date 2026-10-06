def read_map(filepath):
    grid = []
    with open(filepath, 'r') as f:
        for line in f:
            row = line.rstrip('\r\n')
            grid.append(row)
    return grid

def wall(grid, x, y):
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[y]):
        return True
    return grid[y][x] == '%'

def find_initial_state(grid):
    """
    Quy ước ký tự trên Map:
    - '1' hoặc 'A': Agent 1
    - '2' hoặc 'E': Agent 2
    - 'B': Thùng thường chưa thuộc về ai
    - 'D': Vị trí đích (Goal)
    - 'C': Thùng ban đầu nằm trên đích
    - '%': Tường / Vật cản
    """
    pos_a1 = None
    pos_a2 = None
    boxes = []
    goals = []

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            char = grid[y][x]
            if char in ('1', 'A'):
                pos_a1 = (x, y)
            elif char in ('2', 'E'):
                pos_a2 = (x, y)
            elif char == 'B':
                boxes.append((x, y))
            elif char == 'D':
                goals.append((x, y))
            elif char == 'C':
                boxes.append((x, y))
                goals.append((x, y))

    box_owners = {}
    for b in boxes:
        box_owners[b] = None

    return pos_a1, pos_a2, box_owners, frozenset(goals)

def get_next_state_simultaneous(grid, pos_a1, pos_a2, box_owners, goals, action1, action2):
    """
    Xử lý hành động đồng thời của 2 agent tại mỗi bước (Yêu cầu 6).
    action có thể là: 'North', 'South', 'East', 'West', 'Wait'
    """
    deltas = {
        'North': (0, -1),
        'South': (0, 1),
        'East': (1, 0),
        'West': (-1, 0),
        'Wait': (0, 0)
    }

    dx1, dy1 = deltas.get(action1, (0, 0))
    dx2, dy2 = deltas.get(action2, (0, 0))

    next_a1 = (pos_a1[0] + dx1, pos_a1[1] + dy1)
    next_a2 = (pos_a2[0] + dx2, pos_a2[1] + dy2)

    boxes = set(box_owners.keys())

    if next_a1 == pos_a2 and next_a2 == pos_a1:
        return pos_a1, pos_a2, box_owners

    if next_a1 == next_a2 and next_a1 not in boxes:
        return pos_a1, pos_a2, box_owners

    def evaluate_move(agent_pos, next_pos, dx, dy, other_agent_pos):
        if (dx, dy) == (0, 0):
            return agent_pos, None  

        if wall(grid, next_pos[0], next_pos[1]):
            return agent_pos, None 

        if next_pos == other_agent_pos:
            return agent_pos, None  

        if next_pos not in boxes:
            return next_pos, None   

        far_box_cell = (next_pos[0] + dx, next_pos[1] + dy)
        if wall(grid, far_box_cell[0], far_box_cell[1]):
            return agent_pos, None 
        if far_box_cell in boxes:
            return agent_pos, None  
        if far_box_cell == other_agent_pos:
            return agent_pos, None  

        return next_pos, (next_pos, far_box_cell)

    res_a1, push_1 = evaluate_move(pos_a1, next_a1, dx1, dy1, pos_a2)
    res_a2, push_2 = evaluate_move(pos_a2, next_a2, dx2, dy2, pos_a1)

    if push_1 and push_2 and push_1[0] == push_2[0]:
        res_a1, push_1 = pos_a1, None
        res_a2, push_2 = pos_a2, None

    if push_1 and push_2 and push_1[1] == push_2[1]:
        res_a1, push_1 = pos_a1, None
        res_a2, push_2 = pos_a2, None

    if push_1 and push_1[1] == res_a2:
        res_a1, push_1 = pos_a1, None
    if push_2 and push_2[1] == res_a1:
        res_a2, push_2 = pos_a2, None

    new_box_owners = dict(box_owners)

    if push_1:
        old_b, new_b = push_1
        prev_owner = new_box_owners.pop(old_b)
        if new_b in goals:
            new_box_owners[new_b] = 1
        else:
            new_box_owners[new_b] = None

    if push_2:
        old_b, new_b = push_2
        prev_owner = new_box_owners.pop(old_b)
        if new_b in goals:
            new_box_owners[new_b] = 2
        else:
            new_box_owners[new_b] = None

    return res_a1, res_a2, new_box_owners

def calculate_scores(box_owners, goals):
    """Tính điểm hiện tại của Agent 1 và Agent 2 dựa trên số thùng ở đích"""
    score1 = 0
    score2 = 0
    for box, owner in box_owners.items():
        if box in goals:
            if owner == 1:
                score1 += 1
            elif owner == 2:
                score2 += 1
    return score1, score2


if __name__ == "__main__":
    grid = read_map("example_map.txt")
    p1, p2, box_owners, goals = find_initial_state(grid)

    print("--- Khởi tạo Game 2-Agent ---")
    print("Agent 1:", p1)
    print("Agent 2:", p2)
    print("Boxes:", list(box_owners.keys()))
    print("Goals:", goals)