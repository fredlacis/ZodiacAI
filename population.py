import random
from copy import deepcopy
from math import floor
from numpy import interp

from attack_plan import Knight, House, Attack_Plan

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
    self.order_by_fitness()

    self.mating_pool = []

    if random.randint(0,1):
      one_percent = len(self.population)//100
      max_index = max(len(self.population) - (one_percent * self.current_generation), len(self.population)//2)
      chosen_part = self.population[:max_index]
    else:
      chosen_part = self.population

    print(len(chosen_part))
    
    for element in chosen_part:
      fitness = interp(element.fitness, [0, self.population[0].fitness], [0, 1])
      n = floor(fitness * 100)
      for _number_of_occurrences in range(n):
        self.mating_pool.append(element)

  def generate(self, mutation_rate):
    print(len(self.mating_pool))
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
      # child.optmize(try_amount = 15)
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