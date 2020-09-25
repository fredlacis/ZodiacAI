import pygame
from cell import Cell
from cell_types import CellTypes
from colors import *

class Grid:
  def __init__(self, win, rows, width, matrix):
    # Attributes for drawing grid on window
    self.win = win
    self.width = width
    self.rows = rows
    self.start = None
    self.end = None

    # Organize grid according to matrix
    self.matrix = self.make_grid(matrix)

  # Get matrix
  def get_matrix(self):
    return self.matrix

  # Get grid start and end
  def get_start_end(self):
    return self.start, self.end

  # Organize grid according to matrix 
  def make_grid(self, matrix):
    grid = []
    cell_width = self.width // self.rows
    
    for i in range(self.rows):
      grid.append([])
      for j in range(self.rows):
        cell = Cell(i, j, cell_width, self.rows, matrix[j][i])
        if cell.cell_type == CellTypes.start:
          self.start = cell
        elif cell.cell_type == CellTypes.end:
          self.end = cell
        grid[i].append(cell)

    return grid

  # Draw Grid lines between cells
  def draw_grid_lines(self):
    gap = self.width // self.rows
    # TODO: Check this
    for i in range(self.rows):
      pygame.draw.line(self.win, GREY, (0, i * gap), (self.width, i * gap))
      for j in range(self.rows):
        pygame.draw.line(self.win, GREY, (j * gap, 0), (j * gap, self.width))

  # Draw grid on window based on its attributes
  def draw(self, see_every_cost):
    self.win.fill(WHITE)

    for row in self.matrix:
      for cell in row:
        cell.draw(self.win, see_every_cost)

    self.draw_grid_lines()
    pygame.display.update()