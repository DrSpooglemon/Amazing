from kivy.core.window import Window
from kivy.utils import platform
if platform != 'android':
	Window.size = 854, 444
from kivy.app import App
from screens import *


class AmazingApp(App):

	def build(self):
		self.game_screen = AmazingGameScreen()
		return self.game_screen


if __name__ == '__main__':
	AmazingApp().run()
