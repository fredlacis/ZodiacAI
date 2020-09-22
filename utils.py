import csv
import numpy
from cell_types import CellTypes
from colors import *

def read_matrix(path):
  reader = csv.reader(open(path, "r"), delimiter=",")
  x = list(reader)
  result = numpy.array(x).astype("str")

  return result 

def get_color(cell_type, cost):
  if cell_type == CellTypes.start:
    return RED
  elif cell_type == CellTypes.end:
    return GREEN
  elif cell_type == CellTypes.path:
    if cost == 1:
      return GREY
    elif cost == 5:
      return LIGHT_GRAY
    else:
      return DARK_GRAY
  elif cell_type == CellTypes.temple:
    return BLUE
  else:
    return BLACK