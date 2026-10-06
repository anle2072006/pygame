import time
import heapq
from SokobanBoard import SokobanBoard
from PathFinder import PathFinder

class ExperimentRunner:
    def __init__(self, map_file):
        self.board = SokobanBoard(map_file)
        self.solver = PathFinder(self.board)
        self.initial_state = (self.board.initial_agent, self.board.initial_boxes)

    def run_experiment(self, algorithm='A*'):
        counter = 0
        frontier = []
        
        start_h = self.solver.heuristic(self.initial_state[1])
        # Hàng đợi: (f_cost, ID, g_cost, current_state, path)
        if algorithm == 'A*':
            heapq.heappush(frontier, (start_h, counter, 0, self.initial_state, []))
        else: # UCS
            heapq.heappush(frontier, (0, counter, 0, self.initial_state, []))
            
        explored = set()
        is_consistent = True
        
        start_time = time.time()
        
        while frontier:
            f_cost, _, g_cost, current_state, path = heapq.heappop(frontier)
            agent_posit, box_posit = current_state 
            
            # Đạt trạng thái đích
            if self.board.is_goal(box_posit):
                end_time = time.time()
                execution_time = (end_time - start_time) * 1000 # Đổi ra ms
                space_complexity = len(explored) # Số node đã lưu trong bộ nhớ
                return path, execution_time, space_complexity, is_consistent
                
            if current_state in explored:
                continue
                
            explored.add(current_state)
            current_h = self.solver.heuristic(box_posit)
            
            for action in self.solver.directions:
                next_state = self.board.get_next_state(current_state, action)
                
                if next_state is not None and next_state not in explored:
                    counter += 1
                    new_g_cost = g_cost + 1
                    new_path = path + [action]
                    
                    next_h = self.solver.heuristic(next_state[1])
                    
                    # Kiểm tra tính nhất quán (Consistency): h(n) <= c(n, a, n') + h(n')
                    if current_h > 1 + next_h:
                        is_consistent = False
                    
                    if algorithm == 'A*':
                        new_f_cost = new_g_cost + next_h
                    else:
                        new_f_cost = new_g_cost
                        
                    heapq.heappush(frontier, (new_f_cost, counter, new_g_cost, next_state, new_path))
                    
        return None, 0, len(explored), is_consistent

    def generate_report(self):
        print("="*40)
        print("THỰC NGHIỆM YÊU CẦU 3 & 4 (SOKOBAN - OOP)")
        print("="*40)
        
        # 1. Chạy Uniform Cost Search (UCS)
        print("Đang chạy thuật toán UCS...")
        ucs_path, ucs_time, ucs_space, _ = self.run_experiment(algorithm='UCS')
        
        # 2. Chạy A* Search
        print("Đang chạy thuật toán A*...")
        astar_path, astar_time, astar_space, astar_consistent = self.run_experiment(algorithm='A*')
        
        # --- BÁO CÁO YÊU CẦU 3 ---
        print("\n[YÊU CẦU 3] - BẢNG SO SÁNH ĐỘ PHỨC TẠP")
        print(f"{'Thuật toán':<15} | {'Thời gian (ms)':<15} | {'Không gian (Nodes)':<15}")
        print("-" * 55)
        print(f"{'UCS':<15} | {ucs_time:<15.2f} | {ucs_space:<15}")
        print(f"{'A* Search':<15} | {astar_time:<15.2f} | {astar_space:<15}")
        
        # --- BÁO CÁO YÊU CẦU 4 ---
        print("\n[YÊU CẦU 4] - ĐÁNH GIÁ TÍNH CHẤT HEURISTIC (Chebyshev)")
        start_heuristic_val = self.solver.heuristic(self.initial_state[1])
        
        if astar_path is not None:
            actual_optimal_cost = len(astar_path)
            is_admissible = start_heuristic_val <= actual_optimal_cost
            print(f"- Chi phí thực tế tối ưu h*(start): {actual_optimal_cost}")
            print(f"-> Tính chấp nhận được (Admissibility) [h(n) <= h*(n)]: {'THỎA MÃN' if is_admissible else 'KHÔNG THỎA MÃN'}")
        else:
            print("- Chi phí thực tế tối ưu h*(start): Vô cực (Không tìm thấy đường đi)")
            print("-> Tính chấp nhận được (Admissibility) [h(n) <= h*(n)]: BỎ QUA (Bản đồ không có lời giải)")
        print(f"-> Tính nhất quán (Consistency) [h(n) <= c + h(n')]: {'THỎA MÃN' if astar_consistent else 'KHÔNG THỎA MÃN'}")

if __name__ == "__main__":
    # Đảm bảo file example_map.txt nằm cùng thư mục
    experiment = ExperimentRunner("example_map.txt")
    experiment.generate_report()