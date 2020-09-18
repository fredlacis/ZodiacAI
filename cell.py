import kivy
from kivy.uix.button import Button

class Cell(Button):

  value = 0

  def __init__(self, value, **kwargs):
    super(Cell, self).__init__(**kwargs)
    self.value = value

  def hovered(self):
    if self.value % 2 == 0:
      self.background_color = (1, 0, 0, 1)
    else:
      self.background_color = (0, 0, 1, 1)