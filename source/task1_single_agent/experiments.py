import time
import heapq
from board import read_map, find_agentandboxes, find_goal, find_next_state
from algorithms import heuristic

def search_experiment(grid, initial_state, goal_posit, algorithm='A*'):
    counter = 0
    frontier = []
    
    start_h = heuristic(initial_state[1], goal_posit)
    # Hàng đợi: (f_cost, ID, g_cost, current_state, path)
    if algorithm == 'A*':
        heapq.heappush(frontier, (start_h, counter, 0, initial_state, []))
    else: # UCS
        heapq.heappush(frontier, (0, counter, 0, initial_state, []))
        
    explored = set()
    directions = ['North', 'South', 'East', 'West']
    
    # Biến kiểm tra tính chất Heuristic (Yêu cầu 4)
    is_consistent = True
    
    start_time = time.time()
    
    while frontier:
        f_cost, _, g_cost, current_state, path = heapq.heappop(frontier)
        agent_posit, box_posit = current_state 
        
        if box_posit == goal_posit:
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000 # Đổi ra ms
            space_complexity = len(explored) # Số node đã lưu trong bộ nhớ
            return path, execution_time, space_complexity, is_consistent
            
        if current_state in explored:
            continue
            
        explored.add(current_state)
        current_h = heuristic(box_posit, goal_posit)
        
        for action in directions:
            next_state = find_next_state(grid, current_state, action)
            
            if next_state is not None and next_state not in explored:
                counter += 1
                new_g_cost = g_cost + 1
                new_path = path + [action]
                
                next_h = heuristic(next_state[1], goal_posit)
                
                # Kiểm tra tính nhất quán (Consistency): h(n) <= c(n, a, n') + h(n')
                # Trong bài toán này c(n, a, n') = 1
                if current_h > 1 + next_h:
                    is_consistent = False
                
                if algorithm == 'A*':
                    new_f_cost = new_g_cost + next_h
                else:
                    new_f_cost = new_g_cost
                    
                heapq.heappush(frontier, (new_f_cost, counter, new_g_cost, next_state, new_path))
                
    return None, 0, len(explored), is_consistent

if __name__ == "__main__":
    grid = read_map("example_map.txt")
    initial_state = (find_agentandboxes(grid)[0], find_agentandboxes(grid)[1])
    goal_posit = find_goal(grid)
    
    print("="*40)
    print("THỰC NGHIỆM YÊU CẦU 3 & 4 (SOKOBAN)")
    print("="*40)
    
    # 1. Chạy Uniform Cost Search (UCS)
    print("Đang chạy thuật toán UCS...")
    ucs_path, ucs_time, ucs_space, _ = search_experiment(grid, initial_state, goal_posit, algorithm='UCS')
    
    # 2. Chạy A* Search
    print("Đang chạy thuật toán A*...")
    astar_path, astar_time, astar_space, astar_consistent = search_experiment(grid, initial_state, goal_posit, algorithm='A*')
    
    # --- BÁO CÁO YÊU CẦU 3: SO SÁNH ĐỘ PHỨC TẠP ---
    print("\n[YÊU CẦU 3] - BẢNG SO SÁNH ĐỘ PHỨC TẠP")
    print(f"{'Thuật toán':<15} | {'Thời gian (ms)':<15} | {'Không gian (Nodes)':<15}")
    print("-" * 55)
    print(f"{'UCS':<15} | {ucs_time:<15.2f} | {ucs_space:<15}")
    print(f"{'A* Search':<15} | {astar_time:<15.2f} | {astar_space:<15}")
    
    # --- BÁO CÁO YÊU CẦU 4: KIỂM TRA HEURISTIC ---
    print("\n[YÊU CẦU 4] - ĐÁNH GIÁ TÍNH CHẤT HEURISTIC (Chebyshev)")
    
    # Admissibility Check
    start_heuristic_val = heuristic(initial_state[1], goal_posit)
    actual_optimal_cost = len(astar_path)
    is_admissible = start_heuristic_val <= actual_optimal_cost
    
    print(f"- Heuristic tại điểm xuất phát h(start): {start_heuristic_val}")
    print(f"- Chi phí thực tế tối ưu h*(start): {actual_optimal_cost}")
    print(f"-> Tính chấp nhận được (Admissibility) [h(n) <= h*(n)]: {'THỎA MÃN' if is_admissible else 'KHÔNG THỎA MÃN'}")
    
    # Consistency Check
    print(f"-> Tính nhất quán (Consistency) [h(n) <= c + h(n')]: {'THỎA MÃN' if astar_consistent else 'KHÔNG THỎA MÃN'}")