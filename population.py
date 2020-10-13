import random
import string
from datetime import datetime
from copy import deepcopy
from math import floor
from numpy import interp
from attack_plan import Knight, House, Attack_Plan

# INPUT -------------------------------------------------------------------
available_knights = [
  Knight("Seiya", 1.5, "\033[01;31mSeiya\033[00m"),
  Knight("Ikki", 1.4, "\033[01;32mIkki\033[00m"),
  Knight("Shiryu", 1.3, "\033[01;33mShiryu\033[00m"),
  Knight("Hyoga", 1.2, "\033[01;34mHyoga\033[00m"),
  Knight("Shun", 1.1, "\033[01;35mShun\033[00m")
]

houses = [ 
  House(0, 50), 
  House(1, 55), 
  House(2, 60), 
  House(3, 70), 
  House(4, 75), 
  House(5, 80), 
  House(6, 85), 
  House(7, 90), 
  House(8, 95), 
  House(9, 100), 
  House(10, 110), 
  House(11, 120)
]
# END INPUT -------------------------------------------------------------------

def find_weakest():
  weakest = available_knights[0]
  for knight in available_knights:
    if knight.power < weakest.power:
      weakest = knight
  weakest.weakest = True

def log(attack_plan, generation_amount, population_size, mutation_rate):
  f = open("result_logs.txt", "a")
  f.write("┏" + "━" * 58 + "┓" + "\n")
  f.write("┃" + " " * 19 + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " " * 20 + "┃" + "\n")
  f.write("┗" + "━" * 58 + "┛" + "\n")
  f.write("\t%29s: %d\n" % ("Generations", generation_amount))
  f.write("\t%29s: %d\n" % ("Population", population_size))
  f.write("\t%29s: %.3f\n" % ("Mutation rate", mutation_rate))
  f.write("\t%29s: %.4f\n" % ("Time", attack_plan.total_time))
  f.write("\t%29s: %.4f\n" % (" Fitness", attack_plan.fitness))
  f.write("┏" + "━" * 58 + "┓" + "\n")
  f.write("┃" + " " * 23 + "ATTACK PLAN" + " " * 24 + "┃" + "\n")
  f.write("┗" + "━" * 58 + "┛" + "\n")
  f.write(the_best.self_to_string())
  f.write("━" * 60 + "\n")
  f.write("\n")
  f.close()

class Population:
  def __init__(self, houses, available_knights, num):
    self.population = []
    self.mating_pool = []
    self.current_generation = 0

    self.houses = houses
    self.available_knights = available_knights

    for _i in range(num):
      attack_plan = Attack_Plan(houses, available_knights)
      self.population.append(attack_plan)
  
  def calc_fitness(self):
    for attack_plan in self.population:
      attack_plan.calc_fitness()

  def order_by_fitness(self):
    self.population.sort(key=lambda x: x.fitness, reverse=True)

  def natural_selection(self):
    self.calc_fitness()

    population.order_by_fitness()
    self.mating_pool = []

    best_half = self.population#[:len(self.population)//2]
    for element in best_half:
      fitness = interp(element.fitness, [0, self.population[0].fitness], [0, 1])
      n = floor(fitness * 100)
      for _number_of_occurrences in range(n):
        self.mating_pool.append(element)

  def generate(self, mutation_rate):
    for i in range(len(self.population)):
      partnerA = random.choice(self.mating_pool)
      partnerB = random.choice(self.mating_pool)
      
      # Do crossover until a valid child is born
      safe_counter = 0
      while True:
        child = partnerA.crossover(partnerB, deepcopy(self.houses), deepcopy(self.available_knights))

        if child.is_complete():
          break
        
        # If parents can't produce a child, one of the parents becomes the child
        if safe_counter >= 10:
          child = random.choice([partnerA, partnerB])
          break
        safe_counter += 1
      
      child.mutate(mutation_rate)
      self.population[i] = child
    self.current_generation += 1

  def print_self(self):
    display_limit = min(len(self.population), 20)
    for i in range(display_limit):
      self.population[i].print_total_time(i)
      print("-" * 60)

  def print_mating_pool(self):
    for subject_index in range(min(len(self.population),20)):
      subject_count = self.mating_pool.count(self.population[subject_index])
      print("[%f: %d]" % (self.population[subject_index].fitness, subject_count))



# ------------------------------------------------------------------------
GENERATION_AMOUNT = 2
POP_MAX = 200
MUTATION_RATE = 0.035

find_weakest()
population = Population(houses, available_knights, POP_MAX)

the_best = population.population[0]

for generation in range(0, GENERATION_AMOUNT):
  # print("NAT SELECTION")
  population.natural_selection()
  # print("GENERATE")
  population.generate(MUTATION_RATE)
  # print("CALC FITNESS")
  population.calc_fitness()
  # print("ORDER BY")
  population.order_by_fitness()

  print("GENERATION %4d" % population.current_generation, " | Best Time: %.3f" % population.population[0].total_time, " | Best Fitness: %.3f" % population.population[0].fitness)
  if population.population[0].fitness > the_best.fitness:
    the_best = population.population[0]

# population.print_self()
print("-"*60)
print("The best time is ", the_best.total_time, " and its fitness is ", the_best.fitness)
print("BATTLEPLAN")
the_best.print_self()
print("-"*60)
log(the_best, GENERATION_AMOUNT, POP_MAX, MUTATION_RATE)
