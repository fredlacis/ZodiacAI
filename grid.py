import pygame
from cell import Cell
from cell_types import CellTypes
from colors import *
from utils import read_matrix

class Grid:
  def __init__(self, win, rows, width, file_path):
    self.win = win
    self.width = width
    self.rows = rows
    self.start = None
    self.end = None
    csv_matrix = read_matrix(file_path)
    self.matrix = self.make_grid(csv_matrix)

  def get_matrix(self):
    return self.matrix

  def get_start_end(self):
    return self.start, self.end

  def make_grid(self, csv_matrix):
    grid = []
    cell_width = self.width // self.rows
    for i in range(self.rows):
      grid.append([])
      for j in range(self.rows):
        cell = Cell(i, j, cell_width, self.rows, csv_matrix[j][i])
        if cell.get_type() == CellTypes.start:
          self.start = cell
        elif cell.get_type() == CellTypes.end:
          self.end = cell
        grid[i].append(cell)

    return grid

  def draw_grid_lines(self):
    gap = self.width // self.rows
    # TODO: Check this
    for i in range(self.rows):
      pygame.draw.line(self.win, GREY, (0, i * gap), (self.width, i * gap))
      for j in range(self.rows):
        pygame.draw.line(self.win, GREY, (j * gap, 0), (j * gap, self.width))

  def draw(self):
    self.win.fill(WHITE)

    for row in self.matrix:
      for cell in row:
        cell.draw(self.win)

    self.draw_grid_lines()
    pygame.display.update()