import csv
import numpy

def read_matrix(path):
  reader = csv.reader(open(path, "r"), delimiter=",")
  x = list(reader)
  result = numpy.array(x).astype("str")

  return result 