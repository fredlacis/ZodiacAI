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

    self.population = None
    self.mutation_rate = None
    self.generation = None
    self.attack_plan = None

    self.font_50 = pygame.font.Font("assets/Roboto-Regular.ttf", 50)
    self.font_36 = pygame.font.Font("assets/Roboto-Regular.ttf", 36)
    self.font_24 = pygame.font.Font("assets/Roboto-Regular.ttf", 24)
    self.font_20 = pygame.font.Font("assets/Roboto-Regular.ttf", 20)
    self.font_12 = pygame.font.Font("assets/Roboto-Regular.ttf", 12)

    self.temple_img = pygame.image.load("assets/temple.png")
    self.menu_img = pygame.image.load("assets/menu.jpg")
    self.knight_images = {
      "Seiya"  : pygame.image.load("assets/Seiya.png"),
      "Ikki" : pygame.image.load("assets/Ikki.png"),
      "Shiryu" : pygame.image.load("assets/Shiryu.png"),
      "Hyoga"  : pygame.image.load("assets/Hyoga.png"),
      "Shun" : pygame.image.load("assets/Shun.png"),
    }

  def drawCurrent(self):
    if (self.population is not None
    and self.mutation_rate is not None
    and self.generation is not None
    and self.attack_plan is not None):
      self.draw(self.population, self.mutation_rate, self.generation, self.attack_plan, False)
    else:
      pygame.draw.rect(self.win, WHITE, (self.grid_width, 0, self.grid_width + self.tab_width, self.grid_width))

      img_rect = self.menu_img.get_rect()
      img_rect.center = (self.grid_width + self.tab_width/2, self.win_height/2)
      self.win.blit(self.menu_img, img_rect)


  def draw(self, population, mutation_rate, generation, attack_plan, update = True):
    self.population = population
    self.mutation_rate = mutation_rate
    self.generation = generation
    self.attack_plan = attack_plan

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
    best_result_txt = self.font_20.render("Best Result - Time: %.3fmin" % (attack_plan.total_time), True, BLACK)
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
      knight_spacing = min((self.grid_width + self.tab_width - knight_starting_x)/len(house_attack.chosen_knights), 70)
      knight_y = y1 + rect_height/2 - 5
      for i, knight in enumerate(house_attack.chosen_knights):
        knight_x = knight_starting_x + i * knight_spacing
        img_rect = self.knight_images[knight.name].get_rect()
        img_rect.center = (knight_x, knight_y)
        self.win.blit(self.knight_images[knight.name], img_rect)

        power_txt = self.font_12.render(str(knight.power), True, BLACK)
        power_rect = power_txt.get_rect(center=(knight_x, knight_y + img_rect.height/2 + 7))
        self.win.blit(power_txt, power_rect)

      time_txt = self.font_12.render("Time: %.3fmin" % (house_attack.calc_time_taken()), True, BLACK)
      time_txt_width = time_txt.get_rect().width
      time_txt_height = time_txt.get_rect().height
      time_rect = time_txt.get_rect(center=(self.grid_width + self.tab_width - time_txt_width/2 - 7, y1 + time_txt_height))
      self.win.blit(time_txt, time_rect)

    if update:
      pygame.display.update()