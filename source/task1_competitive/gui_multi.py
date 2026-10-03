import pygame
from board_2 import read_map, wall, find_initial_state, get_next_state_simultaneous, calculate_scores

# Import get_next_action từ hai agent và đổi tên để tránh đè lên nhau
from agent1 import get_next_action as agent1_decide
from agent2 import get_next_action as agent2_decide

pygame.init()

grid = read_map("map_competitive.txt")
pos_a1, pos_a2, box_owners, goals = find_initial_state(grid)

# Tính kích thước cửa sổ DỰA THEO bản đồ thật
TILE_SIZE = 40
WIDTH = max(len(row) for row in grid) * TILE_SIZE
HEIGHT = len(grid) * TILE_SIZE

# Tạo cửa sổ SAU KHI đã biết WIDTH, HEIGHT đúng
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban - Competitive 2-Agent")
font = pygame.font.Font(None, 28)

# Số bước giới hạn n, do người dùng nhập
N_STEPS = int(input("Nhập số bước giới hạn n: "))

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

    if not is_paused and not game_over and step_count < N_STEPS:
        if current_time - last_move_time > move_delay:
            remaining = N_STEPS - step_count
            boxes_list = list(box_owners.keys())

            # Gọi quyết định từ 2 Agent
            action1 = agent1_decide(grid, pos_a1, pos_a2, boxes_list, goals, remaining)
            action2 = agent2_decide(grid, pos_a2, pos_a1, boxes_list, goals, remaining)

            # Cập nhật trạng thái mới cho cả 2 agent đồng thời
            pos_a1, pos_a2, box_owners = get_next_state_simultaneous(
                grid, pos_a1, pos_a2, box_owners, goals, action1, action2
            )

            step_count += 1
            last_move_time = current_time

            if step_count >= N_STEPS:
                game_over = True

    screen.fill((200, 200, 200))

    # 1. Vẽ tường
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if wall(grid, x, y):
                pygame.draw.rect(screen, (80, 80, 80), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # 2. Vẽ điểm đích
    for (gx, gy) in goals:
        pygame.draw.circle(screen, (255, 0, 0), (gx * TILE_SIZE + TILE_SIZE // 2, gy * TILE_SIZE + TILE_SIZE // 2), 5)

    # 3. Vẽ thùng với màu sắc theo chủ sở hữu (owner)
    for (bx, by), owner in box_owners.items():
        if owner == 1:
            color = (0, 150, 0)   
        elif owner == 2:
            color = (150, 0, 150)    
        else:
            color = (150, 90, 40)    

        pygame.draw.rect(screen, color, (bx * TILE_SIZE, by * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Agent 1
    cx1 = pos_a1[0] * TILE_SIZE + TILE_SIZE // 2
    cy1 = pos_a1[1] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, (0, 100, 255), (cx1, cy1), TILE_SIZE // 2 - 5)

    #Agent2
    cx2 = pos_a2[0] * TILE_SIZE + TILE_SIZE // 2
    cy2 = pos_a2[1] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, (255, 150, 0), (cx2, cy2), TILE_SIZE // 2 - 5)

    score1, score2 = calculate_scores(box_owners, goals)

    step_text = font.render(f"Step: {step_count}/{N_STEPS}", True, (0, 0, 0))
    score_text = font.render(f"Agent1: {score1} - Agent2: {score2}", True, (0, 0, 0))

    screen.blit(step_text, (10, 10))
    screen.blit(score_text, (10, 35))

    # Hiển thị kết quả kết thúc trận đấu
    if game_over:
        if score1 > score2:
            result_str = "AGENT 1 WINS!"
            res_color = (0, 100, 255)
        elif score2 > score1:
            result_str = "AGENT 2 WINS!"
            res_color = (255, 150, 0)
        else:
            result_str = "DRAW GAME!"
            res_color = (100, 100, 100)

        result_text = font.render(result_str, True, res_color)
        screen.blit(result_text, (10, 60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()