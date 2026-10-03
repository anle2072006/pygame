import pygame
from board import read_map, wall, find_agentandboxes, find_next_state, find_goal
from algorithms import a_star_search, uniform_cost_search

pygame.init()

WIDTH = 500
HEIGHT = 500
TILE_SIZE = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban Game")

grid = read_map("example_map.txt")
agent_posit, box_posit = find_agentandboxes(grid)
goal_posit = find_goal(grid)
initial_state = (agent_posit, box_posit)

font = pygame.font.Font(None, 30)

# chọn thuật toán
choosing = True
chosen_algorithm = None

while choosing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                chosen_algorithm = 'UCS'
                choosing = False
            elif event.key == pygame.K_a:
                chosen_algorithm = 'ASTAR'
                choosing = False

    screen.fill((200, 200, 200))
    text1 = font.render("Press U for UCS", True, (0, 0, 0))
    text2 = font.render("Press A for A*", True, (0, 0, 0))
    screen.blit(text1, (50, 200))
    screen.blit(text2, (50, 240))
    pygame.display.flip()

# gọi thuật toán đã chọn
if chosen_algorithm == 'UCS':
    solution_path, cost = uniform_cost_search(grid, initial_state, goal_posit)
else:
    solution_path, cost = a_star_search(grid, initial_state, goal_posit)

# tính state
states = [initial_state]
current = initial_state
for action in solution_path:
    current = find_next_state(grid, current, action)
    states.append(current)

#biến điều khiển
current_index = 0
is_paused = True
move_delay = 200
last_move_time = 0

running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Bật/tắt trạng thái tự động phát
                is_paused = not is_paused
            elif event.key == pygame.K_RIGHT:
                # Tua tới bước tiếp theo
                if current_index < len(states) - 1:
                    current_index += 1
            elif event.key == pygame.K_LEFT:
                # Tua lùi về bước trước
                if current_index > 0:
                    current_index -= 1

    # Autoplay: nếu KHÔNG pause, tự tăng current_index theo thời gian 
    if not is_paused and current_index < len(states) - 1:
        if current_time - last_move_time > move_delay:
            current_index += 1
            last_move_time = current_time

    # Lấy state hiện tại để vẽ
    agent_posit, box_posit = states[current_index]

    screen.fill((200, 200, 200))

    # Vẽ tường
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if wall(grid, x, y):
                pygame.draw.rect(screen, (80, 80, 80), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Vẽ điểm đích
    for (gx, gy) in goal_posit:
        pygame.draw.circle(screen, (255, 0, 0), (gx * TILE_SIZE + TILE_SIZE // 2, gy * TILE_SIZE + TILE_SIZE // 2), 5)

    # Vẽ thùng (Thùng đã ở vị trí đích sẽ có màu nâu đậm)
    for (bx, by) in box_posit:
        if (bx, by) in goal_posit:
            pygame.draw.rect(screen, (101, 67, 33), (bx * TILE_SIZE, by * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        else:
            pygame.draw.rect(screen, (150, 90, 40), (bx * TILE_SIZE, by * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Vẽ Agent
    if agent_posit is not None:
        center_x = agent_posit[0] * TILE_SIZE + TILE_SIZE // 2
        center_y = agent_posit[1] * TILE_SIZE + TILE_SIZE // 2
        radius = TILE_SIZE // 2 - 5
        pygame.draw.circle(screen, (0, 100, 255), (center_x, center_y), radius)

    # Hiển thị số bước (Action: current_index/len(solution_path)) lên màn hình
    action_text = font.render(f"Action: {current_index}/{len(solution_path)}", True, (0, 0, 0))
    screen.blit(action_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()