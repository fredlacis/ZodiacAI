from datetime import datetime
import pygame
from population import Population
# from planner_tab import Planner_Tab
from colors import BLACK

# Font config
pygame.font.init()
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 15)

# TODO Not working on linux
def log(attack_plan, generation_amount, population_size, mutation_rate):
  f = open("result_logs.txt", "a")
  f.write("=" * 60 + "\n")
  f.write("|" + " " * 19 + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " " * 20 + "|" + "\n")
  f.write("=" * 60 + "\n")
  f.write("\t%29s: %d\n" % ("Generations", generation_amount))
  f.write("\t%29s: %d\n" % ("Population", population_size))
  f.write("\t%29s: %.3f\n" % ("Mutation rate", mutation_rate))
  f.write("\t%29s: %.4f\n" % ("Time", attack_plan.total_time))
  f.write("\t%29s: %.4f\n" % (" Fitness", attack_plan.fitness))
  f.write("=" * 60 + "\n")
  f.write("|" + " " * 23 + "ATTACK PLAN" + " " * 24 + "|" + "\n")
  f.write("=" * 60 + "\n")
  f.write(attack_plan.self_to_string())
  f.write("=" * 60 + "\n")
  f.write("\n")
  f.close()

def find_weakest(available_knights):
  weakest = available_knights[0]
  for knight in available_knights:
    if knight.power < weakest.power:
      weakest = knight
  weakest.weakest = True

# ------------------------------------------------------------------------
def algorithm(planner_tab, generation_amount, pop_max, mutation_rate, available_knights, houses):

  find_weakest(available_knights)
  population = Population(houses, available_knights, pop_max)

  the_best = population.population[0]

  for _generation in range(0, generation_amount):
    # print("NAT SELECTION")
    population.natural_selection()
    # print("GENERATE")
    population.generate(mutation_rate)
    # print("CALC FITNESS")
    population.calc_fitness()
    # print("ORDER BY")
    population.order_by_fitness()

    print("GENERATION %4d" % population.current_generation, " | Best Time: %.3f" % population.population[0].total_time, " | Best Fitness: %.3f" % population.population[0].fitness)
    if population.population[0].fitness > the_best.fitness:
      the_best = population.population[0]

    planner_tab.draw(pop_max, mutation_rate, population.current_generation, the_best)

  # population.print_self()
  print("-"*60)
  print("The best time is ", the_best.total_time, " and its fitness is ", the_best.fitness)
  print("BATTLEPLAN")
  the_best.print_self()
  print("-"*60)
  log(the_best, generation_amount, pop_max, mutation_rate)
