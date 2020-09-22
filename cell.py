import pygame
from colors import *
from utils import get_color
from cell_types import CellTypes

class Cell:

  def __init__(self, row, col, width, total_rows, map_value):
    # For drawing
    self.row = row
    self.col = col
    self.width = width
    self.x = row * width
    self.y = col * width
    self.total_rows = total_rows
    # For the algorithm
    self.neighbors = []
    self.was_opened = False
    self.was_visited = False
    self.is_path = False
    self.cost = 0
    self.cell_type = 0
    # Defining cost and cell_type based on value read from csv file
    if map_value != 'S' and map_value != 'E':
      self.cost = int(map_value)
      if map_value == '200' or map_value == '5' or map_value == '1':
        self.cell_type = CellTypes.path
      else:
        self.cell_type = CellTypes.temple
    else:
      if map_value == 'S':
        self.cell_type = CellTypes.start
      else:
        self.cell_type = CellTypes.end

  def get_pos(self):
    return self.row, self.col

  def is_closed(self):
    return self.was_visited

  def close(self):
    self.was_visited = True

  def is_open(self):
    return self.was_opened

  def opened(self):
    self.was_opened = True

  def on_short_path(self):
    self.is_path = True

  def get_cost(self):
    return self.cost

  def get_type(self):
    return self.cell_type

  def draw(self, win):
    if self.is_path:
      pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.width))
    elif self.was_visited:
      pygame.draw.rect(win, PURPLE, (self.x, self.y, self.width, self.width))
    elif self.was_opened:
      pygame.draw.rect(win, ORANGE, (self.x, self.y, self.width, self.width))
    else:
      pygame.draw.rect(win, get_color(self.cell_type, self.cost), (self.x, self.y, self.width, self.width))

  def update_neighbors(self, matrix):
    if self.row < self.total_rows - 1: #DOWN
      self.neighbors.append(matrix[self.row + 1][self.col])

    if self.row > 0: #UP
      self.neighbors.append(matrix[self.row - 1][self.col])

    if self.col < self.total_rows - 1: #RIGHT
      self.neighbors.append(matrix[self.row][self.col + 1])

    if self.col > 0: #LEFT
      self.neighbors.append(matrix[self.row][self.col - 1])

  # Function used to compare two Cells
  def __lt__(self, other):
    # TODO: implement this
    return False