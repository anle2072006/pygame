import heapq

class PathFinder:
    def __init__(self, board):
        self.board = board
        self.directions = ['North', 'South', 'East', 'West']
    
    # heuristic
    def chebyshev_distance(self, point1, point2):
        return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

    def heuristic(self, box_posit):
        total_distance = 0
        
        # Tính tổng khoảng cách từ mỗi thùng đến mục tiêu gần nhất của nó
        for b in box_posit:
            # Tìm mục tiêu gần nhất bằng Chebyshev
            min_dist = min([self.chebyshev_distance(b, g) for g in self.board.goals])
            total_distance += min_dist
        return total_distance
    
    # UCS
    def uniform_cost_search(self):
        initial_state = (self.board.initial_agent, self.board.initial_boxes)
        counter = 0
        frontier = []
        
        heapq.heappush(frontier, (0, counter, initial_state, []))
        explored = set()
        
        while frontier:
            cost, _, current_state, path = heapq.heappop(frontier)
            agent_posit, box_posit = current_state
            
            if self.board.is_goal(box_posit):
                return path, cost
                
            if current_state in explored:
                continue
                
            explored.add(current_state)
            
            for action in self.directions:
                next_state = self.board.get_next_state(current_state, action)
                if next_state is not None and next_state not in explored:
                    counter += 1
                    new_cost = cost + 1
                    new_path = path + [action]
                    heapq.heappush(frontier, (new_cost, counter, next_state, new_path))
                        
        return None, 0
    
    # A*
    def a_star_search(self):
        initial_state = (self.board.initial_agent, self.board.initial_boxes)
        counter = 0
        frontier = []    

        start_h = self.heuristic(initial_state[1])
        
        # Hàng đợi lưu: (f_cost, ID, g_cost, current_state, path)
        heapq.heappush(frontier, (start_h, counter, 0, initial_state, []))
        
        explored = set()
        
        while frontier:
            f_cost, _, g_cost, current_state, path = heapq.heappop(frontier)
            agent_posit, box_posit = current_state
            
            if self.board.is_goal(box_posit):
                return path, g_cost
                
            if current_state in explored:
                continue
                
            explored.add(current_state)
            
            for action in self.directions:
                next_state = self.board.get_next_state(current_state, action)
                if next_state is not None and next_state not in explored:
                    counter += 1
                    new_g_cost = g_cost + 1
                    new_path = path + [action]
                    h_cost = self.heuristic(next_state[1])
                    new_f_cost = new_g_cost + h_cost
                    heapq.heappush(frontier, (new_f_cost, counter, new_g_cost, next_state, new_path))
                    
        return None, 0