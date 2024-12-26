import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        return [[random.randint(0, 1) if randomize else 0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell
        cells = []
        for nx in range(max(0, x - 1), min(self.rows, x + 2)):
            for ny in range(max(0, y - 1), min(self.cols, y + 2)):
                if nx == x and ny == y:
                    continue
                cells.append(self.curr_generation[nx][ny])
        return cells

    def get_next_generation(self) -> Grid:
        grid = [[0] * self.cols for _ in range(self.rows)]
        for x in range(self.rows):
            for y in range(self.cols):
                alive = sum(self.get_neighbours((x, y)))
                if self.curr_generation[x][y] == 1:
                    if 2 <= alive <= 3:
                        grid[x][y] = 1
                else:
                    if alive == 3:
                        grid[x][y] = 1
        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename, "r")
        grid = [[int(cell) for cell in line.strip()] for line in f]
        rows = len(grid)
        cols = len(grid[0])
        game = GameOfLife(size=(rows, cols), randomize=False)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, "w")
        for row in self.curr_generation:
            f.write("".join(map(str, row)) + "\n")
