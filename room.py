import quantumrandom
import time

generator = quantumrandom.cached_generator()
def die(sides): return quantumrandom.randint(1, sides, generator)


class Room(object):
	def __init__(self, name):
		self.name = name
		self.rolls = []

	def roll(self, user, n, sides, bonus):
		roll = Roll(user, n, sides, bonus)
		self.rolls.append(roll)
		return roll

	def render(self):
		ret = '<form action="{0.name}/roll" method="post">' \
		      '<input type="text" name="rollspec" value="1d4+1">' \
		      '<input type="submit" value="Roll!">' \
		      '</form>'
		ret = ret.format(self)
		ret += '<br>'.join(roll.render() for roll in self.rolls[::-1])
		return ret


class Roll(object):
	def __init__(self, user, n, sides, bonus):
		self.user, self.n, self.sides, self.bonus = user, n, sides, bonus
		self.timestamp = time.time()
		self.results = [die(sides) for x in range(n)]

	@property
	def value(self):
		return sum(self.results) + self.bonus

	@property
	def rollspec(self):
		return "{self.n}d{self.sides}{bonus}".format(
			self=self, bonus='+{}'.format(self.bonus) if self.bonus else ''
		)

	@property
	def timestr(self):
		return time.strftime('%T', time.gmtime(self.timestamp))

	def render(self):
		ret = "{self.timestr} {self.user}: {self.rollspec} = {self.value}".format(self=self)
		if self.n == 1 and not self.bonus: return ret
		ret += ' = '
		ret += ' + '.join(map(str, self.results))
		if self.bonus: ret += " + {}".format(self.bonus)
		return ret
