import pygame
from board_2 import read_map, wall, find_initial_state, get_next_state_simultaneous, calculate_scores
from AStarAgent import AStarAgent
from BFSAgent import BFSAgent

class MultiGameEngine:
    def __init__(self, map_file, n_steps):
        pygame.init()
        self.grid = read_map(map_file)
        self.pos_a1, self.pos_a2, self.box_owners, self.goals = find_initial_state(self.grid)
        
        self.agent1 = AStarAgent(agent_id=1)
        self.agent2 = BFSAgent(agent_id=2)
        
        # Tính kích thước cửa sổ DỰA THEO bản đồ thật
        self.TILE_SIZE = 40
        self.WIDTH = max(len(row) for row in self.grid) * self.TILE_SIZE
        self.HEIGHT = len(self.grid) * self.TILE_SIZE
        
        # Tạo cửa sổ SAU KHI đã biết WIDTH, HEIGHT đúng
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sokoban - Competitive 2-Agent OOP")
        self.font = pygame.font.Font(None, 28)
        
        # Số bước giới hạn n, do người dùng nhập
        self.N_STEPS = n_steps

    def run(self):
        step_count = 0
        is_paused = True
        move_delay = 500  # 2 agent suy nghĩ nên để delay dài hơn đơn-agent
        last_move_time = 0

        running = True
        clock = pygame.time.Clock()
        game_over = False

        while running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: 
                        # Đảo trạng thái is_paused
                        is_paused = not is_paused

            if not is_paused and not game_over and step_count < self.N_STEPS:
                if current_time - last_move_time > move_delay:
                    remaining = self.N_STEPS - step_count
                    boxes_list = list(self.box_owners.keys())

                    # Gọi quyết định từ 2 Agent
                    action1 = self.agent1.get_next_action(self.grid, self.pos_a1, self.pos_a2, boxes_list, self.goals, remaining)
                    action2 = self.agent2.get_next_action(self.grid, self.pos_a2, self.pos_a1, boxes_list, self.goals, remaining)
                    
                    # Cập nhật trạng thái mới cho cả 2 agent đồng thời
                    self.pos_a1, self.pos_a2, self.box_owners = get_next_state_simultaneous(
                        self.grid, self.pos_a1, self.pos_a2, self.box_owners, self.goals, action1, action2
                    )

                    step_count += 1
                    last_move_time = current_time

                    if step_count >= self.N_STEPS:
                        game_over = True

            self._draw_frame(step_count, game_over)
            clock.tick(60)

        pygame.quit()

    def _draw_frame(self, step_count, game_over):
        self.screen.fill((200, 200, 200))
        
        # 1. Vẽ tường
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if wall(self.grid, x, y):
                    pygame.draw.rect(self.screen, (80, 80, 80), (x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
        
        # 2. Vẽ điểm đích
        for (gx, gy) in self.goals:
            pygame.draw.circle(self.screen, (255, 0, 0), (gx * self.TILE_SIZE + self.TILE_SIZE // 2, gy * self.TILE_SIZE + self.TILE_SIZE // 2), 5)
        
        # 3. Vẽ thùng với màu sắc theo chủ sở hữu (owner)
        for (bx, by), owner in self.box_owners.items():
            color = (0, 150, 0) if owner == 1 else (150, 0, 150) if owner == 2 else (150, 90, 40)
            pygame.draw.rect(self.screen, color, (bx * self.TILE_SIZE, by * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
        
        # Agent 1
        cx1 = self.pos_a1[0] * self.TILE_SIZE + self.TILE_SIZE // 2
        cy1 = self.pos_a1[1] * self.TILE_SIZE + self.TILE_SIZE // 2
        pygame.draw.circle(self.screen, (0, 100, 255), (cx1, cy1), self.TILE_SIZE // 2 - 5)
        
        #Agent2
        cx2 = self.pos_a2[0] * self.TILE_SIZE + self.TILE_SIZE // 2
        cy2 = self.pos_a2[1] * self.TILE_SIZE + self.TILE_SIZE // 2
        pygame.draw.circle(self.screen, (255, 150, 0), (cx2, cy2), self.TILE_SIZE // 2 - 5)

        score1, score2 = calculate_scores(self.box_owners, self.goals)
        
        step_text = self.font.render(f"Step: {step_count}/{self.N_STEPS}", True, (0, 0, 0))
        score_text = self.font.render(f"Agent1: {score1} - Agent2: {score2}", True, (0, 0, 0))
        
        self.screen.blit(step_text, (10, 10))
        self.screen.blit(score_text, (10, 35))
        
        # Hiển thị kết quả kết thúc trận đấu
        if game_over:
            result_str = "AGENT 1 WINS!" if score1 > score2 else "AGENT 2 WINS!" if score2 > score1 else "DRAW GAME!"
            res_color = (0, 100, 255) if score1 > score2 else (255, 150, 0) if score2 > score1 else (100, 100, 100)
            result_text = self.font.render(result_str, True, res_color)
            self.screen.blit(result_text, (10, 60))

        pygame.display.flip()

if __name__ == "__main__":
    try:
        steps = int(input("Nhập số bước giới hạn n: "))
    except ValueError:
        steps = 50
    game = MultiGameEngine("map_competitive.txt", steps)
    game.run()