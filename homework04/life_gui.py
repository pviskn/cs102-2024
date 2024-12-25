import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        # Размер клеточного поля
        self.cell_size = cell_size
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

        # Создание кнопки для паузы/возобновления
        self.button = pygame.Rect(0, 0, 130, 40)

        # Устанавливаем состояние игры: False - пауза, True - активна
        self.status = False

        # Добавляем название окну игры
        pygame.display.set_caption("Game of Life")

        # Устанавливаем шрифт для кнопок и сообщений
        pygame.font.init()
        self.font = pygame.font.Font(None, 30)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.screen.get_width(), self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.screen.get_height()))
        for y in range(0, self.screen.get_height(), self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.screen.get_width(), y))

    def draw_grid(self) -> None:
        """Отрисовать список клеток"""
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                color = pygame.Color("green") if self.life.curr_generation[y][x] == 1 else pygame.Color("white")
                rect = pygame.Rect(
                    x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size
                )
                pygame.draw.rect(self.screen, color, rect)

    def handle_mouse_click(self, event) -> None:
        """Обработать клики мыши по кнопке паузы/возобновления игры"""
        mouse_pos = event.pos
        if self.button.collidepoint(mouse_pos):
            self.status = not self.status

    def handle_cell_editing(self, event) -> None:
        """Обработать редактирование клеток в режиме паузы"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            pos_x = mouse_pos[0] // self.cell_size
            pos_y = mouse_pos[1] // self.cell_size
            # Изменение состояния клетки
            self.life.curr_generation[pos_y][pos_x] = 1 - self.life.curr_generation[pos_y][pos_x]

        self.draw_grid()
        self.draw_lines()

    def draw_pause_button(self) -> None:
        """Отрисовать кнопку паузы"""
        pygame.draw.rect(self.screen, pygame.Color("light gray"), self.button, border_radius=10)
        pause_text = self.font.render("Pause", True, pygame.Color("black"))
        self.screen.blit(pause_text, (35, 13))

    def draw_resume_button(self) -> None:
        """Отрисовать кнопку возобновления"""
        pygame.draw.rect(self.screen, pygame.Color("light gray"), self.button, border_radius=10)
        resume_text = self.font.render("Resume", True, pygame.Color("black"))
        self.screen.blit(resume_text, (35, 13))

    def display_errors(self):
        """Отображает ошибки, если они есть"""
        if self.life.is_max_generations_exceeded:
            error_max_generation = self.font.render("Max generations exceeded", True, pygame.Color("red"))
            self.screen.blit(error_max_generation, (self.width // 4, self.height // 2))
            return True

        if not self.life.is_changing:
            error_changing = self.font.render("Stable game obtained", True, pygame.Color("red"))
            self.screen.blit(error_changing, (self.width // 4, self.height // 2))
            return True

        return False

    def run(self) -> None:
        """Запуск игры с отрисовкой и обновлением состояния"""
        pygame.init()
        clock = pygame.time.Clock()
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
                    self.handle_cell_editing(event)
            if self.display_errors():
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
            if not self.status:
                self.life.step()
            self.draw_lines()
            self.draw_grid()

            if self.status is False:
                self.draw_pause_button()
            else:
                self.handle_cell_editing(event)
                self.draw_resume_button()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((50, 50), max_generations=50)
    game = GUI(life)
    game.run()
