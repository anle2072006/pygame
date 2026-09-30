def read_map(filepath):
    grid =[]
    with open(filepath, 'r') as f:#with giúp tự động đóng file sau khi đọc xong tránh lãng phí tài nguyên
        for line in f:
            row = line.rstrip('\r\n') #chỉ bỏ ký tư xuống dòng k bỏ các khoảng trắng tránh bị hư hỏng ma trận
            grid.append(row)
    return grid

def find_agentandboxes(grid):
    agent_posit = None
    box_posit = []
    for y in range (len(grid)):
        for x in range(len(grid[y])):
            char= grid[y][x]
            if char=='A':
                agent_posit = (x, y)
            elif char in ('B','C'):
                box_posit.append((x,y))
    return agent_posit, frozenset(box_posit)

def find_goal(grid):
    goal_posit = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            char = grid[y][x]
            if char in ('D', 'C'):
                goal_posit.append((x,y))
    return frozenset(goal_posit)

def wall(grid, x, y):
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[y]):
        return True
    return grid[y][x] == '%'

def find_next_state(grid, state, direction):
    agent_posit, box_posit = state
    deltas = {'North':(0,1), 'South': (0,-1), 'East':(1,0), 'West':(-1, 0)}
    dx, dy = deltas[direction]
    next_cell = (agent_posit[0] + dx, agent_posit[1] + dy)

    if wall(grid, next_cell[0],next_cell[1]):
        return None

    if next_cell not in box_posit:
        return (next_cell, box_posit)
    else:
        far_cell =(next_cell[0] + dx, next_cell[1]+ dy)

        if wall(grid, far_cell[0], far_cell[1]):
            return None
        if far_cell in box_posit:
            return None

        new_box_posit = set(box_posit)
        new_box_posit.remove(next_cell)
        new_box_posit.add(far_cell)

        return (next_cell, frozenset(new_box_posit))

def goal(box_posit, goal_posit):
    return box_posit == goal_posit

if __name__ == "__main__":
    grid = read_map("example_map.txt")
    agent_posit, box_posit = find_agentandboxes(grid)
    goal_posit = find_goal(grid)

    print("Agent:", agent_posit)
    print("Boxes:", box_posit)
    print("Goals:", goal_posit)
    
    initial_state = (agent_posit, box_posit)
    
    print("\n--- Test chuyển trạng thái ---")
    state_east = find_next_state(grid, initial_state, 'East')
    print("Đi sang East:", state_east)
    
    state_north = find_next_state(grid, initial_state, 'North')
    print("Đi sang North:", state_north)
