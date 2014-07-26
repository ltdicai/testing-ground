from stats import Stats
import numpy as np

class NPC(object):
	def __init__(self, name):
		self.stats = Stats()
		self.name = name

	def show_hp(self):
		print "HP:", self.stats.hit_points

	def attack(self, enemy):
		mod = np.random.uniform(0.9, 1, 1)[0]
		a = self.stats.level*0.3
		b = (float(self.stats.attack)*4/enemy.stats.defense)*4.0 
		c = mod
		damage = max(int(a*b*c), 1)
		enemy.stats.hit_points -= damage
		print "BAM!", enemy.name, "was hit for",  damage
		enemy.stats.hit_points = max(enemy.stats.hit_points, 0)
		return damage

	def level_up(self):
		if self.stats.level < 99:
			self.stats.level += 1
			self.stats.max_hit_points = self.stats.level*8 
			rem_points = 3 
			stat_selector = []
			stat_selector.extend(self.stats.stats_names)
			while(rem_points > 0):
				rand_stat = np.random.choice(stat_selector, 1)
				rand_stat_increase = np.random.randint(1,rem_points+1)
				self.stats.modify_stat(rand_stat, rand_stat_increase) 
				stat_selector.remove(rand_stat)
				rem_points -= rand_stat_increase

	def level_to(self, lvl):
		if lvl > 99:
			lvl = 99
		while(self.stats.level < lvl):
			self.level_up() 

	def show_stats(self):
		print "/"*20
		print self.name, " (LV. " , self.stats.level , ")"
		print self.stats.hit_points , "/", self.stats.max_hit_points
		aux_hp = int((float(self.stats.hit_points)/ self.stats.max_hit_points)*20)
		txt_hp = "+"*aux_hp
		print "[{0:20}]".format(txt_hp)
		print "Att: ", self.stats.attack
		print "Def: ", self.stats.defense
		print "Lck: ", self.stats.luck
		print "/"*20

	def cure(self, hp):
		a = self.stats.hit_points + hp
		if a > self.stats.max_hit_points:
			result = self.stats.max_hit_points - self.stats.hit_points 
			self.stats.hit_points = self.stats.max_hit_points
		else:
			result = hp
			self.stats.hit_points = a
		return result
