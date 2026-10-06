import pygame
from SokobanBoard import SokobanBoard
from PathFinder import PathFinder

class SingleGameEngine:
    def __init__(self, map_file):
        pygame.init()
        self.board = SokobanBoard(map_file)
        self.solver = PathFinder(self.board)
        
        # Tính kích thước cửa sổ DỰA THEO bản đồ thật
        self.TILE_SIZE = 40
        self.WIDTH = max(len(row) for row in self.board.grid) * self.TILE_SIZE
        self.HEIGHT = len(self.board.grid) * self.TILE_SIZE
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sokoban Game - OOP")
        self.font = pygame.font.Font(None, 30)

    def select_algorithm(self):
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

            self.screen.fill((200, 200, 200))
            text1 = self.font.render("Press U for UCS", True, (0, 0, 0))
            text2 = self.font.render("Press A for A*", True, (0, 0, 0))
            self.screen.blit(text1, (50, 200))
            self.screen.blit(text2, (50, 240))
            pygame.display.flip()
            
        return chosen_algorithm

    def run(self):
        algo = self.select_algorithm()
        if algo == 'UCS':
            solution_path, cost = self.solver.uniform_cost_search()
        else:
            solution_path, cost = self.solver.a_star_search()

        if not solution_path:
            print("Không tìm thấy đường đi!")
            pygame.quit()
            return

        initial_state = (self.board.initial_agent, self.board.initial_boxes)
        states = [initial_state]
        current = initial_state
        for action in solution_path:
            current = self.board.get_next_state(current, action)
            states.append(current)

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
                        is_paused = not is_paused
                    elif event.key == pygame.K_RIGHT:
                        if current_index < len(states) - 1:
                            current_index += 1
                    elif event.key == pygame.K_LEFT:
                        if current_index > 0:
                            current_index -= 1

            if not is_paused and current_index < len(states) - 1:
                if current_time - last_move_time > move_delay:
                    current_index += 1
                    last_move_time = current_time

            self._draw_board(states[current_index], current_index, len(solution_path))
            clock.tick(60)

        pygame.quit()

    def _draw_board(self, current_state, current_index, total_steps):
        agent_posit, box_posit = current_state
        self.screen.fill((200, 200, 200))

        for y in range(len(self.board.grid)):
            for x in range(len(self.board.grid[y])):
                if self.board.is_wall(x, y):
                    pygame.draw.rect(self.screen, (80, 80, 80), (x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))

        for (gx, gy) in self.board.goals:
            pygame.draw.circle(self.screen, (255, 0, 0), (gx * self.TILE_SIZE + self.TILE_SIZE // 2, gy * self.TILE_SIZE + self.TILE_SIZE // 2), 5)

        for (bx, by) in box_posit:
            if (bx, by) in self.board.goals:
                pygame.draw.rect(self.screen, (101, 67, 33), (bx * self.TILE_SIZE, by * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
            else:
                pygame.draw.rect(self.screen, (150, 90, 40), (bx * self.TILE_SIZE, by * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))

        if agent_posit is not None:
            center_x = agent_posit[0] * self.TILE_SIZE + self.TILE_SIZE // 2
            center_y = agent_posit[1] * self.TILE_SIZE + self.TILE_SIZE // 2
            pygame.draw.circle(self.screen, (0, 100, 255), (center_x, center_y), self.TILE_SIZE // 2 - 5)

        action_text = self.font.render(f"Action: {current_index}/{total_steps}", True, (0, 0, 0))
        self.screen.blit(action_text, (10, 10))
        pygame.display.flip()

if __name__ == "__main__":
    game = SingleGameEngine("example_map.txt")
    game.run()