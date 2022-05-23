from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.atlas import Atlas
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock, mainthread
from maze import Maze

from random import randint, choice


d = 32
w, w_mod = divmod(Window.width, d)
h, h_mod = divmod(Window.height, d)

margins = hm, vm = w_mod // 2, h_mod // 2


tile_atlas = Atlas(f'assets/tiles.atlas')
outline_atlas = Atlas(f'assets/outline.atlas')


def random_color():
	return choice([
					(1, .1, 0), (1, .4, 0), (1, 1, 0),
					(0, 1,  0), (0, .5, 1), (0, 1, 1),
					(1, 0, 1), (.5, 0, 1)
				])

def get_texture(walls):
	if walls == [1, 1, 1, 1]:
		return tile_atlas['all']
	elif walls == [1, 0, 0, 1]:
		return tile_atlas['top-left']
	elif walls == [1, 1, 0, 0]:
		return tile_atlas['top-right']
	elif walls == [1, 1, 0, 1]:
		return tile_atlas['top-both']
	elif walls == [0, 0, 1, 1]:
		return tile_atlas['bottom-left']
	elif walls == [0, 1, 1, 0]:
		return tile_atlas['bottom-right']
	elif walls == [0, 1, 1, 1]:
		return tile_atlas['bottom-both']
	elif walls == [1, 0, 1, 0]:
		return tile_atlas['top-bottom']
	elif walls == [0, 1, 0, 1]:
		return tile_atlas['left-right']
	elif walls == [1, 0, 1, 1]:
		return tile_atlas['left-both']
	elif walls == [1, 1, 1, 0]:
		return tile_atlas['right-both']
	elif walls == [1, 0, 0, 0]:
		return tile_atlas['top']
	elif walls == [0, 0, 1, 0]:
		return tile_atlas['bottom']
	elif walls == [0, 0, 0, 1]:
		return tile_atlas['left']
	elif walls == [0, 1, 0, 0]:
		return tile_atlas['right']
	else:
		raise Exception(walls)

om = d / 16										#outline margin size
cm = om * 2
def get_outline_rect_kwargs(outline_name, i=0, j=0):
	texture = outline_atlas[outline_name]
	if outline_name == 'top-left':
		kw = {
			'texture':	texture,
			'pos':		(hm - cm, vm + (h-1) * d),
			'size':		(d + cm,) * 2}
	elif outline_name == 'top-right':
		kw = {
			'texture':	texture,
			'pos':		(hm + (w-1) * d, vm + (h-1) * d),
			'size':		(d + cm,) * 2}
	elif outline_name == 'bottom-left':
		kw = {
			'texture':	texture,
			'pos':		(hm - cm, vm - cm),
			'size':		(d + cm,) * 2}
	elif outline_name == 'bottom-right':
		kw = {
			'texture':	texture,
			'pos':		(hm + (w-1) * d, vm - cm),
			'size':		(d + cm,) * 2}
	elif outline_name == 'top':
		kw = {
			'texture':	texture,
			'pos':		((hm - om) + i * d, vm + (h-1) * d),
			'size':		(d + om,) * 2}
	elif outline_name == 'bottom':
		kw = {
			'texture':	texture,
			'pos':		((hm - om) + i * d, vm - om * 2),
			'size':		(d + om,) * 2}
	elif outline_name == 'left':
		kw = {
			'texture':	texture,
			'pos':		(hm - cm, vm + j * d),
			'size':		(d + cm, d)}
	elif outline_name == 'right':
		kw = {
			'texture':	texture,
			'pos':		(hm + (w-1) * d, vm + j * d),
			'size':		(d + om, ) * 2}
	elif outline_name == 'left-cap-top':
		kw = {
			'texture':	texture,
			'pos':		(hm - cm, vm + j * d),
			'size':		(cm + om, d + cm)}
	elif outline_name == 'left-cap-bottom':
		kw = {
			'texture':	texture,
			'pos':		(hm - cm, vm - cm + j * d),
			'size':		(cm + om , d + cm)}
	elif outline_name == 'right-cap-top':
		kw = {
			'texture':	texture,
			'pos':		((hm - om) + d * (w), vm + j * d),
			'size':		(om + cm, d + cm)}
	elif outline_name == 'right-cap-bottom':
		kw = {
			'texture':	texture,
			'pos':		((hm - om) + d * (w), vm - cm + j * d),
			'size':		(om + cm , d + cm)}
	return kw



class AmazingGameMap(Widget):

	def __init__(self):
		super().__init__()
		self.maze = Maze(w, h, starting_coord=(0, 5), ending_coord=(w-1, 5))
		self.tiles = [[] for j in range(h)]
		up_front = False
		with self.canvas:
			self.color = Color(*random_color())
			for corner in {'top-left', 'top-right', 'bottom-left', 'bottom-right'}:
				Rectangle(**get_outline_rect_kwargs(corner))

			for i in range(1, w-1):
				Rectangle(**get_outline_rect_kwargs('top', i=i))
				Rectangle(**get_outline_rect_kwargs('bottom', i=i))

			for j in range(1, h-1):
				if j == self.maze.starting_coord[1] - 1:
					Rectangle(**get_outline_rect_kwargs('left-cap-top', j=j))
				elif j == self.maze.starting_coord[1] + 1:
					Rectangle(**get_outline_rect_kwargs('left-cap-bottom', j=j))
				else:
					rect = Rectangle(**get_outline_rect_kwargs('left', j=j))
					if j == self.maze.starting_coord[1]:
						self.starting_outline = rect							#starting outline
						#------------------------------------------------------------------------
				if j == self.maze.ending_coord[1] - 1:
					Rectangle(**get_outline_rect_kwargs('right-cap-top', j=j))
				elif j == self.maze.ending_coord[1] + 1:
					Rectangle(**get_outline_rect_kwargs('right-cap-bottom', j=j))
				else:
					rect = Rectangle(**get_outline_rect_kwargs('right', j=j))
					if j == self.maze.ending_coord[1]:
						self.ending_outline = rect								#ending outline
						#----------------------------------------------------------------------
			if up_front:
				cell = next(self.maze)

				while cell:
					self.add_texture(*cell)
					cell = next(self.maze)
			else:
				for i in range(w):
					for j in range(h):
						self.add_texture(i, j, self.maze[j][i])
				Clock.schedule_interval(self.walk, 1/100)

	def add_texture(self, x, y, walls):
		with self.canvas:
			self.tiles[y].append(
				Rectangle(
					texture=get_texture(walls),
					pos=(hm + x * d, vm + y * d),
					size=(d, d)))

	def walk(self, _):
		cell = next(self.maze)
		if cell:
			x, y, walls = cell
			if (x, y) == self.maze.starting_coord:
				try:
					self.canvas.children.remove(self.starting_outline)
				except Exception as e:
					print(e)
			elif (x, y) == self.maze.ending_coord:
				try:
					self.canvas.children.remove(self.ending_outline)
				except Exception as e:
					print(e)
			self.tiles[y][x].texture = get_texture(walls)
		else:
			print('finished')
			return False
