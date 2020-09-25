import pygame

from pathfinder import *
from colors import *
from distance import *
from grid import Grid
from utils import read_matrix

# Window configuration
ROWS = 42
WIDTH = ROWS * 23
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Zodiac AI")

def main(win, rows, width):
  matrix = read_matrix('./maps/map.csv')
  grid = Grid(win, rows, width, matrix)

  #debug
  see_every_cost = False

  run = True
  started = False
  while run:
    grid.draw(see_every_cost)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      
      if started:
        continue

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and not started:
          print("Updating neighbors")
          for row in grid.matrix:
            for cell in row:
              cell.update_neighbors(grid.matrix)
          print("Starting algorithm")
          algorithm(grid, see_every_cost)

        if event.key == pygame.K_r:
          grid = Grid(win, rows, width, file_path)

        if event.key == pygame.K_c:
          see_every_cost = not see_every_cost


  pygame.quit()

main(WIN, ROWS, WIDTH)