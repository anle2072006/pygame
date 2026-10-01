import heapq
from board import find_next_state, goal, find_goal

def uniform_cost_search(grid, initial_state, goal_posit):
    # Hàng đợi ưu tiên (Priority Queue) lưu trữ: (chi_phí, ID, trạng_thái, đường_đi)
    # Dùng thêm một biến counter (ID) để tránh lỗi so sánh tuple khi chi phí bằng nhau
    counter = 0
    frontier = []
    heapq.heappush(frontier, (0, counter, initial_state, []))
    
    # Tập hợp các trạng thái đã duyệt để tránh lặp (Visited set)
    # Trạng thái được biểu diễn bằng (agent_posit, box_posit)
    explored = set()
    
    directions = ['North', 'South', 'East', 'West']
    
    while frontier:
        cost, _, current_state, path = heapq.heappop(frontier)
        
        agent_posit, box_posit = current_state
        
        # Kiểm tra nếu đạt trạng thái đích
        if goal(box_posit, goal_posit):
            return path, cost
            
        if current_state in explored:
            continue
            
        explored.add(current_state)
        
        # Duyệt qua các hướng di chuyển có thể
        for action in directions:
            # Gọi hàm để sinh trạng thái tiếp theo
            next_state = find_next_state(grid, current_state, action)
            
            if next_state is not None:
                if next_state not in explored:
                    counter += 1
                    # Mỗi bước di chuyển tốn chi phí là 1
                    new_cost = cost + 1
                    new_path = path + [action]
                    heapq.heappush(frontier, (new_cost, counter, next_state, new_path))
                    
    return None, 0 # Trả về None nếu không tìm thấy đường đi

# Heuristic
def chebyshev_distance(point1, point2):
    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

def heuristic(box_posit, goal_posit):
    total_distance = 0
    # Tính tổng khoảng cách từ mỗi thùng đến mục tiêu gần nhất của nó
    for b in box_posit:
        # Tìm mục tiêu gần nhất bằng Chebyshev
        min_dist = min([chebyshev_distance(b, g) for g in goal_posit])
        total_distance += min_dist
    return total_distance

# A*
def a_star_search(grid, initial_state, goal_posit):
    counter = 0
    frontier = []
    
    # Tính h ban đầu
    start_h = heuristic(initial_state[1], goal_posit)
    
    # Hàng đợi lưu: (f_cost, ID, g_cost, current_state, path)
    heapq.heappush(frontier, (start_h, counter, 0, initial_state, []))
    
    explored = set()
    directions = ['North', 'South', 'East', 'West']
    
    while frontier:
        f_cost, _, g_cost, current_state, path = heapq.heappop(frontier)
        agent_posit, box_posit = current_state
        
        if goal(box_posit, goal_posit):
            return path, g_cost
            
        if current_state in explored:
            continue
            
        explored.add(current_state)
        
        for action in directions:
            next_state = find_next_state(grid, current_state, action)
            
            if next_state is not None and next_state not in explored:
                counter += 1
                new_g_cost = g_cost + 1
                new_path = path + [action]
                
                # Tính Heuristic cho trạng thái mới
                h_cost = heuristic(next_state[1], goal_posit)
                new_f_cost = new_g_cost + h_cost
                
                heapq.heappush(frontier, (new_f_cost, counter, new_g_cost, next_state, new_path))
                
    return None, 0