from kivy.uix.screenmanager import Screen
from widgets import AmazingGameMap


class AmazingGameScreen(Screen):

	def __init__(self):
		super().__init__()
		self.game_map = AmazingGameMap()
		self.add_widget(self.game_map)
