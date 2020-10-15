import pygame
import os

from colors import BLACK, GREY, WHITE

# Font config
pygame.font.init()

class Planner_Tab:
  def __init__(self, win, grid_width, tab_width):
    self.win = win
    self.win_height = grid_width
    self.grid_width = grid_width
    self.tab_width = tab_width

    self.font_50 = pygame.font.Font("assets/Roboto-Regular.ttf", 50)
    self.font_36 = pygame.font.Font("assets/Roboto-Regular.ttf", 36)
    self.font_24 = pygame.font.Font("assets/Roboto-Regular.ttf", 24)

    self.temple_img = pygame.image.load("assets/temple.png")

    self.knight_images = {
      "Seiya"  : pygame.image.load("assets/Seiya.png"),
      "Ikki" : pygame.image.load("assets/Ikki.png"),
      "Shiryu" : pygame.image.load("assets/Shiryu.png"),
      "Hyoga"  : pygame.image.load("assets/Hyoga.png"),
      "Shun" : pygame.image.load("assets/Shun.png"),
    }

  def draw(self, population, mutation_rate, generation, attack_plan):
    pygame.draw.rect(self.win, WHITE, (self.grid_width, 0, self.grid_width + self.tab_width, self.grid_width))

    # Title
    title_txt = self.font_36.render("Genetic Battle Planner", True, BLACK)
    title_rect = title_txt.get_rect(center=(self.grid_width + self.tab_width/2, 20))
    self.win.blit(title_txt, title_rect)

    # Population
    pop_txt = self.font_24.render("Population size: " + str(population), True, BLACK)
    pop_rect = pop_txt.get_rect(center=(self.grid_width + self.tab_width/2, 52))
    self.win.blit(pop_txt, pop_rect)

    # Mutation rate
    mutation_txt = self.font_24.render("Mutation rate: " + str(mutation_rate), True, BLACK)
    mutation_rect = mutation_txt.get_rect(center=(self.grid_width + self.tab_width/2, 80))
    self.win.blit(mutation_txt, mutation_rect)

    # Divider
    pygame.draw.line(self.win, GREY, (self.grid_width, 97), (self.grid_width + self.tab_width, 97))

    # Generation 
    generation_txt = self.font_24.render("Generation: " + str(generation), True, BLACK)
    generation_rect = generation_txt.get_rect(center=(self.grid_width + self.tab_width/2, 114))
    self.win.blit(generation_txt, generation_rect)

    # Best result
    best_result_txt = self.font_24.render("Best Result - Time: %.3fmin - Fitness: %.3f" % (attack_plan.total_time, attack_plan.fitness), True, BLACK)
    best_result_rect = best_result_txt.get_rect(center=(self.grid_width + self.tab_width/2, 136))
    self.win.blit(best_result_txt, best_result_rect)

    # House attacks
    rect_spacing = 2
    rect_height = ((self.win_height - 150) / len(attack_plan.plan))
    rect_width = self.tab_width
    
    for i, house_attack in enumerate(attack_plan.plan):
      x1 = self.grid_width
      y1 = 150 + i * rect_height
      
      # Display gray box
      pygame.draw.rect(self.win, GREY, (x1, y1 + rect_spacing, rect_width, rect_height - rect_spacing))
      
      # Display temple image
      img_rect = self.temple_img.get_rect()
      img_rect.center = (self.grid_width + 30, y1 + rect_height/2)
      self.win.blit(self.temple_img, img_rect)

      # Display difficulty
      difficulty_txt = self.font_50.render(str(house_attack.house.difficulty), True, BLACK)
      difficulty_rect = difficulty_txt.get_rect(center=(self.grid_width + 100, y1 + rect_height/2))
      self.win.blit(difficulty_txt, difficulty_rect)

      # Display warriors
      knight_starting_x = self.grid_width + 180
      for i, knight in enumerate(house_attack.chosen_knights):
        img_rect = self.knight_images[knight.name].get_rect()
        img_rect.center = (knight_starting_x + i * 70, y1 + rect_height/2)
        self.win.blit(self.knight_images[knight.name], img_rect)

    pygame.display.flip()