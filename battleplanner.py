from battle_elements import BattleHouse, Warrior

def generateRandomBattlePlan(house_levels, warrior_options):
  housesPath = []

  for house_level in house_levels:
    housesPath.append(BattleHouse(warrior_options, house_level))

  return housesPath

def battleplanner(house_levels, warrior_options):
  print(house_levels)
  print(warrior_options)

  generateRandomBattlePlan(house_levels, warrior_options)

  