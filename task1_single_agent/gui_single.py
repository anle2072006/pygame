import pygame
from board import read_map, wall, find_agentandboxes, find_next_state

pygame.init()

WIDTH = 500
HEIGHT = 500

TILE_SIZE = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban Game")

grid = read_map("example_map.txt")

agent_posit, box_posit = find_agentandboxes(grid)

running  = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:#di chuyen
            direction = None
            if event.key == pygame.K_UP:
                direction = 'North'
            elif event.key == pygame.K_DOWN:
                direction = 'South'
            elif event.key == pygame.K_LEFT:
                direction = 'West'
            elif event.key == pygame.K_RIGHT:
                direction = 'East'

            if direction is not None:
                result = find_next_state(grid, (agent_posit, box_posit), direction)
                if result is not None:
                    agent_posit, box_posit = result

    screen.fill((200, 200, 200))

    for y in range(len(grid)):# vẽ tường
        for x in range(len(grid[y])):
            if wall(grid, x, y):
                pygame.draw.rect(screen,(80, 80, 80), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    for (bx, by) in box_posit:
        pygame.draw.rect(screen, (150, 90, 40), (bx * TILE_SIZE, by * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    if agent_posit is not None:
        center_x = agent_posit[0] * TILE_SIZE + TILE_SIZE // 2 
        center_y = agent_posit[1] * TILE_SIZE + TILE_SIZE // 2
        radius = TILE_SIZE // 2 - 5
        
        pygame.draw.circle(screen, (0, 100, 255), (center_x, center_y), radius)

    pygame.display.flip()
    clock.tick(60) #giới hạn fps

pygame.quit()