def get_color(value):
  if value == 'S':
    return "green"
  elif value == 'E':
    return "red"
  elif value == '1':
    return "white"
  elif value == '5': 
    return "gray"
  elif value == '200':
    return "dimgray"
  else:
    return "blue"