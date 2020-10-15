import random
import string
from copy import deepcopy
from math import pow, floor

class House:
  def __init__(self, difficulty):
    self.difficulty = difficulty

class Knight:
  def __init__(self, name, power, debug_name = ""):
    self.name = name
    self.power = power
    self.lifeCount = 5
    self.weakest = False
    if debug_name == "":
      self.debug_name = self.name
    else:
      self.debug_name = debug_name

class House_Attack:
  def __init__(self, house, chosen_knights):
    self.house = house
    self.chosen_knights = chosen_knights

  def calc_time_taken(self):
    total_power = 0.0
    for knight in self.chosen_knights:
      total_power += knight.power
    return self.house.difficulty / total_power

  def print_self(self):
    printed_str = "[🏛 -> %4d" % (self.house.difficulty)
    for knight in self.chosen_knights:
      printed_str += ", %20s : %1d" %(knight.debug_name, knight.lifeCount)
    printed_str += "] "
    print(printed_str)

  def self_to_string(self):
    printed_str = "[🏛 -> %4d" % (self.house.difficulty)
    for knight in self.chosen_knights:
      printed_str += ", %8s : %1d" %(knight.name, knight.lifeCount)
    printed_str += "] "
    return printed_str

class Attack_Plan:
  def __init__(self, houses, available_knights, empty = False):
    self.houses = deepcopy(houses)
    self.available_knights = deepcopy(available_knights)

    if not empty:
      self.plan = self.generate_random_attack_plan()
    else:
      self.plan = self.generate_empty_attack_plan()

    self.total_time = float("inf")
    self.fitness = 0.0

  def generate_pioneers(self):
    attack_plan = []

    for house in self.houses:
      knights_selection = []
      
      selected_knight = random.choice(self.available_knights)

      if selected_knight.weakest and selected_knight.lifeCount == 1:
        weakest_knight = selected_knight
        self.available_knights.remove(selected_knight)
        selected_knight = random.choice(self.available_knights)
        self.available_knights.append(weakest_knight)

      selected_knight.lifeCount -= 1

      knights_selection.append(selected_knight)
      
      if selected_knight.lifeCount == 0:
        self.available_knights.remove(selected_knight)
          
      house_attack = House_Attack(house, knights_selection)
      attack_plan.append(house_attack)

    return attack_plan

  def generate_random_attack_plan(self):
    attack_plan = self.generate_pioneers()

    while True:
      chosen_attack = random.choice(attack_plan)
      chosen_knight = random.choice(self.available_knights)

      if(chosen_knight in chosen_attack.chosen_knights):
        continue

      if chosen_knight.weakest and chosen_knight.lifeCount == 1:
        if len(self.available_knights) == 1:
          break
      else:
        chosen_attack.chosen_knights.append(chosen_knight)
        chosen_knight.lifeCount -= 1
        if chosen_knight.lifeCount == 0:
          self.available_knights.remove(chosen_knight)

    return attack_plan
  
  def generate_empty_attack_plan(self):
    attack_plan = []
    for house in self.houses:
      attack_plan.append(House_Attack(house, []))
    return attack_plan
    
  def calc_time(self):
    self.total_time = 0
    for house_attack in self.plan:
      self.total_time += house_attack.calc_time_taken()

  def calc_fitness(self):
    self.calc_time()
    self.fitness = pow(((1/self.total_time) * 1000), 8)

  def crossover(self, partner, houses, available_knights):
    # print("PARENTS ---------")
    # self.print_self()
    # partner.print_self()
    
    child = Attack_Plan(houses, available_knights, empty=True)

    a_attackers = []
    for knight in range(floor(len(available_knights)/2)):
      a_attackers.append(available_knights.pop(random.randint(0, len(available_knights)-1)))
    b_attackers = available_knights

    # Chose partner with highest fitness to get the highest Knights sequences
    if self.fitness > partner.fitness:
      main_partner = self
      secondary_partner = partner
    else:
      main_partner = partner
      secondary_partner = self

    for attacker in a_attackers:
      for i, house_attack in enumerate(secondary_partner.plan):
        for knight in house_attack.chosen_knights:
          if attacker.name == knight.name:
            attacker.lifeCount -= 1
            child.plan[i].chosen_knights.append(attacker)

    for attacker in b_attackers:
      for i, house_attack in enumerate(main_partner.plan):
        for knight in house_attack.chosen_knights:
          if attacker.name == knight.name:
            attacker.lifeCount -= 1
            child.plan[i].chosen_knights.append(attacker)

    # print("\n---------- CHILD ----------\n")
    # child.print_self()
    return child

  def mutate(self, mutationRate):
    for _i, house_attack in enumerate(self.plan):
      if random.uniform(0, 1) < mutationRate:
        index_to_change = random.randint(0, len(self.plan)-1)
        current_house_knights = house_attack.chosen_knights
        house_attack.chosen_knights = self.plan[index_to_change].chosen_knights
        self.plan[index_to_change].chosen_knights = current_house_knights


  def is_complete(self):
    for house_attack in self.plan:
      if not house_attack.chosen_knights:
        return False
    return True

  def print_self(self):
    print("-" * 60)
    for house_attack in self.plan:
      house_attack.print_self()

  def self_to_string(self):
    self_string = ""
    for house_attack in self.plan:
      self_string += house_attack.self_to_string() + "\n"
    return self_string


  def print_total_time(self, index):
    print("Attack Plan %d Time = %.2f | Fitness = %.7f" % (index, self.total_time, self.fitness))