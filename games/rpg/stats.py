class Stats(object):

	stats_names = ("attack", "defense", "luck")

	def __init__(self):
		self.attack = 10
		self.defense = 10
		self.luck = 10
		self.max_hit_points = 100
		self.hit_points = self.max_hit_points
		self.level = 1
		self.exp = 0

	def modify_stat(self, stat, mod):
		if stat == "attack":
			self.attack += mod
		elif stat == "defense":
			self.defense += mod
		elif stat == "luck":
			self.luck += mod
		else:
			print "Not a valid stat."