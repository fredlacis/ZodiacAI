import kivy
from kivy.uix.gridlayout import GridLayout

from cell import Cell

class TheGrid(GridLayout):
  def __init__(self, map_matrix, **kwargs):
    super(TheGrid, self).__init__(**kwargs)
    self.cols = 42
    for i in range(0, 42):
      for j in range(0, 42):
        btn = Cell(value=map_matrix[i][j])
        # btn.bind(on_state=self.callback)
        self.add_widget(btn)

  def callback(self, instance):
    print(instance)
    # instance.background_color = (1, 0, 0, 1)