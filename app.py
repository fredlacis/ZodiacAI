import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

from grid import TheGrid

MAX_SIZE = 1024

class AIApp(App):

  def build(self):
    # Config window size and position
    Window.size = (1024, 1024)
    Window.top = 0
    Window.left = 0
    # Does not let window resize
    Window.bind(on_resize=self.never_resize)
    
    # Binds a function that checks mouse position to every mouse movement on the window
    #   - We are using this function to get win witch cell the mouse is on
    Window.bind(mouse_pos=self.on_mouse_pos)

    # Returning our main Widget, witch is the grid of cells
    return TheGrid()

  def on_start(self):
    print('Starting app!')
    return

  def on_mouse_pos(self, window, pos):
    for cell in self.root.children:
        if cell.collide_point(*pos):
            # Runs a function on the hovered cell
            cell.hovered()

  def never_resize(self, instance, x, y):
      Window.size = (MAX_SIZE, MAX_SIZE)