# pylint: disable=no-member
import pygame

#Internal modules
import pathfinder
import battleplanner
from attack_plan import Knight, House, Attack_Plan

from grid import Grid
from planner_tab import Planner_Tab
from utils import read_matrix

# Window configuration
ROWS = 42
GRID_WIDTH = ROWS * 23
TAB_WIDTH = 450
clock = pygame.time.Clock()

WIN = pygame.display.set_mode((GRID_WIDTH + TAB_WIDTH, GRID_WIDTH))
pygame.display.set_caption("Zodiac AI")

# Genetic algorithm configuration
GENERATION_AMOUNT = 200
POP_MAX = 1000
MUTATION_RATE = 0.01

available_knights = [
  Knight("Seiya", 1.5, "\033[01;31mSeiya\033[00m"),
  Knight("Ikki", 1.4, "\033[01;32mIkki\033[00m"),
  Knight("Shiryu", 1.3, "\033[01;33mShiryu\033[00m"),
  Knight("Hyoga", 1.2, "\033[01;34mHyoga\033[00m"),
  Knight("Shun", 1.1, "\033[01;35mShun\033[00m")
]

# Main execution
def main(win, rows, width):
  matrix = read_matrix('./maps/map.csv')
  grid = Grid(win, rows, width, matrix)
  planner_tab = Planner_Tab(win, GRID_WIDTH, TAB_WIDTH)

  #debug
  see_every_cost = False

  run = True
  started = False
  while run:
    grid.draw(see_every_cost)
    planner_tab.drawCurrent()
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
          print("Starting pathfinder A* algorithm")
          houses = pathfinder.algorithm(grid, see_every_cost)
          print("Starting battleplan genetic algorithm")
          battleplanner.algorithm(planner_tab, GENERATION_AMOUNT, POP_MAX, MUTATION_RATE, available_knights, houses)

        if event.key == pygame.K_r:
          grid = Grid(win, rows, width, matrix)

        if event.key == pygame.K_c:
          see_every_cost = not see_every_cost

      if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
        pass

      clock.tick(10)

  pygame.quit()

main(WIN, ROWS, GRID_WIDTH)
