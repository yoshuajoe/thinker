import string

class Concluder(object):
	def conc(self, states, sta, obs):
		concluder = []	
		for sp in states:
			counter = 0
			for res in sta:
				counter = counter + 1
				if sp == res:
					concluder.append((sp, obs[counter-1]))
		return concluder