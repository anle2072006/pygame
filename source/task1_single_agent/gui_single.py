import pygame
from board import read_map, wall, find_agentandboxes, find_next_state, find_goal
from algorithms import a_star_search, uniform_cost_search

pygame.init()

WIDTH = 500
HEIGHT = 500
TILE_SIZE = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban Game")

# Khởi tạo dữ liệu bản đồ
grid = read_map("example_map.txt")
agent_posit, box_posit = find_agentandboxes(grid)
goal_posit = find_goal(grid)

running  = True
clock = pygame.time.Clock()

# Các biến phục vụ cho AI tự động di chuyển
solution_path = [] 
step_index = 0
ai_running = False
last_move_time = 0
move_delay = 200 

while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                
        if event.type == pygame.KEYDOWN:#di chuyen
            if event.key == pygame.K_SPACE and not ai_running:
                print("Đang tìm đường bằng A*...")
                solution_path, cost = uniform_cost_search(grid, (agent_posit, box_posit), goal_posit)
            
                if solution_path:
                    print(f"Đã tìm thấy đường đi! Tổng chi phí: {cost} bước.")
                    ai_running = True
                    step_index = 0
                    last_move_time = current_time
                else:
                    print("Không tìm thấy đường đi.")
            
            # Logic di chuyển
            direction = None
            if event.key == pygame.K_UP:
                direction = 'North'
            elif event.key == pygame.K_DOWN:
                direction = 'South'
            elif event.key == pygame.K_LEFT:
                direction = 'West'
            elif event.key == pygame.K_RIGHT:
                direction = 'East'

            if direction is not None and not ai_running:
                result = find_next_state(grid, (agent_posit, box_posit), direction)
                if result is not None:
                    agent_posit, box_posit = result

    # Xử lý cho AI tự động đi từng bước theo danh sách hành động tìm được
    if ai_running and step_index < len(solution_path):
        if current_time - last_move_time > move_delay:
            action = solution_path[step_index]
            result = find_next_state(grid, (agent_posit, box_posit), action)
            if result is not None:
                agent_posit, box_posit = result
            step_index += 1
            last_move_time = current_time
    elif ai_running and step_index >= len(solution_path):
        # Dừng AI khi đã đi hết đường
        ai_running = False
        
    # Vẽ nền
    screen.fill((200, 200, 200))

    for y in range(len(grid)):# vẽ tường
        for x in range(len(grid[y])):
            if wall(grid, x, y):
                pygame.draw.rect(screen,(80, 80, 80), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Vẽ điểm mục tiêu
    for (gx, gy) in goal_posit:
        pygame.draw.circle(screen, (255, 0, 0), (gx * TILE_SIZE + TILE_SIZE // 2, gy * TILE_SIZE + TILE_SIZE // 2), 5)
        
    # Vẽ thùng
    for (bx, by) in box_posit:
        if (bx, by) in goal_posit:
            # Thùng nằm trên mục tiêu sẽ có màu nâu sậm
            pygame.draw.rect(screen, (101, 67, 33), (bx * TILE_SIZE, by * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        else:
            # Thùng bình thường
            pygame.draw.rect(screen, (150, 90, 40), (bx * TILE_SIZE, by * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
    # Vẽ nhân vật
    if agent_posit is not None:
        center_x = agent_posit[0] * TILE_SIZE + TILE_SIZE // 2 
        center_y = agent_posit[1] * TILE_SIZE + TILE_SIZE // 2
        radius = TILE_SIZE // 2 - 5
        
        pygame.draw.circle(screen, (0, 100, 255), (center_x, center_y), radius)

    pygame.display.flip()
    clock.tick(60) #giới hạn fps

pygame.quit()