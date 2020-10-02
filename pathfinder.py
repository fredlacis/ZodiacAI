import pygame
from grid import Grid
from cell import Cell
from queue import PriorityQueue
from distance import *
import math
import time
# pylint: disable=no-member

def algorithm(grid, see_every_cost):
  print("Setting variables")
  matrix = grid.matrix
  start, end = grid.get_start_end()

  count = 0
  open_set = PriorityQueue()
  open_set.put((0, count, start))
  came_from = {}
  g_score = {cell: float("inf") for row in matrix for cell in row}
  g_score[start] = 0
  f_score = {cell: float("inf") for row in matrix for cell in row}
  f_score[start] = h(start.get_pos(), end.get_pos())

  open_set_hash = {start}
  
  # speed
  slow_motion = 0.0

  print("Starting loop")
  while not open_set.empty():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
          if slow_motion >= 0.1:
            slow_motion -= 0.1
        elif event.key == pygame.K_LEFT:
          slow_motion += 0.1
        if event.key == pygame.K_c:
          see_every_cost = not see_every_cost

    current = open_set.get()[2]
    open_set_hash.remove(current)

    if current == end:
      reconstruct_path(came_from, end, grid, see_every_cost)
      print("end found")
      return True

    for neighbor in current.neighbors:
      temp_g_score = g_score[current] + neighbor.get_cost() # ??
      if temp_g_score < g_score[neighbor]:
        came_from[neighbor] = current
        g_score[neighbor] = temp_g_score
        f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
        if neighbor not in open_set_hash:
          count += 1
          open_set.put((f_score[neighbor], count, neighbor))
          open_set_hash.add(neighbor)
          neighbor.opened(g_score[neighbor])

    time.sleep(slow_motion)
    
    grid.draw(see_every_cost)

    if current != start:
      current.close()
    

def reconstruct_path(came_from, current, grid, see_every_cost):
  while current in came_from:
    current = came_from[current]
    current.on_short_path()
    grid.draw(see_every_cost)