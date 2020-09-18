import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
kivy.config.Config.set('graphics','resizable', False)
# Config.set('graphics', 'resizable', False)

class AIApp(App):
  
  def build(self):
    # return Label(text='Esse é o app')
    Window.size = (1024, 1024)
    return TheGrid()

  # Rodado toda vez que o app é iniciado
  def on_start(self):
    print('Starting app!')
    Window.bind(mouse_pos=self.on_mouse_pos)
    # Config.set('graphics', 'resizable', False)
    return

  # Rodado toda vez que o app é finalizado
  def on_stop(self):
    print('Ending app!')
    return

  def on_mouse_pos(self, window, pos):
    for butt in self.root.children:
        if butt.collide_point(*pos):
            # butt.background_color = (1, 0, 0, 1)
            butt.tocado()

class TheGrid(GridLayout):
    
  def __init__(self, **kwargs):
    super(TheGrid, self).__init__(**kwargs)
    self.cols = 42
    for i in range(0, 42*42):
      btn = Cell(value=i)
      # btn.bind(on_state=self.callback)
      self.add_widget(btn)

  def callback(self, instance):
    print(instance)
    # instance.background_color = (1, 0, 0, 1)

class Cell(Button):

  value = 0

  def __init__(self, value, **kwargs):
    super(Cell, self).__init__(**kwargs)
    self.value = value

  def tocado(self):
    if self.value % 2 == 0:
      self.background_color = (1, 0, 0, 1)
    else:
      self.background_color = (0, 0, 1, 1)

if __name__ == '__main__':
  AIApp().run()