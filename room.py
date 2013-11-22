

class Room(object):
	def __init__(self, name):
		self.name = name
		self.rolls = []

	def roll(self, n, sides, bonus):
		roll = Roll(n, sides, bonus)
		self.rolls.append(roll)
		return roll

	def render(self):
		ret = '' # TODO html, buttons, etc
		for roll in rolls:
			ret += roll.render()


class Roll(object):
	def __init__(self, n, sides, bonus):
		self.n, self.sides, self.bonus = n, sides, bonus
		self.results = [4 for x in range(n)] # TODO random

	@property
	def value(self):
		return sum(self.results) + self.bonus

	def render(self):
		return "foo"
		#TODO html
