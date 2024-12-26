import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отрисовать границу экрана."""
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """Отображает текущее состояние клеток."""
        height, width = screen.getmaxyx()
        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                if 0 < i < height - 1 and 0 < j < width - 1:
                    char = "O" if cell else " "  # 'O' для живой клетки, пробел для мёртвой
                    screen.addch(i, j, char)

    def display_status(self, screen) -> None:
        """Отображает статус игры внизу экрана."""
        height, _ = screen.getmaxyx()
        screen.addstr(
            height - 1,
            0,
            f"Нажмите [q] для выхода | Поколение: {self.life.generations}",
            curses.color_pair(1) | curses.A_BOLD,
        )

    def run(self) -> None:
        """Основной цикл игры."""
        screen = curses.initscr()
        curses.curs_set(0)
        screen.nodelay(True)
        screen.timeout(100)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        running = True
        while running:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.display_status(screen)
            screen.refresh()
            self.life.step()
            key = screen.getch()
            if key == ord("q"):  # Если нажата клавиша 'q', выходим из игры
                running = False
            if not self.life.is_changing or self.life.is_max_generations_exceeded:
                running = False
            self.life.step()
        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((50, 50), max_generations=100)
    ui = Console(life)
    ui.run()
