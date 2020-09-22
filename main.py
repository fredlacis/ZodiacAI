import pygame

from pathfinder import *
from colors import *
from distance import *
from grid import Grid

# Window configuration
ROWS = 42
WIDTH = ROWS * 19
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Zodiac AI")

def main(win, rows, width):
  file_path = './maps/test_map_2.csv'
  grid = Grid(win, rows, width, file_path)

  run = True
  started = False
  while run:
    grid.draw()
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
          algorithm(grid)

        if event.key == pygame.K_r:
          grid = Grid(win, rows, width, file_path)


  pygame.quit()

main(WIN, ROWS, WIDTH)