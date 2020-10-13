import random
import string
from copy import deepcopy
from math import floor
from numpy import interp
from attack_plan import Knight, House, Attack_Plan

# INPUT -------------------------------------------------------------------
available_knights = [
  Knight("\033[01;31mSeiya\033[00m", 1.5),
  Knight("\033[01;32mIkki\033[00m", 1.4),
  Knight("\033[01;33mShiryu\033[00m", 1.3),
  Knight("\033[01;34mHyoga\033[00m", 1.2),
  Knight("\033[01;35mShun\033[00m", 1.1)
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

    for element in self.population:
      fitness = interp(element.fitness, [0, self.population[0].fitness], [0, 1])
      n = floor(fitness * 100)
      for _number_of_occurances in range(n):
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
GENERATION_AMOUNT = 200
POP_MAX = 500
MUTATION_RATE = 0.01

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

  print("GENERATION ", population.current_generation, " | Best Time: ", population.population[0].total_time, " | Best Fitness: ", population.population[0].fitness)
  if population.population[0].fitness > the_best.fitness:
    the_best = population.population[0]

population.print_self()
print("-"*50)
print("The best time is ", the_best.total_time, " and its fitness is ", the_best.fitness)
print("BATTLEPLAN")
the_best.print_self()
print("-"*50)
