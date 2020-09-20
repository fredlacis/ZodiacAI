import kivy
from kivy.uix.button import Button

class Cell(Button):

  value = 0

  def __init__(self, value, **kwargs):
    super(Cell, self).__init__(**kwargs)
    self.value = value
    self.disabled = True
    self.background_disabled_normal = ''
    if self.value == 'S':
      self.background_color = (0, 1, 0, 1)
    elif self.value == 'E':
        self.background_color = (1, 0, 0, 1)
    elif self.value == '1':
      self.background_color = (0.95, 0.95, 0.95, 1)
    elif self.value == '5': 
      self.background_color = (0.9, 0.9, 0.9, 1)
    elif self.value == '200':
      self.background_color = (0.4, 0.4, 0.4, 1)
    else:
      self.background_color = (0, 0, 1, 1)

  def hovered(self):
    # self.background_color = (0, 0, 1, 1)
    pass