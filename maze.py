from random import randint, sample

class Maze(list):

	def __init__(self, width, height, starting_coord, ending_coord):
		super().__init__([[1, 1, 1, 1] for x in range(width)] for y in range(height))
		self.width, self.height = width, height
		self.starting_coord = starting_coord
		self.ending_coord = ending_coord
		self.stack = []
		self.direction = 1
		self.started_walking = False
		self.backtracked = False

	def __next__(self):
		if not self.started_walking:
			self.stack.append(self.starting_coord)
			self.started_walking = True
		directions = [[0, 1], [1, 0], [0, -1], [-1, 0]] # [up, right, down, left]
		d = self.direction
		if self.stack:
			x, y = self.stack[-1]
			c = self[y][x]
			if not self.backtracked:
				c[d-2] = 0								# opposite wall
			self.backtracked = False
			backtrack = True
			if not (x, y) == self.ending_coord and sum(c) > 1:
				choices = [i for i, e in enumerate(c) if e]
				for d in sample(choices, len(choices)):
					dx, dy = directions[d]
					dx += x
					dy += y
					if 0 <= dx < self.width and 0 <= dy < self.height and sum(self[dy][dx]) == 4:
						self.stack.append((dx, dy))
						c[d] = 0
						self.direction = d
						backtrack = False
						break
			elif (x, y) == self.ending_coord:
				c[1] = 0
			if backtrack:
				self.stack.pop()
				self.backtracked = True
			return x, y, self[y][x]
		else:
			return None
