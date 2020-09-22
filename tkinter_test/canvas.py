import time
import random
import sys

from tkinter import *

from utils.read_matrix import read_matrix
from utils.get_color import get_color

zodiac_map = read_matrix('../maps/' + sys.argv[1] + '.csv')
valueList = ['1', '5', '200', 'S', 'E', '0']

class Cell():
    COLOR_BG = "white"
    COLOR_BORDER = "black"

    def __init__(self, master, x, y, size, value):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= False
        self.value = value

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = get_color(self.value)
            outline = Cell.COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)

class CellGrid(Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):
            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize, zodiac_map[row][column]))

            self.grid.append(line)

        self.draw()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()


if __name__ == "__main__" :
    app = Tk()

    grid = CellGrid(app, 42, 42, 20)
    grid.pack()

    for i in range(0, 42):
      for j in range(0, 42):
        grid.grid[i][j].value = '0'
        grid.grid[i][j].draw()
        
        app.update()

        # time.sleep(0.1)
    